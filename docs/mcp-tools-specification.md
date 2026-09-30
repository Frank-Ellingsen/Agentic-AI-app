# Model Context Protocol (MCP) Tools Specification

This document defines the **Model Context Protocol (MCP)** Tool Schemas for the vertical agent-to-tool and data resource execution layer.

---

## 1. MCP Server Architecture

The MCP Server operates as a JSON-RPC 2.0 client-server broker between Gemini LLM agents and the underlying execution engines:
- **Local Engine:** `DuckDB v1.0+` (Columnar analytics), `SQLite 3` (Control state & run logs), `Python 3.12` (GSL/SciPy/Prophet compute).
- **Transport:** Standard input/output (`stdio`) and HTTP with Server-Sent Events (`SSE`).
- **Security:** Schema validation, strict parameter typing, and sandboxed execution.

---

## 2. Core MCP Tool Definitions

### Tool 1: `mcp_duckdb_execute_sql`
Executes vectorized analytical SQL queries over Parquet, CSV, or DuckDB relational tables.

```json
{
  "name": "mcp_duckdb_execute_sql",
  "description": "Executes vectorized analytical SQL queries in DuckDB over analytics.duckdb or raw CSV/Parquet files.",
  "parameters": {
    "type": "object",
    "properties": {
      "query_id": {
        "type": "string",
        "description": "Unique identifier for query tracing and audit logging."
      },
      "sql_statement": {
        "type": "string",
        "description": "Clean, optimized SQL statement with zero-division guards NULLIF()."
      },
      "read_only": {
        "type": "boolean",
        "default": true
      }
    },
    "required": ["query_id", "sql_statement"]
  }
}
```

---

### Tool 2: `mcp_python_run_forecast`
Executes time-series backtesting, model selection, and point/interval forecast generation.

```json
{
  "name": "mcp_python_run_forecast",
  "description": "Backtests time-series models (Prophet, ARIMA, ETS), selects best model (MAPE <= 15%), and outputs P10/P50/P90 forecasts.",
  "parameters": {
    "type": "object",
    "properties": {
      "dataset_ref": {
        "type": "string",
        "description": "DuckDB table reference containing historical time-series data."
      },
      "target_column": {
        "type": "string"
      },
      "date_column": {
        "type": "string"
      },
      "horizon_periods": {
        "type": "integer",
        "default": 12
      },
      "confidence_levels": {
        "type": "array",
        "items": { "type": "number" },
        "default": [0.80, 0.95]
      }
    },
    "required": ["dataset_ref", "target_column", "date_column", "horizon_periods"]
  }
}
```

---

### Tool 3: `mcp_python_run_monte_carlo`
Runs 10,000-iteration probabilistic risk simulations and sensitivity analysis.

```json
{
  "name": "mcp_python_run_monte_carlo",
  "description": "Runs Monte Carlo simulations over risk drivers to produce EAC probability distributions and Tornado sensitivity impacts.",
  "parameters": {
    "type": "object",
    "properties": {
      "iterations": {
        "type": "integer",
        "default": 10000
      },
      "random_seed": {
        "type": "integer",
        "default": 42
      },
      "variable_distributions": {
        "type": "object",
        "description": "JSON object defining mean, std, and min/max distributions per variable."
      }
    },
    "required": ["variable_distributions"]
  }
}
```

---

### Tool 4: `mcp_python_optimize_portfolio`
Solves multi-criteria decision analysis and constrained portfolio optimization problems.

```json
{
  "name": "mcp_python_optimize_portfolio",
  "description": "Runs SciPy/PuLP constrained optimization over candidate action pools to maximize net savings subject to budget limits.",
  "parameters": {
    "type": "object",
    "properties": {
      "candidate_actions_ref": {
        "type": "string"
      },
      "budget_cap": {
        "type": "number"
      },
      "max_implementation_days": {
        "type": "integer"
      }
    },
    "required": ["candidate_actions_ref", "budget_cap"]
  }
}
```

---

### Tool 5: `mcp_render_tufte_visual`
Renders direct-labeled, high-data-ink visual charts (Bullet, Line, Waterfall, Tornado, S-Curve).

```json
{
  "name": "mcp_render_tufte_visual",
  "description": "Generates direct-labeled matplotlib/seaborn charts conforming to Tufte data-ink design principles.",
  "parameters": {
    "type": "object",
    "properties": {
      "chart_type": {
        "type": "string",
        "enum": ["bullet", "line_trend", "waterfall", "tornado", "scurve_distribution"]
      },
      "title": {
        "type": "string"
      },
      "data_json": {
        "type": "string",
        "description": "Structured JSON string containing plot data points and labels."
      },
      "output_filename": {
        "type": "string"
      }
    },
    "required": ["chart_type", "title", "data_json", "output_filename"]
  }
}
```

---

### Tool 6: `mcp_sqlite_control_store`
Reads and writes system state, task run logs, audit trails, and dataset metadata.

```json
{
  "name": "mcp_sqlite_control_store",
  "description": "Reads/writes task execution status, dataset manifests, and audit events in control.sqlite.",
  "parameters": {
    "type": "object",
    "properties": {
      "action": {
        "type": "string",
        "enum": ["read_state", "write_run_log", "log_audit_event"]
      },
      "payload": {
        "type": "object"
      }
    },
    "required": ["action", "payload"]
  }
}
```
