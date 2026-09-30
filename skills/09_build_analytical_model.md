# 09 - Build Analytical Model

## Purpose

Construct an analytical dimensional model (Star Schema) linking business facts (`FactGL`, `FactBudget`, `FactForecast`, `FactFTE`) to shared conforming dimensions (`DimDate`, `DimAccount`, `DimOrganization`, `DimProject`) to enable high-speed OLAP slicing, metric aggregation, and drill-downs.

## Trigger conditions

- Cleaned and normalized datasets prepared.
- Analytical querying layer or BI reporting model setup.

## Primary agent

**Dimensional Modeling Agent**

## Inputs

```yaml
analytical_model_request:
  facts:
    - name: FactGL
      grain: transaction
      value_columns: [Belop_signert]
    - name: FactBudget
      grain: monthly_account
      value_columns: [BudsjettBelop]
    - name: FactForecast
      grain: monthly_version_account
      value_columns: [ForecastBelop]
    - name: FactFTE
      grain: monthly_org_position
      value_columns: [Aarsverk]
  conformed_dimensions:
    - DimDate
    - DimAccount
    - DimOrganization
    - DimProject
```

## Outputs

```yaml
analytical_model_result:
  model_name: string
  fact_tables: list[string]
  dimension_tables: list[string]
  star_schema_relationships: list[object]
  semantic_measures:
    - Actual_Amount: "SUM(FactGL.Belop_signert)"
    - Budget_Amount: "SUM(FactBudget.BudsjettBelop)"
    - Forecast_Amount: "SUM(FactForecast.ForecastBelop)"
    - FTE_Count: "SUM(FactFTE.Aarsverk)"
```

## Responsibilities

1. **Conformed Dimensions:** Ensure `DimDate`, `DimAccount`, and `DimOrganization` serve as the single source of truth across all fact tables.
2. **Grain Alignment:** Reconcile differences in time grain (e.g. daily transactions in GL vs monthly figures in Budget/Forecast).
3. **Semantic Layer Definition:** Define standardized measure definitions for downstream SQL and DAX queries.

## Guardrails

- Never combine fact tables with different grains into a single flat table without explicit aggregation.
- All dimensional keys must be validated against dimension primary keys.

## Definition of done

- The star schema model is fully specified and ready for in-memory DuckDB or SQL execution.
