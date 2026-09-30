# Skill 03: Recommended Actions & Impact Visuals (ai-skill-recommended-actions)

## Purpose
Formulate concrete, quantified managerial interventions, evaluate operational constraints, run multi-criteria portfolio optimization, compute risk-adjusted net benefits, calculate post-intervention pro-forma balances, and render before-and-after impact visuals.

## Trigger Conditions
- Prognostic or diagnostic analysis identifies an emerging financial gap, schedule delay, or performance overrun.
- User requests actionable prescriptive recommendations, cost-benefit trade-offs, or optimization of mitigation measures.
- Need to display before-and-after reconciliation, waterfall impact charts, or action ranking matrices.

## Primary Agent
**Prescriptive Agent (A5)**

## Inputs Schema (YAML)
```yaml
prescriptive_request:
  gap_to_close: float              # Required recovery amount (e.g., gap to budget)
  identified_drivers: list[object] # Key root cause drivers from diagnostic stage
  implementation_budget_cap: float # Max budget allowed for interventions
  operational_constraints:
    max_headcount_reduction_pct: float
    contractual_deadlines_hard: boolean
    safety_budget_protected: boolean
  optimization_weights:
    net_financial_recovery: 0.40
    implementation_speed: 0.30
    low_execution_risk: 0.30
```

## Workflow Execution Steps
1. **Action Formulation:**
   - Propose specific, concrete operational levers (e.g., "Cap external contractor hours at 37.5 hrs/week", "Renegotiate raw material supplier package B").
   - Reject vague advice such as "improve efficiency" or "reduce costs".
2. **Quantification & Portfolio Optimization:**
   - Estimate recovery potential, implementation cost, execution time (weeks), and feasibility score for each action.
   - Run knapsack / multi-criteria decision analysis (MCDA) to select the optimal portfolio closing the gap while staying under budget caps.
   - Calculate risk-adjusted net savings = (Expected Savings * Success Probability) - Implementation Cost.
3. **Pro-Forma Balance Calculation:**
   - Calculate revised end-of-period position:
     `Post-Intervention EAC = Pre-Intervention Forecast EAC - Risk-Adjusted Net Recovery`.
   - Calculate residual budget gap or surplus remaining after approved actions.
4. **Impact Visual Rendering:**
   - Generate Before-and-After Waterfall charts showing starting forecast, individual action recovery steps, and final post-intervention EAC.
   - Render Action Impact vs. Feasibility matrix / ranked portfolio table.

## Outputs Schema (YAML)
```yaml
prescriptive_result:
  action_portfolio:
    - action_id: string
      title: string
      targeted_driver: string
      estimated_recovery: float
      implementation_cost: float
      time_to_benefit_weeks: integer
      success_probability: float
      risk_adjusted_net_benefit: float
      status: recommended | reserve | rejected
  portfolio_summary:
    total_implementation_cost: float
    total_gross_recovery: float
    total_net_recovery: float
    gap_closure_pct: float
  pro_forma_reconciliation:
    pre_intervention_eac: float
    total_net_recovery: float
    post_intervention_eac: float
    approved_budget: float
    residual_variance: float
  visuals_manifest:
    - chart_id: string
      chart_type: waterfall_bridge | impact_effort_matrix | clean_action_table
      file_path: string
      key_takeaway: string
```

## Guardrails
- **Quantitative Requirement:** Every recommendation must state expected financial saving, cost to implement, and success probability.
- **Positive Net Benefit:** Automatically reject any action where implementation cost exceeds expected recovery.
- **Reconciliation Integrity:** Ensure post-intervention EAC mathematically matches the pre-intervention forecast minus net savings.

## Definition of Done
- Quantified catalog of at least 3 concrete, non-vague candidate actions produced.
- Multi-criteria optimization score and portfolio summary computed.
- Pro-forma before-and-after balance sheet generated alongside Waterfall impact visuals.
