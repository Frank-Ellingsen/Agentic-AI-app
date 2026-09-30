# Extended Application Operations & Governance Skills (Skills 31–37 & MCP Tools)
*Extension to the Autonomous Data-to-Decision Agent Skills Framework for Full-Fledged Application Integration.*

---

## Overview
This specification extends the core 30-skill analytical engine with **7 new operational agent skills** and **5 new Model Context Protocol (MCP) tools**. Tailored for a tech stack utilizing **SQLite** for backend control/data storage and the **Gemini API** (`gemini-2.0-flash` / `gemini-1.5-pro`) for AI intelligence, these extensions bridge analytical outputs into a production-grade, multi-tenant web application.

---

## 1. Operational Skills Specifications (31–37)

### 31 - Manage Authentication, Authorization & RBAC
#### Purpose
Enforce user authentication, multi-tenant organization isolation, Role-Based Access Control (RBAC), and row-level data scoping across all agent API interactions and analytical query execution using SQLite control tables.
#### Trigger conditions
* Any incoming user request or API payload entering the application server.
* Execution of analytical SQL queries or report generation requiring data scoping by organization or user role.
#### Primary agent
**Identity & Security Control Agent**
#### Inputs
```yaml
auth_request:
  jwt_token: string
  requested_resource: string
  action: "read" | "write" | "approve" | "admin"
  tenant_id: string
```
#### Outputs
```yaml
auth_result:
  authenticated: boolean
  user_id: string
  tenant_id: string
  roles: list[string]
  row_level_filters: object
  status: "AUTHORIZED" | "DENIED"
  error_message: string | null
```
#### Responsibilities
1. **Token & Session Verification:** Validate incoming JWT token signatures and session freshness against the SQLite `user_sessions` table.
2. **Multi-Tenancy Enforcer:** Inject explicit `WHERE tenant_id = :tenant_id` clauses into all analytical SQL queries before execution in DuckDB or SQLite.
3. **Role & Permission Mapping:** Check user roles (`viewer`, `analyst`, `approver`, `admin`) against resource permissions in SQLite `rbac_permissions`.
#### Guardrails
* Never execute an un-scoped database query without explicit `tenant_id` isolation.
* Block requests immediately upon token expiration or invalid signature.
#### Definition of done
* Token validated, user identity resolved, and tenant-scoped SQL filter attached to execution context.


---

### 32 - Manage Live Connectors & Webhooks
#### Purpose
Ingest live streaming data, webhook events, and REST/GraphQL API feeds into SQLite staging tables, utilizing the Gemini API for automated unstructured payload extraction and schema alignment.
#### Trigger conditions
* Incoming HTTP webhook trigger (e.g. ERP payment event, inventory update).
* Scheduled cron execution for API polling (e.g. hourly financial sync).
#### Primary agent
**Live Data Ingestion Agent**
#### Inputs
```yaml
ingest_trigger:
  source_type: "webhook" | "rest_api" | "graphql"
  endpoint_name: string
  raw_payload: object | string
  auth_header: string
```
#### Outputs
```yaml
ingest_result:
  ingestion_id: string
  records_processed: integer
  staging_table: string
  schema_validation_status: "VALID" | "SCHEMA_MUTATED" | "ERROR"
  error_log: list[string]
```
#### Responsibilities
1. **Webhook Listener & Ingestion:** Ingest raw HTTP payloads into SQLite `raw_ingress_events` with payload checksums and timestamps.
2. **Gemini Payload Normalization:** Pass unstructured or mutated JSON payloads to Gemini API (`gemini-2.0-flash` with structured JSON output) to map fields to canonical schema tables.
3. **Staging Database Push:** Insert cleaned, typed records into SQLite/DuckDB staging tables for analytical ingestion (Skills 01–08).
#### Guardrails
* Reject unauthenticated webhooks missing HMAC signature verification.
* Idempotent ingestion: ignore duplicate events using payload hash checks.
#### Definition of done
* Raw payload logged to SQLite event store and parsed canonical records deposited into staging tables.


---

