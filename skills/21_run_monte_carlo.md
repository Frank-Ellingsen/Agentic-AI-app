# 21 - Run Monte Carlo

## Purpose

Quantify project cost and schedule uncertainty through stochastic Monte Carlo simulation (1,000 to 10,000 iterations), sampling probability distributions across critical work packages to calculate the cumulative probability of budget overrun.

## Trigger conditions

- Large capital investment or fixed-price engineering/construction contracts.
- Determining required risk contingency buffers at 80% or 90% confidence levels (P80/P90).

## Primary agent

**Quantitative Risk & Simulation Agent**

## Inputs

```yaml
monte_carlo_request:
  iterations: 5000
  random_seed: 42
  uncertain_variables:
    - variable_name: "Engineering_Hours"
      distribution: "triangular" # min, mode, max
      parameters: { min: 10000, mode: 12500, max: 18000 }
    - variable_name: "Steel_Price_Per_Ton"
      distribution: "lognormal"
      parameters: { mean: 15000, std_dev: 2500 }
```

## Outputs

```yaml
monte_carlo_result:
  simulated_outcomes:
    mean_cost: float
    median_cost_p50: float
    p80_cost: float
    p90_cost: float
    standard_deviation: float
  probability_of_budget_overrun: float # e.g. 0.64 (64%)
  contingency_required_for_p80: float
```

## Responsibilities

1. **Probability Sampling:** Draw random samples across assigned parameter distributions using Latin Hypercube or Pseudo-Random sampling.
2. **Percentile Extraction:** Extract P10, P50, P80, and P90 outcomes from the simulated cumulative distribution function.
3. **Contingency Recommendation:** Compute the exact contingency reserve needed to achieve an 80% certainty of finishing within budget.

## Guardrails

- Ensure reproducible execution by logging the random seed.
- Verify that correlated variables (e.g. schedule duration and indirect site supervision costs) include correlation coefficients.

## Definition of done

- S-Curve cumulative distribution generated with calculated P50, P80, and P90 cost thresholds.
