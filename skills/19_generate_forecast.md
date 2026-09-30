# 19 - Generate Forecast

## Purpose

Generate forward-looking point estimates and prediction intervals (P10, P50, P90) across the planning horizon, producing full-year Estimate at Completion (EAC) projections and expected budget gap trajectories.

## Trigger conditions

- Validated model selected (`18_select_and_backtest_model.md`).
- Monthly or quarterly forecast cycle execution.

## Primary agent

**Forecasting Execution Agent**

## Inputs

```yaml
generate_forecast_request:
  selected_model: string
  horizon_months: 12
  confidence_intervals: [0.80, 0.95] # P10/P90, P2.5/P97.5
  known_future_commitments: map[period, committed_amount]
```

## Outputs

```yaml
generate_forecast_result:
  forecast_series:
    - period: string
      point_estimate: float # P50
      lower_bound_p10: float
      upper_bound_p90: float
  annual_totals:
    actual_year_to_date: float
    forecast_remaining_to_complete: float # ETC
    estimate_at_completion: float # EAC = YTD + ETC
    variance_vs_approved_budget: float
```

## Responsibilities

1. **Horizon Projection:** Generate monthly forward estimates for the remaining fiscal periods.
2. **Confidence Intervals:** Calculate prediction bands reflecting historical volatility and forecast decay over distance.
3. **EAC Assembly:** Combine actuals incurred through close date with forecasted remaining periods to calculate EAC.

## Guardrails

- Ensure the transition between the last actual period and first forecast period does not exhibit an artificial step discontinuity.
- Express uncertainty clearly: never present a point estimate without its surrounding interval.

## Definition of done

- Completed forward-looking forecast with P10, P50, and P90 intervals and calculated full-year EAC.
