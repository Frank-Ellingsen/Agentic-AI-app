# 16 - Apply Status RAG

## Purpose

Apply deterministic, governed Red-Amber-Green (RAG) status classifications to business outcomes, projects, and cost centers based on pre-defined objective thresholds, completely preventing LLM hallucination or arbitrary status assignment.

## Trigger conditions

- Metrics and variances calculated (`11_calculate_kpis.md`, `12_analyze_variance.md`).
- Executive dashboard scorecards or traffic-light reporting required.

## Primary agent

**Governance & Status RAG Agent**

## Inputs

```yaml
rag_governance_request:
  entities:
    - entity_id: string
      name: string
      variance_to_budget: float
      variance_pct_budget: float
      eac_vs_budget_pct: float
      schedule_variance_days: integer
  threshold_rules:
    green:
      cost_variance_pct: ">= -2.0%" # within 2% of budget
      schedule_delay_days: "<= 5"
    amber:
      cost_variance_pct: "between -2.0% and -7.5%"
      schedule_delay_days: "between 6 and 20"
    red:
      cost_variance_pct: "< -7.5%" # overrun > 7.5%
      schedule_delay_days: "> 20"
```

## Outputs

```yaml
rag_governance_result:
  entity_statuses:
    - entity_id: string
      status: "RED" | "AMBER" | "GREEN"
      primary_trigger_rule: string
      metric_values: object
      accessible_symbol: "▲ (Green)" | "◆ (Amber)" | "▼ (Red)"
  portfolio_distribution:
    green_count: integer
    amber_count: integer
    red_count: integer
```

## Responsibilities

1. **Deterministic Rule Enforcement:** Apply mathematical comparison logic without heuristic drift.
2. **Accessible Presentation:** Couple color with explicit text labels (`RED`, `AMBER`, `GREEN`) and directional symbols.
3. **Trigger Traceability:** Explicitly document the single metric that triggered an Amber or Red status (e.g. "Triggered RED by EAC overrun of 8.2%").

## Guardrails

- Never permit an LLM prompt to override governed RAG status logic.
- Highlight active risks with color while keeping all normal rows in muted slate tones (Tufte principle).

## Definition of done

- Every entity is assigned an unambiguous RAG status grounded in explicit policy thresholds.