### 33 - Manage Interactive UI & Streaming API
#### Purpose
Provide a responsive WebSocket / Server-Sent Events (SSE) and REST API framework that feeds real-time agent reasoning steps, chart render specs, and scenario controls to web frontends (React/Vue/HTML5).
#### Trigger conditions
* User initiates an analytical workflow, scenario adjustment, or question in the web UI.
* Agent workflow needs to stream progress updates, intermediate visuals, or audit alerts to the client.
#### Primary agent
**Web Application Interface Agent**
#### Inputs
```yaml
ui_interaction_event:
  session_id: string
  user_id: string
  event_type: "run_analysis" | "adjust_scenario" | "chat_query" | "export"
  parameters: object
```
#### Outputs
```yaml
ui_stream_chunk:
  session_id: string
  chunk_type: "agent_thought" | "data_table" | "visual_spec" | "action_prompt" | "completion"
  payload: object
  timestamp: ISO-8601
```
#### Responsibilities
1. **Real-time Event Streaming:** Stream live agent execution logs and reasoning chunks to the frontend via SSE/WebSockets.
2. **Interactive Visual Formatting:** Render interactive chart configurations (Plotly/ECharts JSON) for frontend dynamic rendering.
3. **State Synchronization:** Maintain active UI session state and parameter selections in SQLite `ui_sessions`.
#### Guardrails
* Sanitize all rendered user inputs against XSS and injection attacks.
* Rate-limit API event streams per user session to prevent server overload.
#### Definition of done
* Execution progress and interactive visualization specs streamed to client with zero dropped frames.


---

### 34 - Manage Human-in-the-Loop (HITL) Approvals
#### Purpose
Govern candidate business actions (from Skills 23–25) through a multi-stage approval lifecycle (`draft` -> `pending_review` -> `approved` / `rejected` -> `executed`), capturing manager sign-offs and audit reasons in SQLite.
#### Trigger conditions
* Candidate optimization actions generated by Agent A5 (Skill 24).
* Threshold condition reached requiring executive authorization (e.g. expense re-allocation > $50,000).
#### Primary agent
**Action Governance & Approval Agent**
#### Inputs
```yaml
approval_request:
  action_id: string
  recommendation_summary: string
  financial_impact: number
  risk_level: "LOW" | "MEDIUM" | "HIGH"
  proposed_by_agent: string
```
#### Outputs
```yaml
approval_decision:
  action_id: string
  current_state: "APPROVED" | "REJECTED" | "MODIFIED"
  reviewer_user_id: string
  decision_notes: string
  approval_timestamp: ISO-8601
  audit_trail_id: string
```
#### Responsibilities
1. **Approval State Machine:** Track state transitions of candidate actions in SQLite `action_approvals` table.
2. **Review Routing:** Assign approval tasks to qualified user roles based on financial threshold and risk level.
3. **Override Audit Logging:** Log human overrides, modified action parameters, and justifications for compliance auditing.
#### Guardrails
* Prevent auto-execution of high-risk or high-value actions without explicit human approval.
* Enforce double-authorization for actions exceeding defined financial caps.
#### Definition of done
* Candidate action state updated in SQLite store with complete reviewer identity and decision timestamp.


---

### 35 - Manage Alerts, Notifications & Task Queue
#### Purpose
Manage asynchronous background task processing and multi-channel alerting (Email, Slack, Webhook, Web UI) triggered by analytical anomalies, status breaches (RED RAG), or completed report builds.
#### Trigger conditions
* Status RAG evaluation identifies RED alert on critical KPI (Skill 16).
* Anomaly detection flags statistical outlier or missing accrual (Skill 15).
* Long-running background job (e.g., Monte Carlo simulation) completes.
#### Primary agent
**Alerts & Task Dispatch Agent**
#### Inputs
```yaml
notification_event:
  event_type: "kpi_breach" | "anomaly_alert" | "report_ready" | "approval_needed"
  severity: "INFO" | "WARNING" | "CRITICAL"
  recipient_roles: list[string]
  message_title: string
  message_body: string
  deep_link_url: string
```
#### Outputs
```yaml
dispatch_result:
  event_id: string
  channels_notified: list[string]
  delivery_status: "DELIVERED" | "QUEUED" | "FAILED"
  queued_job_id: string | null
```
#### Responsibilities
1. **SQLite Job Queue Management:** Enqueue background execution jobs into SQLite `job_queue` (`pending`, `processing`, `completed`, `failed`).
2. **Alert Formatting & Delivery:** Format notification templates and dispatch via configured API channels (Slack, Webhook, SMTP).
3. **Alert Deduplication:** Suppress duplicate warning alerts within defined time windows (e.g., max 1 alert per 4 hours for same KPI).
#### Guardrails
* Never drop CRITICAL security or financial breach alerts.
* Implement retry-with-backoff logic for failed webhook dispatches.
#### Definition of done
* Notification successfully delivered to target channels and logged to SQLite alert history.


