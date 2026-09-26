"""Offline, dry-run CRM migration audit. No Zoho API calls or writes."""
from __future__ import annotations
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
import re

EMAIL = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

@dataclass(frozen=True)
class Issue:
    severity: str
    entity: str
    source_id: str
    code: str
    detail: str


def _id(row):
    return str(row.get("id", "")).strip()


def audit(payload: dict) -> dict:
    """Validate a fictional source export and propose, never perform, a target import."""
    entities = ("organizations", "people", "deals", "activities")
    if not isinstance(payload, dict) or any(not isinstance(payload.get(e), list) for e in entities):
        raise ValueError("Expected lists: organizations, people, deals, activities")
    mappings = payload.get("stage_mapping")
    if not isinstance(mappings, dict):
        raise ValueError("stage_mapping must be an object")
    issues: list[Issue] = []
    ids: dict[str, set[str]] = {}
    for entity in entities:
        seen = set()
        for row in payload[entity]:
            if not isinstance(row, dict):
                raise ValueError(f"{entity} must contain objects")
            key = _id(row)
            if not key:
                issues.append(Issue("error", entity, "", "missing_id", "Source ID is required"))
            elif key in seen:
                issues.append(Issue("error", entity, key, "duplicate_id", "Source ID repeats"))
            seen.add(key)
        ids[entity] = seen - {""}

    by_email: dict[str, str] = {}
    for person in payload["people"]:
        key, email = _id(person), str(person.get("email", "")).strip().casefold()
        if not EMAIL.fullmatch(email):
            issues.append(Issue("error", "people", key, "invalid_email", "Email cannot be matched safely"))
        elif email in by_email:
            issues.append(Issue("review", "people", key, "possible_duplicate", f"Email matches source person {by_email[email]}"))
        else:
            by_email[email] = key
        if str(person.get("organization_id", "")) not in ids["organizations"]:
            issues.append(Issue("error", "people", key, "orphan_organization", "Organization ID not present"))

    for deal in payload["deals"]:
        key = _id(deal)
        if str(deal.get("person_id", "")) not in ids["people"]:
            issues.append(Issue("error", "deals", key, "orphan_person", "Person ID not present"))
        if str(deal.get("stage", "")) not in mappings:
            issues.append(Issue("error", "deals", key, "unmapped_stage", "No approved target stage mapping"))

    for activity in payload["activities"]:
        key = _id(activity)
        if str(activity.get("deal_id", "")) not in ids["deals"]:
            issues.append(Issue("error", "activities", key, "orphan_deal", "Deal ID not present"))

    order = {e: i for i, e in enumerate(entities)}
    issues.sort(key=lambda x: (order[x.entity], x.source_id, x.code))
    counts = {e: len(payload[e]) for e in entities}
    errors = sum(x.severity == "error" for x in issues)
    review = sum(x.severity == "review" for x in issues)
    # A duplicate is not silently merged. Even review-only imports need a human decision.
    return {
        "mode": "dry_run_only", "ready_for_import": errors == 0 and review == 0,
        "source_counts": counts, "target_preview_counts": counts if errors == 0 and review == 0 else None,
        "issues": [asdict(x) for x in issues],
        "import_order": list(entities),
        "rollback_manifest": {
            "precondition": "Keep original export and a dated target backup before any real import",
            "source_ids": {e: sorted(ids[e]) for e in entities},
            "action": "No rollback executed; validate target IDs and inverse dependencies in a pilot first"
        },
    }
