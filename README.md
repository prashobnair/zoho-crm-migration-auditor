# Zoho CRM Migration Auditor

An offline, **dry-run** portfolio example for evaluating a fictional CRM migration before any import. It maps an example deal stage, checks foreign-key relationships and duplicate email candidates, and produces a review report and rollback checklist. It does **not** connect to Zoho, migrate real data, merge contacts, or promise a one-click rollback.

## Contract use-case

A [Pipedrive-to-Zoho migration brief](https://www.freelancer.com/projects/sales-management/pipedrive-zoho-crm-migration) calls for contacts, deals, activities, custom fields and stages, a test import, validation and fallback. A [Zoho CRM setup/cleanup brief](https://www.freelancer.com/projects/zoho-crm/zoho-crm-setup-cleanup) adds deduplication and layout/workflow concerns. These were research examples, not live client engagements. This repo covers the *preflight and reconciliation* slice, not layouts or production workflows.

## Run

Python 3.10+ and standard library only. Clone or download the repository, then from its root:

```sh
python3 cli.py examples.json
python3 cli.py examples.json --strict  # exit code 2 if not ready
python3 -m unittest discover -p 'test_*.py' -v
```

The fixture is entirely fictional and deliberately bad: an email duplicate, an orphan organization, an orphan deal-person relationship and an unmapped stage. The report should show `ready_for_import: false`, four issues, source counts of 1 organization, 3 people, 2 deals and 1 activity, and `target_preview_counts: null`. Edit a copy of the fixture to remove the second and third people and second deal to see a clean pass. No Zoho trial, API key, network, Docker or paid service is needed.

## Input and outputs

Four lists, `organizations`, `people`, `deals`, `activities`, contain records with unique `id`s. People refer to `organization_id`, deals to `person_id`, activities to `deal_id`. `stage_mapping` explicitly maps source stage names to target labels. This is a **fictional intermediate schema**, not a statement of Zoho or Pipedrive API field names. Email is normalized with trimming and casefolding for duplicate candidates only. Duplicate candidates require human review; no automatic merge is safe. For this demo any error or review issue blocks readiness. Output has stable issue codes, counts, dependency order and source-ID inventory to assist a pilot rollback plan. It never writes a target record.

## Real deployment boundary

A real implementation would first confirm the tenant's current Zoho CRM API module/field metadata, permissions, limits and data region; use a sandbox, map every custom field, retain activity/note history, handle pagination and rate limits, perform a small test import, reconcile source-to-target IDs and totals, then approve cutover and a tested inverse plan. The rollback manifest here is **not** an executable deletion plan: source IDs are not target IDs, and deletion could remove unrelated changes. Never import client records into this repository. See `DESIGN.md` for mapping, test and operator decisions.