---

### 36 - Manage Gemini API Governance & MLOps
#### Purpose
Manage Gemini API key usage, token consumption tracking, prompt template versioning, response schema validation, and model drift auditing stored in SQLite.
#### Trigger conditions
* Any call to Gemini API for reasoning, extraction, forecasting, or narrative generation.
* Periodic audit of API token costs and LLM response latency.
#### Primary agent
**AI Governance & MLOps Agent**
#### Inputs
```yaml
gemini_api_call_request:
  model_name: "gemini-2.0-flash" | "gemini-1.5-pro"
  prompt_template_id: string
  input_variables: object
  expected_schema: object
  tenant_id: string
```
#### Outputs
```yaml
gemini_api_call_response:
  call_id: string
  response_json: object
  prompt_tokens: integer
  completion_tokens: integer
  total_cost_usd: number
  latency_ms: integer
  schema_valid: boolean
```
#### Responsibilities
1. **Gemini API Call Broker:** Route prompts through centralized wrapper enforcing retry limits, rate limits, and structured JSON output schema validation.
2. **Token & Cost Allocation:** Log token usage per tenant/agent in SQLite `gemini_usage_logs` for billing and quota controls.
3. **Prompt Versioning & Quality Check:** Store prompt templates in SQLite `prompt_templates` with semantic quality regression tracking.
#### Guardrails
* Block API calls if tenant monthly token budget is exceeded.
* Fallback or retry automatically on Gemini API rate limit (429) errors with exponential backoff.
#### Definition of done
* Gemini API response parsed, validated against schema, and usage metadata logged to SQLite.


---

### 37 - Manage Observability & Database Health
#### Purpose
Maintain system observability, structured JSON logging, distributed trace tracing, SQLite database health (WAL checkpointing, vacuuming, indexing), and automated database backup routines.
#### Trigger conditions
* Continuous system runtime logging.
* Scheduled database maintenance cron (e.g. daily SQLite VACUUM/WAL checkpoint).
* System exception or unhandled agent error.
#### Primary agent
**DevOps & System Observability Agent**
#### Inputs
```yaml
maintenance_command:
  action: "health_check" | "wal_checkpoint" | "backup_database" | "log_trace"
  trace_id: string | null
  error_payload: object | null
```
#### Outputs
```yaml
health_status_report:
  system_status: "HEALTHY" | "DEGRADED" | "UNHEALTHY"
  sqlite_db_size_mb: number
  wal_size_mb: number
  active_connections: integer
  last_backup_timestamp: ISO-8601
```
#### Responsibilities
1. **SQLite Database Maintenance:** Automate SQLite `PRAGMA wal_checkpoint(PASSIVE)` and zero-downtime backups.
2. **Structured Log Telemetry:** Write structured JSON execution logs with correlation IDs (`trace_id`) across all agent tools.
3. **Health & Readiness Endpoints:** Provide `/healthz` and `/readyz` endpoints for application monitoring.
#### Guardrails
* Prevent database lock escalation by maintaining WAL mode and short transaction windows.
* Trigger instant admin alerts upon database corruption or unhandled system exceptions.
#### Definition of done
* SQLite maintenance tasks completed cleanly and health report verified.


---

## 2. Extended MCP Tools Specification

### Extended Model Context Protocol (MCP) Tools Specification (Skills 31–37)
This specification adds **5 new MCP tools** to support SQLite storage, Gemini API governance, user authentication, human-in-the-loop approvals, and background job queuing.

--------------------------------------------------------------------------------

#### Extended MCP Tool Definitions

