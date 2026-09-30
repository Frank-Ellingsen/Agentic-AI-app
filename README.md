# Autonomous Data Analytics Platform (Skills 01–37)

[![Python 3.12](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![Google GenAI SDK](https://img.shields.io/badge/SDK-google--genai-green.svg)](https://pypi.org/project/google-genai/)
[![Gemini 3.6 Flash](https://img.shields.io/badge/LLM-Gemini_3.6_Flash-orange.svg)](https://deepmind.google/technologies/gemini/)
[![SQLite Engine](https://img.shields.io/badge/Database-SQLite_WAL-skyblue.svg)](https://www.sqlite.org/)
[![DuckDB Analytics](https://img.shields.io/badge/Engine-DuckDB-yellow.svg)](https://duckdb.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

An enterprise-grade, multi-agent autonomous data analytics application and financial controlling platform. Powered by **Google Gemini 3.6 Flash**, **DuckDB**, **SQLite**, and **FastAPI**, this system converts raw, heterogeneous financial & operational data into governed executive decision reports, P10/P50/P90 time-series forecasts, Monte Carlo risk simulations, and Human-in-the-Loop (HITL) action portfolios.

---

## 🌟 Key Architecture & Capabilities

* **37 Operational Agent Skills:** Full operational coverage across 6 analytical phases (Ingestion, Schema Modeling, Diagnostics, Prognostics, Prescriptions, Publishing) and 7 application management skills (Auth/RBAC, Live Connectors, Interactive SSE UI, HITL Approvals, Task Queues, MLOps Governance, Database Observability).
* **11 Model Context Protocol (MCP) Tools:** Standardized JSON-RPC 2.0 tool schemas connecting Gemini agents to DuckDB columnar queries, time-series backtesting, SciPy portfolio optimization, Tufte visual rendering, and SQLite WAL control stores.
* **Deterministic Financial Truth:** Stated principle across all skills that LLMs do **not** calculate numbers or infer traffic-light colors in prompt text. All figures originate from DuckDB and Python compute engines.
* **Edward Tufte Data-Ink Design:** High-data-ink visuals (Bullet charts, Fan charts, Waterfall bridges, Tornado sensitivity diagrams) with zero vertical gridlines, direct end-point labeling, right-aligned numeric data, and highlight-only colors for active variances.
* **Independent Validator Audit Gate:** Agent A7 acts as an independent auditor with absolute veto authority (`REJECT`) to halt publication if un-reconciled totals or un-cited claims exist.

---

## 📁 Repository Directory Structure

```text
/workspace/
├── app/                                  # Web Application Layer
│   ├── index.html                        # Single-Page Dashboard (Tailwind, Chart.js, Lucide)
│   └── main.py                           # FastAPI Gateway Server (REST / SSE endpoints)
├── data/                                 # Sample Data Fixtures & Documents
│   ├── sample_audit_notes.md             # Qualitative accounting audit notes
│   ├── sample_budget_vs_actual.csv       # Q3 2025 department variance dataset
│   ├── sample_executive_commentary.txt   # Executive management commentary text
│   ├── sample_general_ledger.csv         # 1,526 granular GL posting transactions
│   ├── sample_revenue_forecast.csv       # 26-month time-series financial dataset
│   └── sample_vendor_contract.pdf        # Vendor agreement PDF fixture
├── database/                             # Database Schemas & DDL
│   └── control_schema.sql                # Production SQLite WAL-enabled DDL & seed script
├── docs/                                 # System Architecture & Specifications
│   ├── a2a-agent-cards.md                # Agent-to-Agent Protocol Cards
│   ├── ai-agent-skills-framework.md      # Master 4-Skill Bundle Framework
│   ├── app-development-requirements.md   # Application Development Requirements
│   ├── app-skills-framework-extension.md  # Skills 31–37 & Extended MCP Tools 7–11
│   ├── app-starter-code.md               # App Starter Code Package
│   ├── eda-visuals-skill.md              # Skill 01 Spec (Descriptive EDA)
│   ├── gemini-system-instructions.md      # Agent System Prompts (A0–A7)
│   ├── master-project-manifest.md         # Master Architecture Blueprint
│   ├── mcp-tools-specification.md         # Core MCP Tools 1–6 Specifications
│   ├── orchestration-reporting-skill.md # Skill 04 Spec (Orchestration & Storytelling)
│   ├── predictions-prognosis-skill.md    # Skill 02 Spec (Predictions & Prognosis)
│   ├── recommended-actions-skill.md     # Skill 03 Spec (Recommended Actions)
│   └── reporting-expert-SKILL.md         # Executive Reporting Skill Pack
├── skills/                               # 30 Operational Sub-Skill Contracts
│   ├── 01_inspect_source.md              # Phase I: Ingestion Inspection Contract
│   ├── 02_parse_tabular.md               # Phase I: Tabular Parsing Contract
│   ├── ...                               # Phase II to V Contracts
│   └── 30_publish_reports.md             # Phase VI: Publishing Contract
├── src/                                  # Python Execution Code & SDK Engines
│   ├── document_parser_helper.py         # Gemini 3.6 Flash PDF & Document Parser (Skill 04)
│   └── run_agent_dag.py                  # Official google-genai SDK DAG Runner (Gemini 3.6)
├── .env.example                          # Environment variable configuration template
├── .gitignore                            # Git exclusion rules
├── LICENSE                               # MIT License
└── README.md                             # Master Workspace Index & Execution Guide
```

---

## ⚡ Quickstart & Installation

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/your-username/autonomous-data-analytics-platform.git
cd autonomous-data-analytics-platform

# Copy environment variables
cp .env.example .env
```

Set your Google Gemini API key inside `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.6-flash
SQLITE_DB_PATH=database/control.sqlite
```

### 2. Install Dependencies
```bash
pip install fastapi uvicorn google-genai pypdf duckdb scipy prophet pulp
```

### 3. Initialize SQLite Control Database
```bash
sqlite3 database/control.sqlite < database/control_schema.sql
```

### 4. Run the Agent DAG Execution Engine
```bash
python src/run_agent_dag.py
```

### 5. Launch Web Application Server
```bash
python app/main.py
```
Open `http://localhost:8000` in your browser to view the interactive studio.

---

## 🛠️ Technology Stack

| Layer | Technology | Primary Responsibility |
| :--- | :--- | :--- |
| **Cognitive Intelligence** | Google Gemini 3.6 Flash (`google-genai` SDK) | Intent classification, DAG planning, decision storytelling, structured extraction. |
| **Agent Topology** | 8 Specialist Agents (A0–A7) | Division of labor across Ingestion, Engineering, Diagnostics, Prognostics, Prescriptions, Storytelling, and Independent Audit. |
| **Skill Architecture** | 37 Operational Skills (01–37) | Bounded, testable business capabilities covering analytical pipelines and web app operations. |
| **Vertical Tool Protocol** | Model Context Protocol (MCP v1.0) | 11 JSON-RPC 2.0 tools for DuckDB, Python, SQLite, and Tufte charts. |
| **Analytics Compute Engine** | DuckDB (`analytics.duckdb`) | High-performance columnar SQL, window functions, and Star Schema joins. |
| **Control & Audit Database** | SQLite 3 (`control.sqlite` WAL mode) | Task DAG tracking, RBAC, job queue, HITL approvals, MLOps token logs, and audit trails. |
| **Web Gateway & UI** | FastAPI / HTML5 / Tailwind CSS / Chart.js | Responsive Single-Page Application (SPA) with real-time Server-Sent Events (SSE). |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
