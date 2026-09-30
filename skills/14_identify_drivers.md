# 14 - Identify Drivers

## Purpose

Isolate and rank the underlying operational and commercial root causes driving financial variance, identifying which specific projects, suppliers, work packages, or cost accounts exert the greatest leverage on performance.

## Trigger conditions

- Material variance identified in `12_analyze_variance.md`.
- Management requests actionable root-cause attribution rather than top-level aggregation.

## Primary agent

**Root Cause & Driver Attribution Agent**

## Inputs

```yaml
driver_identification_request:
  target_metric: "variance_to_budget"
  candidate_dimensions: [Project, Organization, AccountGroup, Vendor]
  max_drivers_to_report: 5
  min_explanatory_power: 0.70 # 70% of total variance
```

## Outputs

```yaml
driver_identification_result:
  primary_drivers:
    - rank: integer
      dimension: string
      dimension_key: string
      dimension_label: string
      contributed_variance: float
      percentage_of_total_variance: float
      underlying_mechanism: string
  cumulative_explained_variance_pct: float
```

## Responsibilities

1. **Contribution Ranking:** Rank entities by their absolute contribution to total favorable or unfavorable variance.
2. **Dimension Cross-Tabulation:** Identify intersections (e.g. Project X + Subcontractor Y) that account for the bulk of budget leakage.
3. **Driver Isolation:** Separate external market cost factors (raw material inflation, energy prices) from internal execution factors (overtime hours, rework).

## Guardrails

- Focus on controllable operational levers where management intervention is viable.
- Ensure the top drivers explain at least 70% of the total variance before stopping.

## Definition of done

- Ranked list of top 3 to 5 actionable drivers with quantified contribution to total variance.
