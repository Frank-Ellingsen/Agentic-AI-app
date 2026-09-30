"""
run_agent_dag.py - Autonomous Data-to-Decision Agent DAG Runner
Uses official `google-genai` SDK with Gemini Flash 3.6 model and SQLite control store.
"""

import os
import sys
import json
import sqlite3
import time
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

# Official Google GenAI SDK
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("[WARNING] google-genai package not installed. Install with: pip install google-genai")
    genai = None

# Configuration
DB_PATH = os.getenv("SQLITE_DB_PATH", "control.db")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
API_KEY = os.getenv("GEMINI_API_KEY")

class AgentDAGRunner:
    def __init__(self, db_path: str = DB_PATH, model_name: str = MODEL_NAME):
        self.db_path = db_path
        self.model_name = model_name
        self.client = None
        
        if genai and API_KEY:
            self.client = genai.Client(api_key=API_KEY)
        elif genai:
            # Client will attempt to pick up GEMINI_API_KEY environment variable automatically
            try:
                self.client = genai.Client()
            except Exception as e:
                print(f"[SDK Init Notice] {e}")

    def get_db_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def log_system_event(self, trace_id: str, agent_id: str, event_type: str, message: str, payload: Dict = None):
        """Log structured audit logs to SQLite (Skill 37)."""
        conn = self.get_db_connection()
        try:
            conn.execute(
                """
                INSERT INTO system_logs (trace_id, agent_id, event_type, log_level, message, payload_json)
                VALUES (?, ?, ?, 'INFO', ?, ?)
                """,
                (trace_id, agent_id, event_type, message, json.dumps(payload or {}))
            )
            conn.commit()
        finally:
            conn.close()

    def log_gemini_usage(
        self, trace_id: str, agent_id: str, prompt_tokens: int, completion_tokens: int,
        latency_ms: int, status: str = "SUCCESS", error_msg: str = None
    ):
        """Log Gemini API token usage and cost tracking to SQLite (Skill 36)."""
        conn = self.get_db_connection()
        # Estimated cost for Gemini Flash 3.6 ($0.10 / 1M input, $0.40 / 1M output)
        estimated_cost = (prompt_tokens * 0.00000010) + (completion_tokens * 0.00000040)
        try:
            conn.execute(
                """
                INSERT INTO gemini_api_logs 
                (trace_id, agent_id, model_version, prompt_tokens, completion_tokens, total_tokens, estimated_cost_usd, latency_ms, status, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    trace_id, agent_id, self.model_name, prompt_tokens, completion_tokens,
                    prompt_tokens + completion_tokens, estimated_cost, latency_ms, status, error_msg
                )
            )
            conn.commit()
        finally:
            conn.close()

    def call_gemini_agent(
        self, trace_id: str, agent_id: str, system_instruction: str, user_prompt: str, json_schema: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Executes a structured call to Gemini 3.6 Flash via google-genai SDK."""
        if not self.client:
            raise RuntimeError("Gemini Client not initialized. Set GEMINI_API_KEY environment variable.")

        self.log_system_event(trace_id, agent_id, "AGENT_START", f"Starting execution for {agent_id}")
        start_time = time.time()

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.1,  # Low temperature for analytical precision
        )

        if json_schema:
            config.response_mime_type = "application/json"
            config.response_schema = json_schema

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=user_prompt,
                config=config,
            )

            latency_ms = int((time.time() - start_time) * 1000)
            
            # Extract token usage metadata from response
            usage = getattr(response, "usage_metadata", None)
            prompt_tokens = getattr(usage, "prompt_token_count", 0) if usage else 0
            completion_tokens = getattr(usage, "candidates_token_count", 0) if usage else 0

            self.log_gemini_usage(trace_id, agent_id, prompt_tokens, completion_tokens, latency_ms)
            self.log_system_event(trace_id, agent_id, "AGENT_COMPLETE", f"Finished execution in {latency_ms}ms")

            if json_schema:
                return json.loads(response.text)
            return {"raw_text": response.text}

        except Exception as e:
            latency_ms = int((time.time() - start_time) * 1000)
            self.log_gemini_usage(trace_id, agent_id, 0, 0, latency_ms, status="ERROR", error_msg=str(e))
            self.log_system_event(trace_id, agent_id, "AGENT_ERROR", f"Failed: {str(e)}")
            raise e

    def run_dag(self, job_id: str, tenant_id: str, dataset_ref: str, business_question: str):
        """Executes the full 6-phase analytical agent DAG."""
        trace_id = f"trace_{job_id}"
        print(f"[DAG] Starting Execution for Job: {job_id} | Tenant: {tenant_id} | Model: {self.model_name}")

        # Phase 1: Ingestion & Schema Agent (A1)
        a1_schema = {
            "type": "object",
            "properties": {
                "dataset_status": {"type": "string", "enum": ["valid", "data_quality_issues", "invalid"]},
                "schema_summary": {"type": "string"},
                "detected_metrics": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["dataset_status", "schema_summary"]
        }
        
        a1_sys = "You are Agent A1 (Data Ingestion & Profiler). Analyze the source dataset structure and return schema findings."
        a1_prompt = f"Analyze dataset reference '{dataset_ref}' for business context: {business_question}"
        a1_result = self.call_gemini_agent(trace_id, "A1_IngestionAgent", a1_sys, a1_prompt, a1_schema)
        print(f"  └─ A1 Schema Result: {a1_result['dataset_status']}")

        # Phase 2: Diagnostic Analytics Agent (A2)
        a2_schema = {
            "type": "object",
            "properties": {
                "kpis": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "actual": {"type": "number"},
                            "target": {"type": "number"},
                            "status": {"type": "string", "enum": ["RED", "AMBER", "GREEN"]}
                        }
                    }
                },
                "key_drivers": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["kpis", "key_drivers"]
        }
        
        a2_sys = "You are Agent A2 (Diagnostic Analytics Expert). Calculate core financial/operational KPIs and identify key variance drivers."
        a2_prompt = f"Given schema {json.dumps(a1_result)}, analyze variance for question: {business_question}"
        a2_result = self.call_gemini_agent(trace_id, "A2_DiagnosticAgent", a2_sys, a2_prompt, a2_schema)
        print(f"  └─ A2 Diagnostic Result: {len(a2_result['kpis'])} KPIs calculated.")

        # Phase 3: Forecasting & Prognosis Agent (A3)
        a3_schema = {
            "type": "object",
            "properties": {
                "forecast_summary": {"type": "string"},
                "expected_eac": {"type": "number"},
                "p10_eac": {"type": "number"},
                "p90_eac": {"type": "number"}
            },
            "required": ["forecast_summary", "expected_eac"]
        }
        a3_sys = "You are Agent A3 (Predictive Analytics & Monte Carlo Simulation). Output P10/P50/P90 projections."
        a3_prompt = f"Run projections based on KPIs: {json.dumps(a2_result['kpis'])}"
        a3_result = self.call_gemini_agent(trace_id, "A3_PredictiveAgent", a3_sys, a3_prompt, a3_schema)
        print(f"  └─ A3 Forecast Result: Expected EAC = {a3_result['expected_eac']}")

        # Phase 4: Prescriptive Action Agent (A4)
        a4_schema = {
            "type": "object",
            "properties": {
                "candidate_actions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "action_title": {"type": "string"},
                            "category": {"type": "string"},
                            "impact_usd": {"type": "number"},
                            "feasibility_score": {"type": "number"}
                        }
                    }
                }
            },
            "required": ["candidate_actions"]
        }
        a4_sys = "You are Agent A4 (Prescriptive Action Engine). Generate targeted, cost-saving candidate actions with quantified ROI."
        a4_prompt = f"Generate actions to address drivers: {json.dumps(a2_result['key_drivers'])}"
        a4_result = self.call_gemini_agent(trace_id, "A4_PrescriptiveAgent", a4_sys, a4_prompt, a4_schema)
        
        # Save actions to SQLite HITL Table (Skill 34)
        conn = self.get_db_connection()
        for idx, act in enumerate(a4_result["candidate_actions"]):
            conn.execute(
                """
                INSERT INTO candidate_actions (job_id, tenant_id, action_code, title, category, impact_amount, feasibility_score)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (job_id, tenant_id, f"ACT-{idx+1:03d}", act["action_title"], act["category"], act["impact_usd"], act["feasibility_score"])
            )
        conn.commit()
        conn.close()
        print(f"  └─ A4 Prescriptive Result: {len(a4_result['candidate_actions'])} actions generated and staged for HITL approval.")

        # Phase 5 & 6: Independent Auditor Gate (A7) & Publisher (A5/A6)
        a7_schema = {
            "type": "object",
            "properties": {
                "audit_status": {"type": "string", "enum": ["PASS", "REJECT"]},
                "audit_summary": {"type": "string"},
                "discrepancies_found": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["audit_status", "audit_summary"]
        }
        a7_sys = "You are Agent A7 (Independent Validation & Governance Gatekeeper). Audit mathematical consistency and reject unreconciled claims."
        a7_prompt = f"Audit reporting package: KPIs={json.dumps(a2_result['kpis'])}, Forecast={json.dumps(a3_result)}, Actions={json.dumps(a4_result)}"
        a7_result = self.call_gemini_agent(trace_id, "A7_AuditorAgent", a7_sys, a7_prompt, a7_schema)
        print(f"  └─ A7 Audit Gate Status: {a7_result['audit_status']}")

        return {
            "job_id": job_id,
            "status": "COMPLETED" if a7_result["audit_status"] == "PASS" else "AUDIT_REJECTED",
            "trace_id": trace_id,
            "a1_schema": a1_result,
            "a2_diagnostics": a2_result,
            "a3_forecast": a3_result,
            "a4_actions": a4_result,
            "a7_audit": a7_result
        }

if __name__ == "__main__":
    runner = AgentDAGRunner()
    print(f"Agent DAG Runner Initialized for model: {runner.model_name}")
    print("To execute a job, instantiate AgentDAGRunner().run_dag(job_id, tenant_id, dataset_ref, question)")
