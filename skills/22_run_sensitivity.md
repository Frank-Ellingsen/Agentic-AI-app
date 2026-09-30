# 22 - Run Sensitivity

## Purpose

Perform deterministic One-at-a-Time (OAT) parameter stress testing, calculating elasticities and generating Tornado sensitivity diagrams to rank which individual risk variables exert the greatest leverage on total project outcome.

## Trigger conditions

- Evaluating project risk sensitivity prior to contract signing or major milestone reviews.
- Identifying high-leverage risk drivers to target for mitigation actions.

## Primary agent

**Sensitivity Analysis Agent**

## Inputs

```yaml
sensitivity_analysis_request:
  target_metric: "EAC"
  base_parameters: map[variable_name, base_value]
  variation_range_pct: 0.15 # +/- 15% swing on each parameter
  variables_to_test:
    - Labor_Hourly_Rate
    - Subcontractor_Productivity
    - FX_EUR_NOK
    - Material_Scrap_Rate
```

## Outputs

```yaml
sensitivity_analysis_result:
  tornado_rankings:
    - rank: integer
      variable: string
      low_outcome: float # outcome at -15%
      high_outcome: float # outcome at +15%
      swing_range: float # abs(high - low)
      elasticity: float # % change in EAC / % change in variable
  most_sensitive_variable: string
```

## Responsibilities

1. **Parameter Perturbation:** Swing each key parameter by +/- 10% to 20% while holding all other variables constant.
2. **Tornado Bridge Construction:** Sort variables by total swing range in descending order.
3. **Elasticity Calculation:** Quantify sensitivity coefficients ($E = \frac{\Delta \text{EAC} / \text{EAC}}{\Delta X / X}$).

## Guardrails

- Ensure identical percentage perturbation across all tested parameters to maintain valid comparative ranking.
- Distinguish linear sensitivities from non-linear threshold effects.

## Definition of done

- Ranked tornado sensitivity table with calculated swing ranges and elasticity metrics.
