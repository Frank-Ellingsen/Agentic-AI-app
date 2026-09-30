# 02 - Parse Tabular

## Purpose

Parse raw delimited text files (CSV, TSV, DSV) into structured tabular data structures while preserving character fidelity, quote escaping, European number formats, and column definitions.

## Trigger conditions

- Completed source inspection (`01_inspect_source.md`) passes validation.
- Tabular text datasets need to be loaded into memory, DuckDB, or downstream staging frames.

## Primary agent

**Tabular Parser Agent**

## Inputs

```yaml
tabular_parse_request:
  file_path: string
  delimiter: string
  encoding: string
  has_header: boolean
  quote_char: '"'
  escape_char: null | "\\"
  decimal_separator: "," | "."
  thousand_separator: "." | " " | ""
```

## Outputs

```yaml
tabular_parse_result:
  table_name: string
  row_count: integer
  column_count: integer
  headers: list[string]
  sample_rows: list[list[string]]
  malformed_rows_count: integer
  parsing_warnings: list[string]
```

## Responsibilities

1. **Dialect-Aware Parsing:** Handle embedded newlines inside quoted fields, double-quote escapes (`""`), and varying line terminations (`\r\n` vs `\n`).
2. **European Numeric Handling:** Correctly parse Scandinavian/European currency and quantity amounts (e.g. `1.250.000,50` or space-separated `1 250 000,50`).
3. **Ragged Row Recovery:** Detect and log rows that have more or fewer columns than the header line without failing the entire batch silently.
4. **Header Normalization:** Strip extraneous whitespace, remove non-printable characters, and detect duplicate header names.

## Guardrails

- Never truncate long numeric strings (such as GL account numbers or cost center codes) to floating point numbers.
- Retain exact row-level counts to ensure the general ledger debit/credit balances can be audited.
- Report any row where the parsed field count does not match the header field count.

## Definition of done

- The dataset is parsed into a verified rectangular tabular structure.
- Malformed row count is zero or fully documented in the parse report.
