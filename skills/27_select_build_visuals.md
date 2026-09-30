# 27 - Select and Build Visuals

## Purpose

Select and format data visualizations strictly adhering to Edward Tufte's Data-Ink ratio principles: eliminating chartjunk, vertical gridlines, drop shadows, and decorative clutter, using direct labeling, and applying muted color palettes with selective highlights.

## Trigger conditions

- Composing visual charts for management presentations, reports, or HTML dashboards.
- Reviewing visual clarity and information density of analytical outputs.

## Primary agent

**Visual Design & Data-Ink Agent**

## Inputs

```yaml
visual_selection_request:
  data_type: "variance_bridge" | "time_series_trend" | "category_comparison" | "distribution"
  target_audience: "executive" | "controller" | "project_manager"
  data_payload: object
  design_constraints:
    tufte_compliant: true
    no_vertical_gridlines: true
    direct_labeling: true
    no_drop_shadows: true
```

## Outputs

```yaml
visual_selection_result:
  selected_chart_type: "waterfall" | "sparkline" | "direct_labeled_line" | "sorted_bar" | "clean_table"
  chart_configuration:
    palette: "muted_slate" # highlight with red/amber only on active variances
    gridlines: "horizontal_subtle_only"
    direct_labels: list[object]
    legend: "none_embedded_labels"
  accessibility:
    high_contrast: boolean
    screen_reader_summary: string
```

## Responsibilities

1. **Chart Type Selection:**
   - Variance analysis $\rightarrow$ **Waterfall bridge**.
   - Multi-period trends $\rightarrow$ **Line chart with direct end-point labeling**.
   - Cost category rankings $\rightarrow$ **Horizontal sorted bar chart**.
   - Exact numbers $\rightarrow$ **Clean table without vertical gridlines**.
2. **Data-Ink Maximization:** Remove background drop shadows, decorative icons, heavy borders, and 3D effects.
3. **Typography & Layout:** Right-align all numeric values with aligned decimal places; left-align text headers.

## Guardrails

- Never use pie or donut charts for complex financial comparisons.
- Never use color as the sole conveyor of status or meaning.

## Definition of done

- Visual specifications formatted with high data-ink density, direct labeling, and zero visual clutter.
