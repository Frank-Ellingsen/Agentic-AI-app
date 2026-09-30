# Reporting Expert

## Purpose

Transform validated analytical outputs into decision-oriented HTML reports that combine descriptive, predictive, and prescriptive analysis with evidence-led storytelling, appropriate visuals, deterministic Red-Amber-Green status formatting, accessibility, and traceability.

## Trigger conditions

Use this skill when the request asks to:

- analyze data and design a management or executive report;
- combine descriptive, predictive, or prescriptive results;
- select or critique charts and visual hierarchy;
- create an HTML dashboard, analytical report, or decision story;
- apply Red-Amber-Green status formatting;
- transform analytical results into recommendations and quantified outcomes;
- validate whether a report follows storytelling-with-data principles.

Do not use this skill to calculate source KPIs, train forecasting models, or optimize recommendations from raw data. Invoke the appropriate analytical skills first and consume their validated outputs.

## Primary agent

Reporting Expert / Storytelling Agent, with final approval from the Validator.

## Inputs

The skill expects a typed reporting package containing as many of these components as are available:

```yaml
report_request:
  audience: executive | management | analyst | operational
  purpose: monitor | explain | decide | act
  reporting_period: string
  decision_question: string
  output: html

validated_results:
  descriptive: []
  predictive: []
  prescriptive: []
  kpis: []
  rag_results: []
  evidence: []
  assumptions: []
  limitations: []
  data_quality: []
```

If the audience, decision question, reporting period, or status thresholds are missing, state the limitation. Never invent them.

## Required companion skills

Use outputs from these skills when applicable:

- `diagnostic.calculate_kpis`
- `diagnostic.analyze_variance`
- `diagnostic.analyze_trends`
- `diagnostic.identify_drivers`
- `diagnostic.detect_anomalies`
- `prognostic.forecast`
- `prognostic.scenarios`
- `prognostic.monte_carlo`
- `prognostic.sensitivity`
- `prescriptive.optimize_actions`
- `prescriptive.new_balance`
- `governance.apply_status_rag`
- `knowledge.retrieve_evidence`
- `validation.validate_results`

## Workflow

### 1. Establish the reporting contract

Identify:

1. audience;
2. business question;
3. decision to support;
4. reporting period;
5. required level of detail;
6. available descriptive, predictive, and prescriptive results;
7. governed RAG rules;
8. evidence, assumptions, limitations, and data-quality warnings.

### 2. Classify analytical content

Apply the following classification:

- **Descriptive:** what happened, current status, actuals, targets, trends, variances, composition, and exceptions.
- **Diagnostic:** where, when, and why the result changed; contribution, segmentation, anomaly, and measurable driver evidence.
- **Predictive:** what is likely to happen; forecast, interval, scenario, probability, simulation, and sensitivity.
- **Prescriptive:** what should be done; action, owner, timing, cost, benefit, risk, constraint, expected impact, and new end result.

Do not label a section predictive if it contains only trends. Do not label advice prescriptive unless its expected effect is quantified or explicitly marked as unquantified.

### 3. Build the decision story

Use this sequence unless the reporting request requires another order:

1. **Executive answer:** status, primary message, decision required.
2. **Current state:** actual versus target/baseline and trend.
3. **Diagnosis:** largest contributors, exceptions, and supported drivers.
4. **Outlook:** base forecast, uncertainty, and scenario range.
5. **Options:** feasible interventions and trade-offs.
6. **Recommendation:** prioritized action or portfolio.
7. **Expected impact:** before/after result and remaining gap/risk.
8. **Confidence and governance:** assumptions, limitations, data quality, evidence, and validation state.

Every page or section must answer a question. Every chart must support a statement. Remove visuals that do not change understanding or action.

### 4. Select visuals

Use the chart-selection rules in `references/visual-selection.md`.

General rules:

- comparison: sorted bar or dot plot;
- time: line chart with target or forecast distinction;
- variance bridge: waterfall;
- part-to-whole: bar, stacked bar, or table; avoid unnecessary pie/donut charts;
- distribution or uncertainty: histogram, box plot, density, fan chart, or interval plot;
- relationship: scatter plot with appropriate caveats;
- probability and scenarios: interval, percentile, tornado, or scenario comparison;
- prescriptive options: impact-effort matrix, ranked action table, waterfall, or before/after comparison;
- exact values and actions: compact table.

Use takeaway titles, direct labels, annotations, and visual emphasis. Avoid 3D, decorative effects, dual axes unless essential and clearly explained, excessive precision, and color-only encoding.

### 5. Apply status RAG

RAG means Red-Amber-Green status in this skill.

- Consume the result from `governance.apply_status_rag`.
- Never infer thresholds from the visual design.
- Never let an LLM assign or override status.
- Display text labels such as `RED`, `AMBER`, and `GREEN` with the color.
- Show actual, target, variance, threshold/rule, trend, and forecast where available.
- Use neutral colors for context and reserve strong status color for exceptions or emphasis.
- Include an accessible symbol or text indicator so color is not the sole carrier of meaning.

### 6. Compose the HTML report

Use semantic HTML and the structure in `references/html-report-contract.md`.

Minimum content:

- report title, period, audience, and generated timestamp;
- executive summary;
- RAG KPI strip;
- descriptive and diagnostic section;
- predictive section;
- prescriptive section;
- action table;
- assumptions and limitations;
- data quality and validation status;
- evidence/source register;
- print-friendly CSS.

### 7. Validate before publication

Run the checks in `references/report-validation.md` and require the Validator to approve the package.

Block publication when:

- narrative values differ from tables or charts;
- a RAG color does not match the governed status result;
- forecast horizon, model reference, or uncertainty is missing where required;
- a recommendation has no stated expected effect and is presented as quantified;
- before/after results do not reconcile;
- an unsupported causal statement appears;
- charts lack labels, units, source context, or accessible descriptions;
- filters or reporting periods are inconsistent.

## Output contract

```yaml
report_package:
  report_id: string
  title: string
  reporting_period: string
  audience: string
  executive_answer: string
  sections: []
  kpi_cards: []
  visuals: []
  actions: []
  assumptions: []
  limitations: []
  evidence: []
  validation_status: pass | fail
  html_artifact_ref: string | null
```

## Guardrails

1. Do not change validated numbers while improving prose or layout.
2. Do not invent thresholds, targets, assumptions, confidence, owners, deadlines, or sources.
3. Separate observed facts, model estimates, scenarios, and recommendations visually and linguistically.
4. Distinguish association from causation.
5. Show uncertainty where predictive outputs provide it.
6. Show both expected benefit and implementation cost/risk for prescriptive outputs when available.
7. Pass references to data and artifacts rather than embedding large datasets in the prompt.
8. Treat retrieved evidence as sourced context, not automatic proof.
9. Preserve units, currency, reporting period, filters, and dimensional grain.
10. Require independent validation before publishing.

## Definition of done

A report is complete only when:

- the intended audience and decision are explicit;
- descriptive, predictive, and prescriptive content is correctly classified;
- the executive message is supported by validated analysis;
- visuals are purposeful, correctly selected, and accessible;
- RAG statuses match governed rules;
- recommendations include expected impact or are marked as unquantified;
- before/after outcomes reconcile;
- assumptions, uncertainty, limitations, and data quality are visible;
- the HTML is semantic, responsive, keyboard usable, and print friendly;
- evidence and analytical lineage are present;
- the validator returns `pass`.
