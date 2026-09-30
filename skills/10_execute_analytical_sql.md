# 10 - Execute Analytical SQL

## Purpose

Execute optimized analytical SQL transformations and aggregations using local-first analytical SQL engines (**DuckDB** for high-performance columnar analytics, with **SQLite** for lookup queries), calculating summaries and complex window functions.

## Trigger conditions

- Analytical model defined (`09_build_analytical_model.md`).
- Metric queries, time-series rollups, or cohort aggregations requested.

## Primary agent

**SQL Execution Agent**

## Inputs

```yaml
sql_execution_request:
  engine: "duckdb" | "sqlite"
  database: ":memory:" | filepath
  registered_views: list[string]
  sql_queries:
    - query_id: string
      purpose: string
      sql: string
```

## Outputs

```yaml
sql_execution_result:
  query_id: string
  execution_time_ms: float
  rows_returned: integer
  columns: list[string]
  result_records: list[dict]
  plan_summary: string
```

## Responsibilities

1. **Local-First Execution:** Leverage DuckDB's vectorized query execution directly over CSVs or Parquet files without external server overhead.
2. **CTE Organization:** Structure queries using clean Common Table Expressions (CTEs) separating raw extraction, dimension joins, and metric calculations.
3. **Window Functions:** Compute cumulative sums (year-to-date), moving averages, and period-over-period differences.

## Guardrails

- Ensure zero-division guards are applied in SQL: `NULLIF(denominator, 0)`.
- Avoid `SELECT *`; explicitly name all columns and use descriptive aliases.

## Definition of done

- Analytical SQL queries execute deterministically and return typed tabular results within performance budgets.
