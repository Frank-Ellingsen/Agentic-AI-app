# 05 - Infer Schema

## Purpose

Examine columns and sample rows across parsed tables to infer strict physical datatypes, nullability, primary key candidates, categorical domains, and dimensional grain.

## Trigger conditions

- New parsed tabular dataset ready for database ingestion or relational modeling.
- Schema drift check during regular ELT pipeline runs.

## Primary agent

**Schema Inference Agent**

## Inputs

```yaml
schema_infer_request:
  tables: list[string]
  sample_size_rows: integer # e.g. 5000 or full scan
  type_preference:
    dates: "ISO-8601"
    numerics: "decimal_exact"
```

## Outputs

```yaml
schema_infer_result:
  tables:
    - table_name: string
      row_count: integer
      columns:
        - name: string
          inferred_type: string | integer | float | boolean | date | timestamp
          null_count: integer
          null_percentage: float
          unique_count: integer
          is_unique: boolean
          primary_key_candidate: boolean
          sample_values: list[string]
```

## Responsibilities

1. **Type Resolution:** Discriminate integers, floating point currency amounts, booleans (`true/false`, `ja/nei`), and calendar dates (`YYYY-MM-DD`, `DD.MM.YYYY`).
2. **Key Detection:** Identify candidate primary keys (columns with 100% unique values and 0% nulls).
3. **Grain Definition:** Document the atomic level of each table (e.g. transaction-level GL vs monthly summarized budget).

## Guardrails

- Never infer float for exact integer identifiers (like `KontoNr` or `ProsjektNr`).
- Retain leading zeros in codes by keeping them as string.

## Definition of done

- Every table has a complete column-by-column schema definition with inferred types, nullability, and primary key indicators.
