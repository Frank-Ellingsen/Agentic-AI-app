# 04 - Extract Document

## Purpose

Extract unstructured context, management commentaries, board resolutions, contract terms, milestone dates, and audit notes from business documents (PDFs, Word documents, text notes) to enrich quantitative datasets with qualitative evidence.

## Trigger conditions

- Monthly project status reports with narrative progress notes.
- Vendor contracts or change orders containing milestone schedules, liquidated damages, or billing terms.
- Auditor notes explaining year-end accounting adjustments.

## Primary agent

**Document Understanding Agent**

## Inputs

```yaml
document_extract_request:
  document_path: string
  document_type: pdf | docx | txt | markdown
  target_entities:
    - entity_type: milestone | contract_value | risk_note | variation_order
      expected_keys: list[string]
  reporting_period: string
```

## Outputs

```yaml
document_extract_result:
  document_metadata:
    title: string
    author: string
    date_published: string
    page_count: integer
  extracted_entities:
    - type: string
      key: string
      value: string | number
      confidence: float
      source_reference:
        page_number: integer
        section_heading: string
        verbatim_excerpt: string
  validation_status: pass | review_required
```

## Responsibilities

1. **Entity Extraction:** Pull explicit monetary values, project codes, revision dates, and cost variance explanations.
2. **Context Linking:** Map qualitative explanations to specific cost centers, projects, or GL accounts.
3. **Traceability:** Maintain verbatim text quotations and page numbers for audit trails.

## Guardrails

- Never fabricate values not present in the document.
- If a qualitative statement is ambiguous or contradicts the general ledger, flag it as an unresolved variance.

## Definition of done

- All target qualitative entities are extracted with verbatim references and confidence scores.
