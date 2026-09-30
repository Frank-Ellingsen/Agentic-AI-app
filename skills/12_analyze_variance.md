# 12 - Analyze Variance

## Purpose

Decompose and explain variances between Actual results and Budget/Forecast baselines into explanatory business components: Rate (price/labor rate), Volume (hours/units), and Mix (staffing seniority or project phase composition).

## Trigger conditions

- Material cost or revenue variances identified exceeding governed thresholds (e.g. >5% or >100,000 NOK).
- Monthly project review variance bridge preparation.

## Primary agent

**Variance Analyst Agent**

## Inputs

```yaml
variance_analysis_request:
  reporting_period: string
  baseline: "budget" | "prior_forecast" | "prior_year"
  comparison_target: "actual"
  dimensions_for_breakdown: [Account, CostCenter, Project, Vendor]
  materiality_threshold: 50000.0 # NOK
```

## Outputs

```yaml
variance_analysis_result:
  total_variance: float
  variance_breakdown:
    - dimension_value: string
      actual: float
      baseline: float
      variance: float
      variance_pct: float
      rate_variance: float | null
      volume_variance: float | null
      explanation: string
  waterfall_bridge_steps:
    - step_name: string
      amount: float
      cumulative: float
```

## Responsibilities

1. **Waterfall Bridge Construction:** Build the step-by-step bridge starting at Budget and concluding at Actual.
2. **Rate/Volume Decomposition:** Separate hourly labor rate increases from excess hours billed.
3. **Materiality Filtering:** Focus executive attention on the top 20% of variances causing 80% of the financial gap (Pareto principle).

## Guardrails

- Ensure the sum of individual variance components equals the total overall variance to the exact cent.
- Do not attribute causation without supporting transactional evidence.

## Definition of done

- Completed variance breakdown and waterfall bridge reconciling baseline to actual.
