#!/usr/bin/env python3
"""Lightweight validator for a workspace-standards instance file.

Not a full JSON Schema engine (no `jsonschema`/`ajv` available in this
environment) — checks the specific shape rules that matter here: required
fields present, dates parse and are self-consistent, known enums respected.
Good enough to catch the failure mode the schema's own research notes flag
(LLM-generated YAML with a plausible-looking but structurally wrong edit).

A repo's instance file may set `extends: <path>` to a workspace-level (or
another repo's) instance file. Resolution is block-level, not deep-merged:
any top-level key present locally REPLACES the inherited value wholesale
(e.g. setting your own `repoRoot` replaces the whole inherited repoRoot,
it doesn't merge individual sub-keys) — same "closer file wins" simplicity
as EditorConfig, chosen so a local override is never a surprise partial
merge. By default every command below validates/prints the RESOLVED
(merged) config, i.e. what's actually in effect for this repo — pass
--raw to operate on the local file's own declared content only.

Usage:
  validate_workspace_standards.py <instance.yml>            # full check on the resolved config
  validate_workspace_standards.py <instance.yml> --resolve   # print the merged effective config as YAML
  validate_workspace_standards.py <instance.yml> --due       # exit 0 if review is due, 1 if not
  validate_workspace_standards.py <instance.yml> --quiet     # full check, no output unless it fails
  validate_workspace_standards.py <instance.yml> --raw       # operate on the local file only, don't resolve extends
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


def resolve_extends(path: Path, seen: set | None = None) -> dict:
    """Return the fully-merged effective config for `path`, following
    `extends` chains. Block-level override: each top-level key in a more
    local file replaces the corresponding key inherited from its base
    entirely (see module docstring)."""
    path = path.expanduser().resolve()
    seen = seen or set()
    if path in seen:
        raise ValueError(f"extends cycle detected at {path}")
    seen = seen | {path}

    doc = load(path) or {}
    extends_raw = doc.pop("extends", None)
    if not extends_raw:
        return doc

    base_path = Path(extends_raw).expanduser()
    if not base_path.is_absolute():
        base_path = (path.parent / base_path).resolve()
    if not base_path.exists():
        # Can't resolve (e.g. dotfiles not cloned on this machine) — fall
        # back to the local file alone rather than crashing; the missing
        # base will surface as a warning, not a validation crash.
        doc["_extendsUnresolved"] = str(extends_raw)
        return doc

    base = resolve_extends(base_path, seen)
    merged = dict(base)
    merged.update(doc)  # local keys win wholesale, per key
    return merged


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

    raw = "--raw" in flags
    if raw:
        doc = load(path)
        unresolved_note = None
    else:
        doc = resolve_extends(path)
        unresolved_note = doc.pop("_extendsUnresolved", None)

    if "--resolve" in flags:
        print(f"# resolved effective config for {path}")
        if unresolved_note:
            print(f"# NOTE: extends target '{unresolved_note}' not found on this machine — showing local file only")
        print(yaml.safe_dump(doc, sort_keys=False, default_flow_style=False))
        sys.exit(0)

    errors = validate(doc)
    if unresolved_note:
        errors.insert(0, f"extends: target '{unresolved_note}' not found on this machine (dotfiles not cloned here?) — validated local file alone")

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