##### Tool 7: mcp_sqlite_auth_and_rbac
Validates JWT session tokens, tenant context, and user permissions against SQLite RBAC tables.
```json
{
  "name": "mcp_sqlite_auth_and_rbac",
  "description": "Authenticates user tokens, checks role-based permissions, and retrieves tenant row-level SQL filters from SQLite control tables.",
  "parameters": {
    "type": "object",
    "properties": {
      "jwt_token": {
        "type": "string"
      },
      "required_permission": {
        "type": "string",
        "description": "e.g. reports:publish, actions:approve, data:query"
      },
      "tenant_id": {
        "type": "string"
      }
    },
    "required": ["jwt_token", "required_permission"]
  }
}
```

--------------------------------------------------------------------------------

##### Tool 8: mcp_gemini_structured_call
Executes Gemini API requests (`gemini-2.0-flash` / `gemini-1.5-pro`) with strict JSON Schema enforcement, automated retries, and token usage tracking in SQLite.
```json
{
  "name": "mcp_gemini_structured_call",
  "description": "Routes prompt to Gemini API with JSON Schema enforcement, retries, and token cost logging into SQLite.",
  "parameters": {
    "type": "object",
    "properties": {
      "model": {
        "type": "string",
        "enum": ["gemini-2.0-flash", "gemini-1.5-pro"],
        "default": "gemini-2.0-flash"
      },
      "prompt": {
        "type": "string"
      },
      "response_schema": {
        "type": "object",
        "description": "JSON Schema object enforcing structured model output."
      },
      "tenant_id": {
        "type": "string"
      }
    },
    "required": ["prompt", "response_schema"]
  }
}
```

--------------------------------------------------------------------------------

##### Tool 9: mcp_sqlite_job_queue
Manages asynchronous background jobs (ingestion, alerts, Monte Carlo runs) in the SQLite task queue.
```json
{
  "name": "mcp_sqlite_job_queue",
  "description": "Enqueues, dequeues, or updates background task state in the SQLite job_queue table.",
  "parameters": {
    "type": "object",
    "properties": {
      "action": {
        "type": "string",
        "enum": ["enqueue", "poll_next", "update_status"]
      },
      "job_type": {
        "type": "string",
        "description": "e.g. process_webhook, dispatch_alert, run_monte_carlo"
      },
      "payload": {
        "type": "object"
      },
      "job_id": {
        "type": "string"
      },
      "status": {
        "type": "string",
        "enum": ["pending", "processing", "completed", "failed"]
      }
    },
    "required": ["action"]
  }
}
```

--------------------------------------------------------------------------------

##### Tool 10: mcp_sqlite_hitl_approval
Updates candidate action lifecycle states (`pending_review`, `approved`, `rejected`), user signatures, and audit reasons in SQLite.
```json
{
  "name": "mcp_sqlite_hitl_approval",
  "description": "Logs human-in-the-loop review decisions, parameter overrides, and sign-off timestamps in SQLite action_approvals.",
  "parameters": {
    "type": "object",
    "properties": {
      "action_id": {
        "type": "string"
      },
      "decision": {
        "type": "string",
        "enum": ["APPROVED", "REJECTED", "MODIFIED"]
      },
      "reviewer_user_id": {
        "type": "string"
      },
      "decision_notes": {
        "type": "string"
      },
      "modified_parameters": {
        "type": "object"
      }
    },
    "required": ["action_id", "decision", "reviewer_user_id"]
  }
}
```

--------------------------------------------------------------------------------

##### Tool 11: mcp_sqlite_observability_maintenance
Performs health checks, WAL checkpoints, database size inspection, and automated zero-downtime backups on SQLite database files.
```json
{
  "name": "mcp_sqlite_observability_maintenance",
  "description": "Executes SQLite PRAGMA checks, WAL checkpoints, and backup tasks to ensure database health.",
  "parameters": {
    "type": "object",
    "properties": {
      "command": {
        "type": "string",
        "enum": ["health_check", "wal_checkpoint", "backup", "vacuum"]
      },
      "database_path": {
        "type": "string",
        "default": "control.sqlite"
      }
    },
    "required": ["command"]
  }
}
```
