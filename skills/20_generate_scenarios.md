# 20 - Generate Scenarios

## Purpose

Construct coherent macroeconomic and operational scenarios (Baseline, Conservative, Optimistic, and Stress Case) reflecting varying assumptions on labor productivity, material inflation, project delay penalties, and revenue conversion rates.

## Trigger conditions

- Forecast generation completed (`19_generate_forecast.md`).
- Strategic planning, project board reviews, or contingency reserve sizing.

## Primary agent

**Scenario Architect Agent**

## Inputs

```yaml
generate_scenarios_request:
  baseline_forecast: map[period, amount]
  scenarios_to_build:
    - name: "baseline"
      description: "Most probable path under current operating conditions"
    - name: "conservative"
      description: "Adverse conditions: higher subcontractor rates and 10% delivery delay"
    - name: "optimistic"
      description: "Accelerated execution and favorable supply chain terms"
    - name: "stress_test"
      description: "Severe shock: 20% cost surge on critical path items"
```

## Outputs

```yaml
generate_scenarios_result:
  scenarios:
    baseline:
      actual_total: float
      expected_total: float
      variance_vs_budget: float
      eac: float
    conservative:
      actual_total: float
      expected_total: float
      variance_vs_budget: float
      eac: float
    optimistic:
      actual_total: float
      expected_total: float
      variance_vs_budget: float
      eac: float
  spread_range:
    max_eac: float
    min_eac: float
    delta_spread: float
```

## Responsibilities

1. **Parameter Bundling:** Link related assumptions coherently (e.g. higher volume should correlate with higher direct material costs).
2. **Variance Impact Modeling:** Quantify the financial delta of each scenario against the baseline and original budget.
3. **Contingency Testing:** Determine whether current management contingency reserves can absorb the conservative scenario.

## Guardrails

- Avoid extreme unrealistic scenarios that distract from actionable decision making.
- Explicitly list the key drivers differentiating each scenario.

## Definition of done

- Mutually distinct, structured scenarios with calculated EAC and variance outcomes.
