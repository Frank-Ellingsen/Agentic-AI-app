# 24 - Evaluate and Optimize Actions

## Purpose

Score, filter, and optimize candidate actions using multi-criteria decision analysis (Impact, Feasibility, Cost, Risk, Time-to-Benefit), selecting the optimal portfolio of actions that closes the financial gap while minimizing operational friction.

## Trigger conditions

- Action pool generated (`23_generate_candidate_actions.md`).
- Multi-intervention trade-off analysis required for management sign-off.

## Primary agent

**Optimization & Decision Scoring Agent**

## Inputs

```yaml
evaluate_actions_request:
  candidate_actions: list[object]
  gap_target: float # e.g. 500000.0 NOK
  budget_cap_for_implementation: float
  scoring_weights:
    net_financial_impact: 0.40
    feasibility_speed: 0.30
    low_execution_risk: 0.30
```

## Outputs

```yaml
evaluate_actions_result:
  scored_actions:
    - action_id: string
      title: string
      impact_score: float # 0.0 - 1.0 composite
      expected_result: string
      net_benefit: float
      rank: integer
      status: "recommended" | "reserve" | "rejected"
  portfolio_summary:
    total_net_recovery: float
    total_implementation_cost: float
    gap_closure_percentage: float
```

## Responsibilities

1. **Composite Scoring:** Calculate normalized utility scores weighting net financial return, implementation speed, and risk.
2. **Knapsack / Portfolio Optimization:** Select the highest-impact combination of actions subject to implementation budget and time constraints.
3. **Executive Ranking:** Rank recommendations clearly so leadership can approve the package in tiers.

## Guardrails

- Show both expected benefit and required cost/risk for every single recommendation.
- Explicitly reject actions where implementation cost exceeds expected recovery.

## Definition of done

- Ranked portfolio of optimized actions with composite impact scores and quantified recovery totals.
