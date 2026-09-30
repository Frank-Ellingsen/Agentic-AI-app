# Skill 01: Descriptive EDA & Visuals (ai-skill-eda-visuals)

## Purpose
Perform exploratory data analysis (EDA), data quality profiling, KPI diagnostics, variance attribution, and Tufte-compliant visual selection on any structured or tabular dataset.

## Trigger Conditions
- User provides raw tabular data (CSV, Excel, Database, Parquet) requiring initial inspection.
- Request asks to identify "what happened," profile data quality, compute core KPIs, analyze trends, or detect anomalies.
- Need to generate descriptive visuals and diagnostic dashboards without hallucinated numbers.

## Primary Agent
**Data Intake & Diagnostic Agent (A1 / A3)**

## Inputs Schema (YAML)
```yaml
eda_request:
  dataset_ref: string          # Path or table reference in DuckDB/Pandas
  target_metrics: list[string] # Metrics to compute (e.g., revenue, cost_variance, volume)
  group_dimensions: list[string] # Dimensions for segmentation (e.g., region, supplier, category)
  time_dimension: string       # Period/Date column
  baseline_type: budget | prior_period | target
  visual_constraints:
    tufte_compliant: true
    direct_labeling: true
    max_charts: 6
```

## Workflow Execution Steps
1. **Source Inspection & Profiling:**
   - Detect data types, null counts, duplicate records, outliers, and sign conventions.
   - Standardize units, currency, and date formats across dimension and fact tables.
2. **Diagnostic Calculation (Deterministic Engine):**
   - Execute SQL/Python aggregations for baseline vs. actuals (e.g., Variance = Actual - Target, Variance % = (Actual - Target) / Target).
   - Rank top 3–5 contributing drivers explaining the total variance.
   - Detect statistical anomalies (> 3 sigma or Isolation Forest flags).
3. **Visual Selection & Rendering:**
   - Apply Data-Ink Ratio rules: remove chartjunk, vertical gridlines, drop shadows, and decorative colors.
   - Select chart types based on analytical intent:
     - Actual vs. Target -> Bullet chart / Dot plot / Bar
     - Time Series Trend -> Direct-labeled line chart
     - Variance Drivers -> Waterfall chart or sorted horizontal contribution bar
     - Exceptions -> Highlight table with muted slate palette and selective status highlights.

## Outputs Schema (YAML)
```yaml
eda_result:
  quality_profile:
    completeness_score: float
    detected_issues: list[string]
  summary_kpis:
    - metric_name: string
      actual: float
      baseline: float
      variance: float
      variance_pct: float
      status_rag: GREEN | AMBER | RED
  top_drivers:
    - dimension: string
      driver_key: string
      contributed_variance: float
      pct_explained: float
  visuals_manifest:
    - chart_id: string
      chart_type: waterfall | line | bullet | bar
      title: string
      data_ref: string
      takeaway_annotation: string
```

## Guardrails
- **No LLM Math:** All KPI and variance figures must originate from DuckDB/Python execution engines.
- **Data-Ink Ratio:** Enforce Tufte principles; avoid 3D charts, pie charts with > 5 slices, and dual axes unless explicitly justified.
- **Causal Distinction:** Label driver rankings as statistical contributions, not unproven causal mechanisms.

## Definition of Done
- Complete data quality score computed.
- Reconciled KPI summary and variance driver matrix produced.
- Clean, direct-labeled visual assets generated and stored as artifacts.
