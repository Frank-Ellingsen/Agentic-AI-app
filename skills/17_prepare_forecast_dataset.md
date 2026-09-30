# 17 - Prepare Forecast Dataset

## Purpose

Construct high-integrity time-series feature datasets for forecasting, engineering lag variables, rolling window statistics, calendar indicators, seasonality indices, and committed backlog spend.

## Trigger conditions

- Prior to training or executing time-series forecasting models (`18_select_and_backtest_model.md`).
- Building quarterly/annual rolling forecast projections.

## Primary agent

**Feature Engineering & Forecasting Data Agent**

## Inputs

```yaml
prepare_forecast_data_request:
  history_table: "FactGL"
  target_column: "Belop_signert"
  date_column: "Dato"
  aggregation_grain: "monthly"
  feature_requirements:
    lags: [1, 2, 3, 12]
    rolling_means: [3, 6]
    include_fte_feature: boolean
    include_inflation_index: boolean
```

## Outputs

```yaml
prepare_forecast_data_result:
  dataset_name: string
  row_count: integer
  feature_columns: list[string]
  train_split_periods: list[string]
  test_split_periods: list[string]
  stationarity_test:
    is_stationary: boolean
    differencing_order_d: integer
```

## Responsibilities

1. **Calendar Alignment:** Fill gaps in historical time-series with explicit zero postings where appropriate.
2. **Lag & Rolling Features:** Create lag features ($t-1, t-2, t-12$) and rolling averages to capture momentum and seasonality.
3. **Train/Validation Partition:** Split data cleanly on time boundaries without future information leakage.

## Guardrails

- Never randomize or shuffle time-series data; chronological order must remain strictly intact.
- Guard against survivorship bias by retaining closed accounts and discontinued projects.

## Definition of done

- Clean, rectangular feature matrix formatted for forecasting models with zero lookahead bias.
