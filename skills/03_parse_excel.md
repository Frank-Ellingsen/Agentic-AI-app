# 03 - Parse Excel

## Purpose

Extract, normalize, and validate structured financial tables from Microsoft Excel workbooks (.xlsx, .xlsm, .xls), handling multi-tab workbooks, title blocks, merged headers, formula values, and date serial numbers.

## Trigger conditions

- Budget submissions, project EAC models, or financial controller workbooks submitted in Excel format.
- Tabular financial models with hierarchical or nested headers requiring flattening.

## Primary agent

**Spreadsheet Extraction Agent**

## Inputs

```yaml
excel_parse_request:
  workbook_path: string
  target_sheets: list[string] | "all"
  header_row_offset: integer | "auto"
  data_range: string | null # e.g. "A5:M120"
  evaluate_formulas: boolean # use cached calculated values
  date_system: "1900" | "1904"
```

## Outputs

```yaml
excel_parse_result:
  sheet_catalogs:
    - sheet_name: string
      detected_table_range: string
      row_count: integer
      column_count: integer
      headers: list[string]
      unmerged_cells_count: integer
      formula_cells_count: integer
  normalized_tables: list[object]
```

## Responsibilities

1. **Header Identification:** Detect where metadata/title blocks end and actual column headers begin.
2. **Merged Cell Resolution:** Unmerge merged cells and forward-fill values across spans to maintain complete relational records.
3. **Date Serial Conversion:** Correctly convert Excel numeric date serials (e.g. 45292) into ISO-8601 calendar dates (`YYYY-MM-DD`).
4. **Formula Value Extraction:** Extract the calculated results rather than raw formula strings when extracting analytical facts.

## Guardrails

- Never assume headers are always on Row 1; inspect cell contents to detect tabular headers.
- Flag any `#REF!`, `#VALUE!`, or `#DIV/0!` formula errors immediately.
- Preserve text format for account codes with leading zeros (e.g., `"0100"`).

## Definition of done

- Every targeted sheet is parsed into a clean 2D table with 1 header row and consistent typed rows.
