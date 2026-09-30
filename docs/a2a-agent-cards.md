# Agent-to-Agent (A2A) Protocol Specification & Agent Cards

This document defines the **Agent-to-Agent (A2A) Protocol** discovery manifests (**Agent Cards**) for all 8 specialized agents in the autonomous data analytics application.

---

## 1. Protocol Architecture Overview

The application utilizes A2A Protocol v1.0 for peer-to-peer horizontal agent collaboration, task delegation, and artifact exchange:
- **Discovery Endpoint:** `/.well-known/agent-card.json`
- **Transport Bindings:** HTTP+JSON, JSON-RPC 2.0, Server-Sent Events (SSE) streaming for long-running tasks.
- **Data Exchange:** Typed `Message`, `Task`, and `Artifact` payloads.

---

## 2. Master Agent Cards Manifest

```yaml
a2a_version: "1.0"
organization: "Autonomous Data Analytics Platform"
protocol_bindings: ["json-rpc-2.0", "http-json"]
transport_security: "TLS-1.3"

agents:
  - agent_id: "A0-orchestrator"
    name: "Orchestrator & Analysis Planner"
    description: "Main cognitive router. Classifies user intent, generates DAG execution plans, delegates subtasks, and handles iterative re-planning."
    endpoint: "https://analytics.internal/api/a2a/v1/orchestrator"
    agent_card_url: "https://analytics.internal/.well-known/agent-a0.json"
    capabilities:
      skills:
        - name: "plan_analysis"
          description: "Generate a multi-agent execution DAG based on user query and input dataset inventory."
        - name: "replan_analysis"
          description: "Modify task execution graph upon worker failure or data quality rejection."
    authentication:
      type: "oauth2"
      grant_type: "client_credentials"
      scopes: ["analytics:orchestrate"]

  - agent_id: "A1-intake"
    name: "Data Intake & Discovery Agent"
    description: "Inspects raw CSV, Excel, PDF, and text files. Validates footprints, delimiters, encodings, and row counts."
    endpoint: "https://analytics.internal/api/a2a/v1/intake"
    agent_card_url: "https://analytics.internal/.well-known/agent-a1.json"
    capabilities:
      skills:
        - name: "inspect_source"
          description: "Discover delimiters, BOM encodings, file modification dates, and row footprints."
        - name: "extract_document"
          description: "Extract structured entities and text excerpts from PDF, DOCX, or text files."
    authentication:
      type: "bearer_token"

  - agent_id: "A2-data-engineer"
    name: "Data Engineering & Quality Agent"
    description: "Profiles data quality, standardizes schemas, normalizes currencies/dates, and builds DuckDB star-schema models."
    endpoint: "https://analytics.internal/api/a2a/v1/data-engineer"
    agent_card_url: "https://analytics.internal/.well-known/agent-a2.json"
    capabilities:
      skills:
        - name: "profile_quality"
          description: "Audit completeness, uniqueness, outlier ratios, and debit/credit equality."
        - name: "build_analytical_model"
          description: "Construct conforming star-schema dimension and fact tables in analytics.duckdb."
    authentication:
      type: "bearer_token"

  - agent_id: "A3-diagnostic"
    name: "Diagnostic Analytics Agent"
    description: "Calculates KPIs, variance bridges, trends, anomalies, and performs driver contribution ranking."
    endpoint: "https://analytics.internal/api/a2a/v1/diagnostic"
    agent_card_url: "https://analytics.internal/.well-known/agent-a3.json"
    capabilities:
      skills:
        - name: "calculate_kpis"
          description: "Run SQL aggregations for actuals vs baselines (Budget, Target, Prior Period)."
        - name: "identify_drivers"
          description: "Perform Pareto and contribution analysis to isolate top variance drivers."
    authentication:
      type: "bearer_token"

  - agent_id: "A4-prognostic"
    name: "Prognostic & Simulation Agent"
    description: "Executes time-series backtesting, generates point/P10/P90 forecasts, Monte Carlo risk simulations, and sensitivity analysis."
    endpoint: "https://analytics.internal/api/a2a/v1/prognostic"
    agent_card_url: "https://analytics.internal/.well-known/agent-a4.json"
    capabilities:
      skills:
        - name: "select_backtest_model"
          description: "Evaluate candidate time-series models over expanding historical windows (MAPE <= 15%)."
        - name: "run_monte_carlo"
          description: "Simulate 10,000 probabilistic iterations over risk drivers to produce EAC distributions."
    authentication:
      type: "bearer_token"

  - agent_id: "A5-prescriptive"
    name: "Prescriptive Decision Agent"
    description: "Formulates candidate interventions, runs multi-criteria portfolio optimization under constraints, and reconciles post-action balances."
    endpoint: "https://analytics.internal/api/a2a/v1/prescriptive"
    agent_card_url: "https://analytics.internal/.well-known/agent-a5.json"
    capabilities:
      skills:
        - name: "generate_candidate_actions"
          description: "Formulate concrete intervention options mapped to identified root drivers."
        - name: "optimize_actions"
          description: "Solve constrained optimization problems for maximum net benefit under budget limits."
    authentication:
      type: "bearer_token"

  - agent_id: "A6-storytelling"
    name: "Storytelling & Visualization Agent"
    description: "Sequences BLUF executive narratives, applies governed RAG scorecards, and renders Tufte-compliant charts."
    endpoint: "https://analytics.internal/api/a2a/v1/storytelling"
    agent_card_url: "https://analytics.internal/.well-known/agent-a6.json"
    capabilities:
      skills:
        - name: "build_decision_story"
          description: "Construct BLUF executive narrative structures."
        - name: "select_build_visuals"
          description: "Generate Tufte-compliant visual charts (Bullet, Line, Waterfall, Tornado)."
    authentication:
      type: "bearer_token"

  - agent_id: "A7-validator"
    name: "Validator & Publisher Gatekeeper Agent"
    description: "Independently reconciles numeric totals, audits evidence citations, enforces publication guardrails, and exports HTML/Excel packages."
    endpoint: "https://analytics.internal/api/a2a/v1/validator"
    agent_card_url: "https://analytics.internal/.well-known/agent-a7.json"
    capabilities:
      skills:
        - name: "validate_results"
          description: "Reconcile cross-sectional calculations and verify source citation lineage."
        - name: "publish_reports"
          description: "Render responsive HTML executive reports and downloadable Excel workbooks."
    authentication:
      type: "oauth2"
      grant_type: "client_credentials"
      scopes: ["analytics:publish"]
```
