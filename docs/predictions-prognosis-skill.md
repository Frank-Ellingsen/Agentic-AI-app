# Skill 02: Predictions & Prognosis Visuals (ai-skill-predictions-prognosis)

## Purpose
Prepare time-series feature datasets, backtest forecasting models, generate forward-looking point estimates with prediction intervals (P10/P50/P90), run Monte Carlo and sensitivity stress tests, and render fan chart visualizations.

## Trigger Conditions
- User requests forward-looking forecasts, Estimate at Completion (EAC) projections, or trajectory estimates.
- Need to quantify project/financial uncertainty or run "what-if" scenario stress tests.
- Generation of predictive fan charts, interval plots, or risk distribution diagrams.

## Primary Agent
**Prognostic Agent (A4)**

## Inputs Schema (YAML)
```yaml
prognosis_request:
  historical_data_ref: string   # Historical time-series table reference
  target_variable: string       # Metric to forecast (e.g., monthly_cost, demand)
  horizon_periods: integer      # Number of future periods (e.g., 12 months)
  candidate_models:
    - naive_last_period
    - moving_average
    - holt_winters_ets
    - auto_arima
    - linear_trend
  confidence_intervals: [0.80, 0.95] # Maps to P10/P90 and P2.5/P97.5
  simulation_params:
    monte_carlo_iterations: 10000
    random_seed: 42
    sensitivity_variables: list[string]
```

## Workflow Execution Steps
1. **Feature & Dataset Preparation:**
   - Construct regular time index, handle missing periods, evaluate seasonality, trend, and stationarity.
2. **Expanding Window Backtesting & Model Selection:**
   - Execute expanding-window backtest across historical folds.
   - Evaluate candidate algorithms using MAPE (Mean Absolute Percentage Error) and RMSE.
   - Select parsimonious model outperforming naive baseline with MAPE <= 15%.
3. **Forecast Generation & Uncertainty Simulation:**
   - Generate point forecasts (P50) and prediction intervals (P10, P90).
   - Execute Monte Carlo simulations over uncertain variables to derive cumulative probability distribution (S-curve).
   - Perform One-at-a-Time (OAT) sensitivity stress testing (+/- 15% swings) to identify top leverage parameters.
4. **Prognostic Visual Rendering:**
   - Render forecast fan charts with clear historical vs. forecast cutoff lines.
   - Plot Tornado diagrams for parameter sensitivity.
   - Generate S-curves with explicit target/budget threshold markers.

## Outputs Schema (YAML)
```yaml
prognosis_result:
  selected_model:
    model_name: string
    backtest_mape: float
    backtest_rmse: float
  forecast_summary:
    expected_eac_p50: float
    p10_optimistic: float
    p90_pessimistic: float
    budget_gap_p50: float
  scenarios:
    base_case: float
    upside_case: float
    downside_case: float
  sensitivity_top_drivers:
    - variable_name: string
      base_value: float
      high_swing_impact: float
      low_swing_impact: float
  visuals_manifest:
    - chart_id: string
      chart_type: fan_chart | tornado_diagram | scurve_distribution
      file_path: string
      key_takeaway: string
```

## Guardrails
- **Baseline Comparison:** Always compare ML/statistical forecasts against a naive no-change baseline.
- **Uncertainty Exposure:** Never output a point forecast without explicit prediction intervals (P10/P90).
- **Reproducibility:** Fix random seeds for Monte Carlo simulations to ensure exact auditability.

## Definition of Done
- Winning forecasting algorithm selected with backtest MAPE documented.
- P10/P50/P90 EAC projections and scenario matrix produced.
- Fan charts and Tornado diagrams rendered with direct labels and clear cutoff lines.
