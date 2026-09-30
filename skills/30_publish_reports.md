# 30 - Publish Reports

## Purpose

Render and distribute validated analytical outputs into responsive, semantic, accessible HTML reports and executive insight packages, complete with print stylesheets, interactive drilldowns, and audit registers.

## Trigger conditions

- Validator Agent issues `PASS` status (`29_validate_results.md`).
- Scheduled distribution to executive steering committee, project directors, or finance leadership.

## Primary agent

**Report Publisher & Delivery Agent**

## Inputs

```yaml
publish_report_request:
  validated_package: object
  output_formats: ["html", "markdown", "json"]
  distribution_channels: ["web_studio", "file_export"]
  report_metadata:
    title: string
    reporting_period: string
    audience: string
    author: string
```

## Outputs

```yaml
publish_report_result:
  publication_timestamp: ISO-8601
  artifacts_generated:
    - format: "html"
      path: string
      url: string | null
    - format: "markdown"
      path: string
  distribution_status: "published"
  audit_checksum_sha256: string
```

## Responsibilities

1. **Semantic HTML Composition:** Structure the document with appropriate header tags (`h1`, `h2`, `h3`), semantic `<main>`, `<section>`, and `<aside>` elements.
2. **Print-Friendly Styling:** Include `@media print` rules removing interactive controls and optimizing page breaks.
3. **Accessibility:** Comply with WCAG 2.1 AA standards: high contrast ratios, screen-reader table headers, and keyboard navigation.

## Guardrails

- Never publish an unvalidated or draft report as an official release.
- Retain an immutable snapshot of published reports with cryptographic checksums.

## Definition of done

- Clean, responsive HTML report published and accessible via the analytics studio.
