# 28 - Build Decision Story

## Purpose

Synthesize quantitative diagnostics, prognostic scenarios, and prioritized prescriptions into a compelling, evidence-led executive decision story structured with Bottom-Line Up Front (BLUF), context, root-cause diagnosis, forward outlook, and decision options.

## Trigger conditions

- Validated analytical metrics and recommendations ready for executive delivery.
- Preparing monthly project controller briefings or steering committee decks.

## Primary agent

**Storytelling & Narrative Synthesis Agent**

## Inputs

```yaml
decision_story_request:
  audience: "executive_board" | "project_director" | "controller"
  key_metrics: object # actual, budget, forecast, variance
  prognostic_scenarios: object # baseline, conservative, optimistic
  ranked_prescriptions: list[object]
  governed_rag_status: "RED" | "AMBER" | "GREEN"
  evidence_citations: list[string]
```

## Outputs

```yaml
decision_story_result:
  narrative_structure:
    1_executive_bluf: string # status, key number, core decision required
    2_current_state: string # actual vs budget, trend trajectory
    3_diagnosis: string # largest contributors and root causes
    4_outlook: string # base forecast vs conservative downside risk
    5_recommended_actions: string # prioritized portfolio with quantified outcomes
    6_governance_limitations: string # assumptions, data quality, confidence
  headline: string
  call_to_action: string
```

## Responsibilities

1. **BLUF Framing:** State the primary financial takeaway and required management action in the very first sentence.
2. **Logical Flow:** Maintain a strict logical progression: Observation $\rightarrow$ Diagnosis $\rightarrow$ Prognosis $\rightarrow$ Recommendation $\rightarrow$ Governance.
3. **Clarity & Tone:** Maintain a calm, professional, objective controller tone; eliminate speculative adjectives.

## Guardrails

- Narrative numbers must match underlying tables and charts to the exact currency unit.
- Never invent facts, targets, deadlines, or owners not substantiated in the analytical package.

## Definition of done

- Completed executive decision narrative ready for publication with 100% numerical consistency.
