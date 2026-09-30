# 13 - Analyze Trends

## Purpose

Analyze historical trajectories, run-rates, moving averages, and seasonality across time-series metrics to evaluate momentum, acceleration, and early warnings of cost runaway.

## Trigger conditions

- Periodic trend reporting across trailing 12 months (T12M) or cumulative project lifecycle.
- Identifying whether an adverse monthly variance is a one-off anomaly or an emerging structural trend.

## Primary agent

**Trend & Time-Series Agent**

## Inputs

```yaml
trend_analysis_request:
  metric: string # e.g. "Monthly Actual Cost" or "FTE Count"
  time_grain: "daily" | "weekly" | "monthly" | "quarterly"
  history_window_periods: 24
  smoothing_window: 3 # 3-month moving average
```

## Outputs

```yaml
trend_analysis_result:
  metric: string
  periods: list[string]
  actual_values: list[float]
  moving_average: list[float]
  compound_monthly_growth_rate: float
  trajectory: "accelerating" | "stable" | "decelerating" | "inflection"
  run_rate_annualized: float
```

## Responsibilities

1. **Run-Rate Calculation:** Determine current monthly burn rate and annualize it to evaluate full-year budget sufficiency.
2. **Moving Averages:** Apply 3-month or 6-month trailing moving averages to filter out calendar noise and invoice timing lags.
3. **Trajectory Classification:** Classify direction as stable, accelerating overspend, or improving cost efficiency.

## Guardrails

- Account for seasonality (such as summer vacation dip or December fiscal closing surge) before inferring structural trends.

## Definition of done

- Trend analysis artifact generated with calculated run-rates and trajectory classifications.
