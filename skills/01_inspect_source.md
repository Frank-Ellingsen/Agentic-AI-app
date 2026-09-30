# 01 - Inspect Source

## Purpose

Assess raw input sources (ERP general ledger dumps, budget workbooks, forecast submissions, project registers, and timesheet exports) to verify file existence, format encoding, delimiter conventions, freshness, row counts, and data footprint integrity before ingestion.

## Trigger conditions

- New raw files uploaded or deposited in the ingestion landing zone.
- Periodic batch runs ingesting financial and operational accounting files.
- Discrepancy flagged between expected source catalog and landing directory.

## Primary agent

**Ingestion & Source Inspector Agent**

## Inputs

```yaml
source_inspection_request:
  data_directory: string
  expected_files:
    - filename: string
      required: boolean
      category: dimension | fact | metadata
  encoding_candidates: [utf-8, utf-8-sig, latin-1, cp1252]
  delimiter_candidates: [";", ",", "\t", "|"]
```

## Outputs

```yaml
source_inspection_result:
  inspection_timestamp: ISO-8601 string
  file_catalog:
    - filename: string
      size_bytes: integer
      detected_encoding: string
      detected_delimiter: string
      estimated_rows: integer
      status: valid | empty | missing | unreadable
  footprint_summary:
    total_files: integer
    total_bytes: integer
    missing_required_files: list[string]
  validation_status: pass | fail
```

## Responsibilities

1. **Footprint & File Verification:** Check that all mandatory business tables (e.g. `FactGL.csv`, `FactBudget.csv`, `FactForecast.csv`, `DimDate.csv`) exist in the target directory.
2. **Encoding & BOM Detection:** Identify UTF-8, UTF-8-BOM (`utf-8-sig`), or Western European legacy encodings (`cp1252`/`latin-1`) common in Scandinavian ERP exports.
3. **Delimiter Discovery:** Detect whether semicolon (`;`) or comma (`,`) is the primary separator using frequency sampling across the first 4 KB.
4. **Freshness & Stale Data Guard:** Record file modification timestamps to prevent processing stale accounting snapshots.

## Guardrails

- Never proceed to parsing if mandatory fact tables are zero bytes or missing.
- Do not alter or write to raw source files; maintain an immutable audit trail.
- Flag any files with non-standard byte order marks or mixed delimiters immediately.

## Definition of done

- Every file in the landing zone has a verified delimiter, encoding, and row count estimate.
- A structured `source_inspection_result` artifact is produced for downstream parser agents.
