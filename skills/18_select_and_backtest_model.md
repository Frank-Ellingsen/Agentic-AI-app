# 18 - Select and Backtest Model

## Purpose

Select and validate forecasting algorithms (Exponential Smoothing, Holt-Winters, ARIMA, Linear Trend, or Ensembles) via expanding-window historical backtesting, evaluating Mean Absolute Percentage Error (MAPE) and Root Mean Squared Error (RMSE).

## Trigger conditions

- Feature dataset prepared (`17_prepare_forecast_dataset.md`).
- Evaluation of competing forecasting algorithms prior to final publication.

## Primary agent

**Forecasting Model Selection Agent**

## Inputs

```yaml
model_selection_request:
  train_data: string
  candidate_models: ["naive_last_period", "moving_average", "holt_winters_ets", "auto_arima", "linear_trend"]
  backtest_folds: 4
  evaluation_metric: "mape" | "rmse"
  max_acceptable_mape: 0.15 # 15% error
```

## Outputs

```yaml
model_selection_result:
  selected_model: string
  model_parameters: dict
  backtest_performance:
    - model_name: string
      mean_mape: float
      mean_rmse: float
      rank: integer
  baseline_improvement_pct: float
```

## Responsibilities

1. **Expanding Window Backtesting:** Train models on periods $1..T$, test on $T+1..T+h$, expanding $T$ sequentially.
2. **Error Metric Calculation:** Compute MAPE and RMSE to assess both average percentage error and sensitivity to large deviations.
3. **Model Selection:** Choose the simplest model that meets accuracy targets (parsimony principle).

## Guardrails

- Do not select over-parameterized complex models that overfit short historical cycles.
- Always compare against a naive "no-change" baseline.

## Definition of done

- Winning forecasting model selected and ranked with documented historical backtest error metrics.
