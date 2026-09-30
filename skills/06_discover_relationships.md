# 06 - Discover Relationships

## Purpose

Discover, validate, and document foreign key relationships and dimensional associations between fact tables (`FactGL`, `FactBudget`, `FactForecast`, `FactFTE`) and dimension tables (`DimDate`, `DimAccount`, `DimOrganization`, `DimProject`).

## Trigger conditions

- Schema inference completed (`05_infer_schema.md`).
- Explicit `Relationships.csv` file provided for verification or automatic join discovery required.

## Primary agent

**Relational Modeler Agent**

## Inputs

```yaml
relationship_discovery_request:
  table_schemas: map[table_name, columns]
  declared_relationships_file: string | null # e.g. "Relationships.csv"
  max_unmatched_ratio: float # e.g. 0.001
```

## Outputs

```yaml
relationship_discovery_result:
  relationships:
    - from_table: string
      from_column: string
      to_table: string
      to_column: string
      cardinality: "many-to-one" | "one-to-one" | "many-to-many"
      orphan_keys_count: integer
      match_rate_pct: float
      valid: boolean
  model_topology: star | snowflake | constellation
  integrity_issues: list[string]
```

## Responsibilities

1. **Declared Relationship Verification:** Validate whether foreign keys in fact tables match corresponding dimension primary keys.
2. **Orphan Key Detection:** Flag transactions in fact tables referencing non-existent accounts, departments, or project codes.
3. **Cardinality Verification:** Confirm that dimensions on the "one" side of the relationship contain strictly unique primary keys.

## Guardrails

- Never silently drop fact records with orphan foreign keys; report and quarantine them.
- Avoid many-to-many relationships in the analytical core without bridge tables.

## Definition of done

- Every declared or discovered foreign key relationship is tested for referential integrity.
