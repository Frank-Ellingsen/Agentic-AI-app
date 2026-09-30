# 11 - Calculate KPIs

## Purpose

Calculate core business, financial, and operational Key Performance Indicators (KPIs), specifically Actual Cost, Budget, Latest Forecast, Estimate at Completion (EAC), Estimate to Complete (ETC), Cost Variance (CV), Schedule Variance (SV), and Full-Time Equivalent (FTE) labor burn rates.

## Trigger conditions

- Periodic monthly reporting close.
- Ad-hoc project health checks or executive dashboard refresh.

## Primary agent

**Financial Controller / KPI Calculation Agent**

## Inputs

```yaml
kpi_calculation_request:
  reporting_period: string # e.g. "2024-Q3" or "2024-10"
  financial_data:
    actual_table: "FactGL"
    budget_table: "FactBudget"
    forecast_table: "FactForecast"
    fte_table: "FactFTE"
  dimensions_slice:
    project_id: string | null
    org_unit: string | null
```

## Outputs

```yaml
kpi_calculation_result:
  metrics:
    actual_total: float
    budget_total: float
    forecast_total: float
    variance_to_budget: float # Actual - Budget
    variance_to_forecast: float # Actual - Forecast
    variance_pct_budget: float
    fte_total: float
    cost_performance_index: float # CPI = EV / AC if earned value available
    estimate_at_completion: float # EAC
    estimate_to_complete: float # ETC = EAC - AC
  calculation_metadata:
    currency: "NOK"
    grain: string
    timestamp: ISO-8601
```

## Responsibilities

1. **Standardized Formula Execution:**
   - $\text{Variance to Budget} = \text{Actual} - \text{Budget}$
   - $\text{Variance to Forecast} = \text{Actual} - \text{Forecast}$
   - $\text{Actual vs Budget \%} = \frac{\text{Actual}}{\text{Budget}} \times 100$
2. **Project Controlling Metrics:** Reconcile committed purchase orders, incurred costs, and latest forecast revisions into Estimate at Completion (EAC).
3. **Operational FTE Tracking:** Calculate average and period-ending full-time equivalent staffing count from timesheet and payroll facts.

## Guardrails

- Clear sign conventions: negative variance represents cost overruns or revenue shortfalls depending on account classification.
- Never mix different forecast versions without explicit version labeling.

## Definition of done

- Verified KPIs computed with 100% mathematical reconciliation to source ledger aggregates.
