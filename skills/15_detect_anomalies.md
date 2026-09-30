# 15 - Detect Anomalies

## Purpose

Detect statistically unusual postings, spikes, missing recurring accruals, duplicate invoice payments, and out-of-pattern general ledger transactions using statistical outlier detection (Z-scores, IQR fences, isolation trees).

## Trigger conditions

- Periodic audit of accounting transactions before ledger close.
- Unexplained sudden jumps in cost run-rates or abnormal zero balances.

## Primary agent

**Anomaly & Fraud Detection Agent**

## Inputs

```yaml
anomaly_detection_request:
  target_table: "FactGL"
  value_column: "Belop_signert"
  group_by_dimensions: [Account, CostCenter]
  methods: ["z_score", "iqr_fence", "recurring_accrual_gap"]
  sensitivity: "standard" # threshold z > 3.0 or IQR > 2.5
```

## Outputs

```yaml
anomaly_detection_result:
  flagged_anomalies:
    - transaction_id: string
      date: string
      account: string
      amount: float
      expected_range: { min: float, max: float }
      score: float
      reason: "large_spike" | "missing_accrual" | "duplicate_amount" | "weekend_posting"
  anomaly_count: integer
  total_at_risk_amount: float
```

## Responsibilities

1. **Statistical Outlier Detection:** Flag transactions exceeding 3 standard deviations ($Z > 3$) from historical account means.
2. **Missing Accruals:** Detect expected monthly cost items (e.g. software licenses, rent, utilities) missing in the current period.
3. **Duplicate Transactions:** Flag identical amounts posted to the same account and vendor within close calendar windows.

## Guardrails

- Differentiate legitimate seasonal capital expenditures from operational expense anomalies.
- Never delete or alter flagged transactions; report them for human controller review.

## Definition of done

- Ranked list of anomalous transactions with confidence scores and specific audit rationales.
