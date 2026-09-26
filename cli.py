"""Run: python3 cli.py examples.json [--strict]. No network or credentials."""
import argparse
import json
from pathlib import Path
from migration import audit

def main():
    parser = argparse.ArgumentParser(description="Preview a fictional CRM migration")
    parser.add_argument("fixture", help="JSON export containing fictional CRM records")
    parser.add_argument("--strict", action="store_true", help="exit 2 when import is not ready")
    args = parser.parse_args()
    try:
        report = audit(json.loads(Path(args.fixture).read_text(encoding="utf-8")))
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        parser.exit(1, f"Input error: {exc}\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    if args.strict and not report["ready_for_import"]:
        parser.exit(2)

if __name__ == "__main__":
    main()
