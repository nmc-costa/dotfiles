#!/usr/bin/env python3
"""Lightweight validator for a workspace-standards instance file.

Not a full JSON Schema engine (no `jsonschema`/`ajv` available in this
environment) — checks the specific shape rules that matter here: required
fields present, dates parse and are self-consistent, known enums respected.
Good enough to catch the failure mode the schema's own research notes flag
(LLM-generated YAML with a plausible-looking but structurally wrong edit).

Usage:
  validate_workspace_standards.py <instance.yml>            # full check, prints report
  validate_workspace_standards.py <instance.yml> --due       # exit 0 if review is due, 1 if not
  validate_workspace_standards.py <instance.yml> --quiet     # full check, no output unless it fails
"""
import sys
import re
import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("FAIL: pyyaml not installed (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")


def load(path: Path):
    text = path.read_text()
    if path.suffix in (".yml", ".yaml"):
        return yaml.safe_load(text)
    import json
    return json.loads(text)


def parse_date(s, errors, field):
    if not isinstance(s, str) or not DATE_RE.match(s):
        errors.append(f"{field}: '{s}' is not an ISO date (YYYY-MM-DD)")
        return None
    try:
        return datetime.date.fromisoformat(s)
    except ValueError as e:
        errors.append(f"{field}: '{s}' does not parse ({e})")
        return None


def validate(doc: dict) -> list[str]:
    errors = []
    if not isinstance(doc, dict):
        return ["document root is not a mapping"]

    sv = doc.get("schemaVersion")
    if sv is None:
        errors.append("schemaVersion: required, missing")
    elif not SEMVER_RE.match(str(sv)):
        errors.append(f"schemaVersion: '{sv}' is not semver (x.y.z)")

    review = doc.get("review")
    if review is None:
        errors.append("review: required block, missing")
    elif not isinstance(review, dict):
        errors.append("review: must be a mapping")
    else:
        cadence = review.get("cadenceDays")
        if not isinstance(cadence, int) or cadence < 1:
            errors.append(f"review.cadenceDays: must be a positive integer, got {cadence!r}")
        last = parse_date(review.get("lastReviewed"), errors, "review.lastReviewed")
        next_due_raw = review.get("nextDue")
        if next_due_raw is not None:
            next_due = parse_date(next_due_raw, errors, "review.nextDue")
            if last and next_due and isinstance(cadence, int):
                expected = last + datetime.timedelta(days=cadence)
                if next_due != expected:
                    errors.append(
                        f"review.nextDue: '{next_due_raw}' inconsistent with "
                        f"lastReviewed + cadenceDays (expected {expected.isoformat()})"
                    )
        onDrift = review.get("onDrift", "open-pr")
        if onDrift not in ("open-pr", "report-only"):
            errors.append(f"review.onDrift: '{onDrift}' not one of open-pr, report-only")

    entry = doc.get("agentEntrypoints")
    if entry is not None:
        canonical = entry.get("canonical")
        if canonical is not None and canonical not in ("AGENTS.md", "CLAUDE.md"):
            errors.append(f"agentEntrypoints.canonical: '{canonical}' not AGENTS.md or CLAUDE.md")

    readme = doc.get("readme")
    if readme is not None:
        sections = readme.get("requiredSections")
        if sections is not None and not isinstance(sections, list):
            errors.append("readme.requiredSections: must be a list")
        diagram = readme.get("diagram")
        if diagram is not None:
            dtype = diagram.get("type")
            if dtype is not None and dtype not in ("mermaid-flowchart", "mermaid-mindmap", "none"):
                errors.append(f"readme.diagram.type: '{dtype}' not a known diagram type")

    role = doc.get("repoRole")
    if role is not None and role not in (
        "workspace-control-plane", "personal-project", "org-project", "archived"
    ):
        errors.append(f"repoRole: '{role}' not a known role")

    return errors


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(2)
    path = Path(args[0])
    if not path.exists():
        print(f"FAIL: {path} does not exist", file=sys.stderr)
        sys.exit(2)

    doc = load(path)
    errors = validate(doc)

    if "--due" in flags:
        review = (doc or {}).get("review", {})
        next_due = review.get("nextDue")
        if not next_due:
            # No nextDue recorded -> treat as due (never reviewed on schedule).
            sys.exit(0)
        try:
            due_date = datetime.date.fromisoformat(str(next_due))
        except ValueError:
            sys.exit(0)  # malformed date -> treat as due, let the full check report why
        sys.exit(0 if datetime.date.today() >= due_date else 1)

    quiet = "--quiet" in flags
    if errors:
        print(f"=== {path}: {len(errors)} error(s) ===")
        for e in errors:
            print(f"  FAIL {e}")
        sys.exit(1)
    if not quiet:
        print(f"=== {path}: OK ===")
    sys.exit(0)


if __name__ == "__main__":
    main()
