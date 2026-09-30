# AI Agent Skills Framework for Autonomous Data Analytics

## Framework Overview
This document defines the complete AI Agent Skill Architecture required to transform raw heterogeneous data (CSV, Excel, PDF, Text) into an automated analytics pipeline covering **Descriptive EDA**, **Predictions & Prognosis**, **Recommended Actions & Impact**, and **Executive Storytelling**.

---

## Architecture: 8 Specialists & 4 Core Skill Bundles

```text
                                  ┌───────────────────────────┐
                                  │      USER / API INPUT     │
                                  └─────────────┬─────────────┘
                                                │
                                                ▼
                                  ┌───────────────────────────┐
                                  │  A0 Orchestrator Agent    │
                                  └─────────────┬─────────────┘
                                                │
       ┌────────────────────────┬───────────────┴────────────────┬────────────────────────┐
       ▼                        ▼                                ▼                        ▼
┌──────────────┐      ┌──────────────────┐             ┌──────────────────┐     ┌──────────────────┐
│  Skill 01    │      │     Skill 02     │             │     Skill 03     │     │     Skill 04     │
│ Descriptive  │─────▶│   Predictions    │────────────▶│   Recommended    │────▶│  Orchestration   │
│ EDA & Visuals│      │    & Prognosis   │             │ Actions & Impact │     │   & Reporting    │
└──────────────┘      └──────────────────┘             └──────────────────┘     └──────────────────┘
  (Data Intake /        (Forecasting /                   (Optimization &          (Storytelling /
   Diagnostics)          Simulations)                     Prescriptions)           Validation)
```

---

## Skill Bundle Summary

| Skill ID | Skill Name | Scope & Capabilities | Key Outputs & Visuals | Primary Engine |
| :--- | :--- | :--- | :--- | :--- |
| **Skill 01** | `ai-skill-eda-visuals` | Data profiling, type normalization, KPI calculation, variance attribution, driver ranking | Quality score, variance matrix, waterfall/bullet/line charts | DuckDB / Python |
| **Skill 02** | `ai-skill-predictions-prognosis` | Feature prep, expanding-window backtesting, model selection (MAPE <= 15%), Monte Carlo simulation, sensitivity analysis | P10/P50/P90 forecasts, fan charts, Tornado diagrams, S-curves | Python / Prophet / ARIMA |
| **Skill 03** | `ai-skill-recommended-actions` | Action formulation, multi-criteria portfolio optimization, cost-benefit scoring, pro-forma post-action balance | Action pool, net benefit recovery, Before/After waterfall, impact matrix | Python / SciPy / PuLP |
| **Skill 04** | `ai-skill-orchestration-reporting` | End-to-end pipeline execution, deterministic Red-Amber-Green (RAG) rules, BLUF decision storytelling, independent validation | Executive RAG cards, BLUF decision story, validated HTML/Excel reports | SQLite / Jinja2 / HTML |

---

## Core Engineering Principles

1. **LLMs Do Not Own Financial Truth:** All numbers, variances, forecasts, and pro-forma balances come from deterministic code (DuckDB, Python). LLMs plan workflows, select tools, and explain takeaways.
2. **Deterministic RAG Governance:** Red-Amber-Green traffic-light thresholds are strictly evaluated via configuration YAML rules, preventing LLM status hallucination.
3. **Quantified Prescriptions:** Every recommendation includes an estimated gross saving, implementation cost, success probability, and post-intervention EAC position.
4. **Independent Validation Gate:** An independent validator agent reconciles figures across all stages before report publication.
