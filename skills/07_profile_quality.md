# 07 - Profile Quality

## Purpose

Profile data quality across fact and dimension tables, auditing completeness, uniqueness, value distributions, sign conventions (debit/credit), date ranges, and unexpected zero balances.

## Trigger conditions

- Prior to loading data into analytical models or calculating official reporting metrics.
- Identifying accounting reconciliations errors or data pipeline failures.

## Primary agent

**Data Quality Auditor Agent**

## Inputs

```yaml
profile_quality_request:
  tables: list[string]
  balance_check:
    debit_credit_equality: boolean
  tolerance_threshold: float # e.g. 0.01 NOK
```

## Outputs

```yaml
profile_quality_result:
  quality_score_overall: float # 0.0 - 1.0
  table_assessments:
    - table_name: string
      total_rows: integer
      duplicate_rows: integer
      null_cells_count: integer
      zero_value_transactions: integer
      date_range: { min: string, max: string }
      numeric_ranges: map[column_name, { min: float, max: float, sum: float }]
  reconciliation:
    debit_total: float
    credit_total: float
    imbalance: float
    reconciles: boolean
  critical_issues: list[string]
```

## Responsibilities

1. **Accounting Imbalance Detection:** Verify that total general ledger debits equal total credits or net signed amounts reconcile.
2. **Duplicate Row Detection:** Identify duplicate journal entries or re-imported batch files.
3. **Out-of-Period Postings:** Flag transactions posted outside active fiscal years or closed reporting periods.

## Guardrails

- Any financial data pipeline where debit minus credit != 0 must halt and raise a red audit alert.
- Do not impute or invent financial transaction values.

## Definition of done

- Data quality profile generated with clear pass/fail indicators for completeness, consistency, and financial balance.
