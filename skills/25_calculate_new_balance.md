# 25 - Calculate New Balance

## Purpose

Project the adjusted post-intervention financial and operational balance, calculating the revised Estimate at Completion (EAC), residual gap to budget, and expected new performance trajectory if all approved actions are executed.

## Trigger conditions

- Action portfolio selected (`24_evaluate_optimize_actions.md`).
- Demonstrating before-and-after reconciliation to project leadership or steering committee.

## Primary agent

**Pro-Forma Reconciliation Agent**

## Inputs

```yaml
calculate_new_balance_request:
  pre_intervention_metrics:
    actual_ytd: float
    baseline_forecast_etc: float
    pre_intervention_eac: float
    approved_budget: float
  approved_actions: list[object]
```

## Outputs

```yaml
calculate_new_balance_result:
  post_intervention_metrics:
    new_etc: float
    new_eac: float
    net_improvement: float
    revised_variance_to_budget: float
    reconciliation_status: "budget_restored" | "gap_reduced" | "contingency_required"
  before_after_comparison:
    metric: "Variance to Budget"
    before: float
    after: float
    delta: float
```

## Responsibilities

1. **Before/After Reconciliation:** Calculate the exact bridge from the pre-intervention EAC to the post-intervention revised position.
2. **Residual Gap Analysis:** Identify any remaining budget gap that still requires management contingency or client change orders.
3. **Double-Counting Guard:** Ensure independent actions do not claim savings on the exact same cost transactions.

## Guardrails

- Ensure before and after numbers reconcile mathematically ($EAC_{new} = EAC_{old} - \sum \text{Savings}_{net}$).
- Clearly state the execution risk discount applied to anticipated savings.

## Definition of done

- Reconciled pro-forma balance table showing before-and-after variance to budget and revised EAC.
