# 08 - Normalize Data

## Purpose

Standardize field values, accounting sign conventions, date representations, currency denominations (NOK, EUR, USD), and organization hierarchy keys across fragmented datasets into a uniform canonical format.

## Trigger conditions

- Data parsed from varied accounting systems or international joint-venture partners with divergent chart of accounts or conventions.
- Unnormalized naming strings (e.g. `Dept. 10`, `Department 10`, `Avd 10`).

## Primary agent

**Data Normalization Agent**

## Inputs

```yaml
normalization_request:
  tables: list[string]
  target_currency: "NOK"
  fx_rate_table: string | null
  date_format: "YYYY-MM-DD"
  sign_convention: "signed_net" # Revenues negative / expenses positive, or explicit type
  text_case: "title" | "upper" | "preserve"
```

## Outputs

```yaml
normalization_result:
  normalized_tables: list[string]
  conversions_applied:
    currency_conversions: integer
    date_standardizations: integer
    text_casing_changes: integer
    sign_inversions: integer
  audit_log_path: string
```

## Responsibilities

1. **Sign Convention Standardization:** Ensure expenses and revenues follow consistent signs across Actuals, Budget, and Forecast.
2. **Calendar Standardization:** Convert all date formats (`DD.MM.YYYY`, `MM/DD/YYYY`, timestamps) into standard ISO-8601 (`YYYY-MM-DD`).
3. **Key Cleaning:** Trim whitespace, strip special characters, and standardize uppercase for ID columns (`KontoNr`, `ProsjektNr`).

## Guardrails

- Currency conversions must use dated exchange rates matching the transaction date.
- Never alter the original raw tables; write normalized outputs to a clean staging layer.

## Definition of done

- All tables follow unified sign, currency, date, and naming conventions.
