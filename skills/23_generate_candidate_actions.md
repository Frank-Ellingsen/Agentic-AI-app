# 23 - Generate Candidate Actions

## Purpose

Formulate concrete, actionable managerial interventions and mitigation options (e.g. tightening discretionary travel, vendor volume renegotiations, scope descoping, overtime caps, or billing milestones acceleration) directly targeted at the identified variance drivers.

## Trigger conditions

- Negative variance to budget or projected EAC overrun detected (`12_analyze_variance.md`, `19_generate_forecast.md`).
- Request for prescriptive interventions to close an emerging financial gap.

## Primary agent

**Prescriptive Action Formulator Agent**

## Inputs

```yaml
candidate_actions_request:
  financial_gap_to_close: float # amount needed to recover budget
  identified_drivers: list[object]
  operational_constraints:
    cannot_reduce_safety_budget: boolean
    max_headcount_reduction_pct: float
    contractual_delivery_deadline: string
```

## Outputs

```yaml
candidate_actions_result:
  action_pool:
    - action_id: string
      title: string
      description: string
      category: "cost_reduction" | "revenue_acceleration" | "risk_mitigation"
      targeted_driver: string
      estimated_recovery_amount: float
      time_to_implement_weeks: integer
      feasibility: "high" | "medium" | "low"
      implementation_cost: float
```

## Responsibilities

1. **Driver Targeting:** Propose specific actions mapped to the largest root causes found in Skill 14.
2. **Quantification:** Provide an initial estimate of both recovery potential and required implementation cost.
3. **Operational Grounding:** State who would execute the action and within what time horizon.

## Guardrails

- Never propose vague advice like "improve efficiency"; formulate concrete, measurable interventions (e.g. "Cap external contractor hours at 37.5 hours/week").
- Do not violate specified hard constraints (e.g. safety or contractual delivery dates).

## Definition of done

- Action catalog produced containing at least 3 distinct, quantified candidate options.
