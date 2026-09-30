# Skill 04: Orchestration & Decision Storytelling (ai-skill-orchestration-reporting)

## Purpose
Orchestrate multi-agent data analytics workflows, enforce deterministic RAG (Red-Amber-Green) status thresholds, construct executive decision stories following Bottom-Line Up Front (BLUF) structure, validate outputs independently, and publish executive-ready reports.

## Trigger Conditions
- System orchestrates end-to-end multi-agent execution pipeline across intake, diagnostic, prognostic, and prescriptive stages.
- Need to synthesize complex quantitative analytics into executive briefings, RAG cards, or HTML reports.
- Final validation gatekeeper check before publishing deliverables to leadership.

## Primary Agent
**Orchestrator, Storytelling & Validator Agents (A0 / A6 / A7)**

## Inputs Schema (YAML)
```yaml
orchestration_request:
  user_objective: string
  source_data_files: list[string]
  reporting_format: html | excel | executive_briefing
  rag_threshold_config:
    cost_variance_pct:
      green: "<= 2.0%"
      amber: "between 2.0% and 7.5%"
      red: "> 7.5%"
    schedule_delay_days:
      green: "<= 5"
      amber: "between 6 and 20"
      red: "> 20"
```

## Workflow Execution Steps
1. **Pipeline Orchestration (A0 Orchestrator):**
   - Plan multi-agent stage execution: Intake -> Data Quality -> Diagnostics -> Prognostics -> Prescriptive -> Storytelling -> Validation.
   - Pass dataset references and typed state parameters between agents rather than passing raw prompt data.
2. **Deterministic Status RAG Application:**
   - Evaluate calculated KPIs against configuration rules. Never allow LLMs to assign arbitrary traffic-light colors.
   - Generate RAG cards containing metric name, status (RED/AMBER/GREEN), actual value, target, variance, trend arrow, and forecast.
3. **Decision Story Synthesis (BLUF Structure):**
   - Sequence narrative logically:
     1. Executive Answer (Status, Core Finding, Required Decision)
     2. Current Performance (KPIs & Variance Bridge)
     3. Root-Cause Diagnosis (Ranked Drivers)
     4. Prognostic Outlook (Base Forecast & P10/P90 Range)
     5. Recommended Actions & Impact (Cost-Benefit & Revised EAC)
     6. Governance & Traceability (Data Quality, Assumptions, Evidence Citations)
4. **Independent Validation & Publishing Gate (A7 Validator):**
   - Reconcile all numerical figures across sections.
   - Verify that all claims cite grounded evidence and that post-action math matches.
   - Veto publication if unsupported claims or un-reconciled numbers exist.

## Outputs Schema (YAML)
```yaml
orchestration_result:
  execution_summary:
    run_id: string
    stages_completed: list[string]
    validation_status: PASS | REJECTED
  rag_scorecard:
    - metric_name: string
      status: RED | AMBER | GREEN
      actual: float
      target: float
      variance: float
      trend: up | down | flat
  storytelling_narrative:
    bluf_headline: string
    executive_summary: string
    key_recommendations: list[string]
  published_artifacts:
    - artifact_name: string
      format: html | xlsx | pdf
      file_path: string
      audit_log_ref: string
```

## Guardrails
- **Deterministic RAG:** Status colors must originate from hardcoded governance configuration, not LLM inference.
- **Independent Veto:** Validation agent has strict authority to reject reports with un-reconciled figures or missing source citations.
- **Data Lineage & Traceability:** Every metric and visual must retain query and source dataset references.

## Definition of Done
- Complete multi-agent pipeline executed with audit trail stored in control database.
- Deterministic Red-Amber-Green scorecard evaluated against governed rules.
- BLUF-structured executive report validated and published to the Studio panel.
