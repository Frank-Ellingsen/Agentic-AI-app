# Autonomous Data Analytics Platform — Master Project Manifest

This document serves as the **Master System Deployment Manifest** linking all architectural components, agent cards, skill definitions, protocol interfaces, data contracts, and execution runtimes for the autonomous data analytics application.

---

## 1. System Overview & Technology Stack

| Layer | Technology | Primary Responsibility |
| :--- | :--- | :--- |
| **Cognitive Intelligence** | Gemini LLM | Intent classification, DAG planning, decision storytelling, and agent reasoning. |
| **Agent Topology** | 8 Specialist Agents (A0–A7) | Specialized division of labor across the analytical lifecycle. |
| **Skill Architecture** | 4 Core Bundles / 30 Sub-skills | Bounded, testable business capabilities mapped across agents. |
| **Vertical Tool Protocol** | Model Context Protocol (MCP) | JSON-RPC 2.0 interface for DuckDB, Python, SQLite, and chart tools. |
| **Horizontal Agent Protocol** | Agent-to-Agent (A2A) Protocol | Peer discovery via Agent Cards (`.well-known/agent-card.json`), Task lifecycle, and Artifacts. |
| **Analytics Compute Engine** | DuckDB (`analytics.duckdb`) | High-performance columnar SQL, window functions, and Star Schema joins. |
| **Control & Audit Database** | SQLite (`control.sqlite`) | Task DAG tracking, run state, RAG governance rules, and audit logs. |
| **Predictive & Prescriptive Engine** | Python 3.12 (`SciPy`, `Prophet`, `PuLP`) | Backtested forecasting, 10k-iteration Monte Carlo, and portfolio optimization. |
| **Reporting & Export Layer** | HTML5 / CSS3 / Jinja2 / Excel | Responsive BLUF executive web reports and drillable Excel workbooks. |

---

## 2. End-to-End Workflow Mapping (The 6 Phases)

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ PHASE I: Ingestion & Inspection (Skills 01–04)                                              │
│ - Agent: A1 (Data Intake)                                                                   │
│ - Output: Verified Source Manifest & raw file footprint                                     │
└──────────────────────────────┬──────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ PHASE II: Schema & Dimensional Modeling (Skills 05–10)                                      │
│ - Agent: A2 (Data Engineering)                                                              │
│ - Output: Data Quality Profile & Star Schema in analytics.duckdb (`model.*`)                 │
└──────────────────────────────┬──────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ PHASE III: Diagnostic Analytics & Visuals (Skills 11–16)                                     │
│ - Agent: A3 (Diagnostic)                                                                    │
│ - Output: Reconciled KPIs, Variance Bridge, Top 3–5 Drivers, Bullet & Waterfall Visuals     │
└──────────────────────────────┬──────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ PHASE IV: Prognostics & Simulation (Skills 17–22)                                            │
│ - Agent: A4 (Prognostic)                                                                    │
│ - Output: Backtested Forecast (MAPE <= 15%), P10/P50/P90 Intervals, Fan/Tornado Charts      │
└──────────────────────────────┬──────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ PHASE V: Prescriptive Optimization & Impact (Skills 23–26)                                  │
│ - Agent: A5 (Prescriptive)                                                                  │
│ - Output: Optimized Action Plan, Cost-Benefit Ratios, Revised Pro-Forma EAC Balance         │
└──────────────────────────────┬──────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ PHASE VI: Storytelling, Validation & Publishing (Skills 27–30)                              │
│ - Agents: A0 (Orchestrator), A6 (Storytelling), A7 (Validator)                              │
│ - Output: BLUF Executive Decision Story, Governed RAG Scorecard, Published HTML/Excel Report │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Directory Layout & File Catalog

```text
/workspace/out/
├── master-project-manifest.md           ← Complete System Architecture Manifest (This File)
├── gemini-system-instructions.md        ← Gemini System Prompts for A0-A7
├── a2a-agent-cards.md                  ← A2A Protocol Agent Cards Definition
├── mcp-tools-specification.md           ← Model Context Protocol Tool Schemas
├── ai-agent-skills-framework.md        ← Master 8-Agent / 4-Skill Framework
├── eda-visuals-skill.md                 ← Skill 01 Specification (Descriptive EDA)
├── predictions-prognosis-skill.md       ← Skill 02 Specification (Predictions & Prognosis)
├── recommended-actions-skill.md         ← Skill 03 Specification (Recommended Actions)
└── orchestration-reporting-skill.md     ← Skill 04 Specification (Orchestration & Storytelling)
```

---

## 4. Key Architectural Contracts & Guardrails

1. **Deterministic Calculation Mandate:** All numeric outputs, forecasts, and pro-forma balances must originate from `analytics.duckdb` or Python compute scripts.
2. **Governed RAG Rules:** Traffic-light status indicators are strictly evaluated using configuration rules in `config/rag/status_rules.yaml`.
3. **Independent Validation Gate:** Agent A7 acts as an independent auditor with veto power to reject reports containing un-reconciled totals or missing source citations.
4. **Publication Target:** All final executive deliverables are rendered as responsive, semantic HTML reports and downloadable Excel workbooks synced directly to the user's Studio panel.
