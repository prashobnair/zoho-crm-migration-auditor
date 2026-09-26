# Design and acceptance notes

## Scope and mapping

The demo's four entity lists approximate organizations → accounts, people → contacts, deals → deals, and activities → activities. These names are **internal illustrative concepts** and must be mapped to current tenant-specific Zoho CRM modules and fields before integration. `stage_mapping` is explicit and reviewable, rather than silently assigning an unknown stage. No actual Zoho payload is generated; custom fields, notes, owners, currencies, attachments and date/time conversion are out of scope.

## Pilot and validation checklist

1. Inventory source data and exports; verify legal basis and strip sensitive data from fixtures.
2. Capture current destination state and backup before a pilot, with immutable source IDs.
3. Approve target fields, lookup relationships, owner mappings, picklists and stage mapping with a business owner.
4. Run this offline preflight. For every issue, decide fix/skip/merge explicitly and save the decision outside this demo.
5. Pilot a limited record subset in a sandbox; map source IDs to returned target IDs, compare values and counts, sample linked activities and histories.
6. Test rerun idempotency, duplicate policy, rate-limit retry and partial-failure recovery before full cutover.
7. Reconcile after cutover with a signed report. Rollback must use verified target IDs, reverse dependency order and a backup, and must not erase later user edits.

## Test matrix

`test_migration.py` covers deliberately broken source data, clean source, duplicate IDs, orphan activity, malformed envelope and deterministic repeated runs. A production suite would add malformed dates, custom field coercion, large-batch pagination, partial retries, PII redaction and live sandbox contract tests. `--strict` can fail a CI preflight with code 2; code 1 means the fixture itself could not be read/parsed.

## Safety and limitations

The tool is deliberately read-only and local. It doesn't authenticate to Zoho, create an import job, claim external API compatibility, or infer an SLA. `EMAIL` is a lightweight demo syntax check, not full RFC validation. Casefolded email is a possible match, not identity proof. A readiness pass means only that these narrow checks pass, not that importing is safe without the pilot and approvals above.
