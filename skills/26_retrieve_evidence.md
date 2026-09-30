# 26 - Retrieve Evidence

## Purpose

Gather, cross-reference, and index verifiable transaction-level evidence, audit vouchers, purchase orders, time-card approvals, and contract clauses supporting analytical claims and proposed interventions.

## Trigger conditions

- Preparing audit-ready backing material for executive decision stories.
- Resolving disputed variances or preparing documentation for client claims.

## Primary agent

**Evidence & Lineage Retrieval Agent**

## Inputs

```yaml
retrieve_evidence_request:
  target_findings:
    - finding_id: string
      statement: string # e.g. "Overtime cost surged by 340,000 NOK in Fabrication"
      associated_tables: [FactGL, FactFTE, DimOrganization]
  required_evidence_level: "transaction_level" | "documentary" | "aggregated"
```

## Outputs

```yaml
retrieve_evidence_result:
  evidence_register:
    - finding_id: string
      supporting_records:
        - voucher_id: string
          posting_date: string
          account: string
          amount: float
          reference_text: string
          source_file: string
      documentary_citations: list[string]
      traceability_confidence: float # 0.0 - 1.0
  unsupported_statements: list[string]
```

## Responsibilities

1. **Transaction Drilldown:** Query the underlying general ledger or timesheet records that substantiate the aggregated totals.
2. **Citation Register:** Build a formal register linking every claim in the analytical summary to explicit source row numbers or voucher IDs.
3. **Audit Trail Assembly:** Compile provenance metadata confirming that evidence was not altered in transit.

## Guardrails

- Never state a financial claim as fact if underlying transactional evidence is missing.
- Treat retrieved commentary as corroborated evidence only when verified against the general ledger.

## Definition of done

- Completed evidence register providing 100% citation coverage for key analytical assertions.
