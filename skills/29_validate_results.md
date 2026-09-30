# 29 - Validate Results

## Purpose

Perform independent, automated cross-validation and mathematical audit on the complete analytical reporting package before publication, blocking reports that have reconcile errors, RAG mismatches, missing horizons, or unsubstantiated claims.

## Trigger conditions

- Final step before HTML rendering, distribution, or publishing.
- Mandatory gatekeeper audit in the multi-agent workflow.

## Primary agent

**Independent Validator & Gatekeeper Agent**

## Inputs

```yaml
validation_request:
  full_reporting_package:
    metrics: object
    narrative: object
    tables: list[object]
    visuals: list[object]
    governed_rag: string
    prescriptions: list[object]
```

## Outputs

```yaml
validation_result:
  validation_status: "PASS" | "FAIL"
  check_results:
    numerical_reconciliation: pass | fail
    rag_governance_match: pass | fail
    evidence_coverage: pass | fail
    tufte_design_compliance: pass | fail
    accessibility_check: pass | fail
  blocking_errors: list[string]
  warnings: list[string]
```

## Responsibilities

1. **Cross-Check Narrative vs Tables:** Verify that every numerical figure quoted in the text corresponds identically to the figures in the tables.
2. **Status RAG Integrity:** Ensure that the RAG status color and label match the deterministic governance output from Skill 16.
3. **Prescriptive Reconciliation:** Verify that before-and-after calculations reconcile mathematically without double counting.

## Guardrails

- The Validator Agent holds absolute veto authority; any blocking error halts the pipeline immediately.
- Never allow automated "soft pass" on mathematical discrepancies.

## Definition of done

- Formal validation report issued with status `PASS` and zero blocking errors.
