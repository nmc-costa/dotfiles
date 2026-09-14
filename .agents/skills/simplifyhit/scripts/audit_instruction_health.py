#!/usr/bin/env python3
"""
Audit Instruction Health Script

Measures system instruction quality metrics:
- Word count vs token budget
- Section structure completeness
- Critical rules count (target: 3-5)
- Anti-patterns count (target: 3-5)
- Flowchart presence
- Example presence
- Estimated token overhead
- Readability score (Flesch-Kincaid)

Usage:
    python audit_instruction_health.py --file ../../../instructions/base-personas/archi.md
    python audit_instruction_health.py --file ../../../instructions/base-personas/archi.md --verbose
    python audit_instruction_health.py --audit-all  # Audit all instructions under .agents/instructions/
"""

import os
import re
import sys
import json
from pathlib import Path
from collections import namedtuple
import argparse

# Token estimation: Average 1 token per 4 characters (rough)
CHARS_PER_TOKEN = 4.0


# Readability calculation: Flesch-Kincaid Grade Level
def flesch_kincaid_grade(text):
    """Calculate Flesch-Kincaid Grade Level."""
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]

    words = text.split()

    # Syllable estimation (very rough)
    def count_syllables(word):
        word = word.lower()
        syllable_count = 0
        vowels = "aeiou"
        previous_was_vowel = False
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel
        if word.endswith("e"):
            syllable_count -= 1
        if word.endswith("le") and len(word) > 2 and word[-3] not in vowels:
            syllable_count += 1
        return max(1, syllable_count)

    total_syllables = sum(count_syllables(word) for word in words)

    if len(sentences) == 0 or len(words) == 0:
        return 0.0

    grade = 0.39 * (len(words) / len(sentences)) + 11.8 * (total_syllables / len(words)) - 15.59
    return max(0, grade)


class InstructionAudit:
    """Audit system instruction health."""

    def __init__(self, filepath):
        self.filepath = filepath
        self.name = filepath.stem
        self.content = self._load_file()
        self.results = {}

    def _load_file(self):
        """Load instruction file."""
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            print(f"❌ File not found: {self.filepath}")
            sys.exit(1)

    def _extract_metadata(self):
        """Extract YAML metadata block."""
        match = re.match(r"---\n(.*?)\n---", self.content, re.DOTALL)
        if match:
            yaml_content = match.group(1)
            metadata = {}
            for line in yaml_content.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    metadata[key.strip()] = value.strip()
            return metadata
        return {}

    def check_metadata(self):
        """Check for YAML metadata block."""
        if re.match(r"^---\n", self.content):
            self.results["metadata_present"] = True
            metadata = self._extract_metadata()
            self.results["metadata"] = metadata
            required_keys = ["name", "version", "token_budget"]
            missing = [k for k in required_keys if k not in metadata]
            self.results["metadata_complete"] = len(missing) == 0
            if missing:
                self.results["metadata_missing_keys"] = missing
            return True
        self.results["metadata_present"] = False
        return False

    def check_purpose_statement(self):
        """Check for one-sentence purpose statement."""
        # Look for "## ONE-SENTENCE PURPOSE" or "## Purpose"
        pattern = r"##\s*(?:ONE-SENTENCE\s+)?PURPOSE\s*\n+([^\n]+(?:\n[^\n]+)*?)\n\n"
        match = re.search(pattern, self.content, re.IGNORECASE)
        if match:
            purpose = match.group(1).strip()
            word_count = len(purpose.split())
            self.results["purpose_statement_present"] = True
            self.results["purpose_statement"] = purpose[:100] + "..." if len(purpose) > 100 else purpose
            self.results["purpose_word_count"] = word_count
            self.results["purpose_concise"] = word_count <= 20  # Target ≤15, allowing some tolerance
            return True
        self.results["purpose_statement_present"] = False
        return False

    def check_critical_rules(self):
        """Check for critical rules section."""
        # Look for critical rules table or list
        patterns = [
            r"##\s*CRITICAL\s+RULES.*?\n(.*?)(?=\n##|\Z)",
            r"##\s*CRITICAL.*?\n(.*?)(?=\n##|\Z)",
        ]

        for pattern in patterns:
            match = re.search(pattern, self.content, re.IGNORECASE | re.DOTALL)
            if match:
                rules_section = match.group(1)
                # Count pipe-separated rows (table format)
                rows = [row for row in rules_section.split("\n") if "|" in row]
                # Count bullet points
                bullets = [line for line in rules_section.split("\n") if line.strip().startswith("- ")]
                # Count numbered items
                numbers = [line for line in rules_section.split("\n") if re.match(r"^\s*\d+\.", line)]

                rule_count = max(len(rows) // 2, len(bullets), len(numbers))  # Table rows counted as pairs

                self.results["critical_rules_present"] = True
                self.results["critical_rules_count"] = rule_count
                self.results["critical_rules_optimal"] = 3 <= rule_count <= 5
                return True

        self.results["critical_rules_present"] = False
        self.results["critical_rules_count"] = 0
        return False

    def check_anti_patterns(self):
        """Check for anti-patterns section."""
        patterns = [
            r"##\s*ANTI[_-]?PATTERNS.*?\n(.*?)(?=\n##|\Z)",
            r"##\s*COMMON\s+MISTAKES.*?\n(.*?)(?=\n##|\Z)",
        ]

        for pattern in patterns:
            match = re.search(pattern, self.content, re.IGNORECASE | re.DOTALL)
            if match:
                anti_section = match.group(1)
                # Count ❌ emoji markers or "### [Pattern]" headings
                emoji_count = anti_section.count("❌")
                heading_count = len(re.findall(r"^###\s+", anti_section, re.MULTILINE))
                pattern_count = max(emoji_count, heading_count)

                self.results["anti_patterns_present"] = True
                self.results["anti_patterns_count"] = pattern_count
                self.results["anti_patterns_optimal"] = 3 <= pattern_count <= 5
                return True

        self.results["anti_patterns_present"] = False
        self.results["anti_patterns_count"] = 0
        return False

    def check_flowchart(self):
        """Check for mermaid flowchart."""
        has_flowchart = "```mermaid" in self.content
        self.results["flowchart_present"] = has_flowchart
        return has_flowchart

    def check_examples(self):
        """Check for concrete examples section."""
        patterns = [
            r"##\s*EXAMPLE",
            r"##\s*CONCRETE\s+EXAMPLE",
            r"##\s*CASE\s+STUDY",
            r"##\s*WALKTHROUGH",
        ]

        has_examples = any(re.search(pattern, self.content, re.IGNORECASE) for pattern in patterns)
        self.results["examples_present"] = has_examples
        return has_examples

    def check_improvement_loop(self):
        """Check for improvement/feedback loop section."""
        patterns = [
            r"##\s*IMPROVEMENT\s+LOOP",
            r"##\s*FEEDBACK\s+LOOP",
            r"##\s*AUDIT",
            r"##\s*METRICS",
        ]

        has_loop = any(re.search(pattern, self.content, re.IGNORECASE) for pattern in patterns)
        self.results["improvement_loop_present"] = has_loop
        return has_loop

    def measure_word_count(self):
        """Count words in content."""
        words = len(self.content.split())
        self.results["word_count"] = words

        # Estimate tokens
        chars = len(self.content)
        estimated_tokens = int(chars / CHARS_PER_TOKEN)
        self.results["estimated_tokens"] = estimated_tokens

        # Check budget
        metadata = self._extract_metadata()
        budget = metadata.get("token_budget", "2500")
        try:
            budget_int = int(budget)
            self.results["token_budget"] = budget_int
            self.results["within_budget"] = estimated_tokens <= budget_int
        except ValueError:
            self.results["token_budget"] = None
            self.results["within_budget"] = None

        return words

    def measure_readability(self):
        """Calculate Flesch-Kincaid Grade Level."""
        # Extract main content (skip metadata)
        content_without_meta = re.sub(r"^---.*?---\n", "", self.content, flags=re.DOTALL)

        grade = flesch_kincaid_grade(content_without_meta)
        self.results["flesch_kincaid_grade"] = round(grade, 1)
        self.results["readability_acceptable"] = grade <= 11  # Target: High school level

        return grade

    def check_section_structure(self):
        """Check overall section structure."""
        sections = re.findall(r"^##\s+(.+)$", self.content, re.MULTILINE)
        self.results["section_count"] = len(sections)
        self.results["sections"] = sections

        # Check for key sections
        key_sections = ["PURPOSE", "CRITICAL", "WORKFLOW", "EXAMPLE", "ANTI"]
        found_sections = sum(1 for section in sections for key in key_sections if key.upper() in section.upper())
        self.results["key_sections_found"] = found_sections
        self.results["key_sections_target"] = len(key_sections)

        return len(sections)

    def run_full_audit(self):
        """Run complete audit."""
        self.check_metadata()
        self.check_purpose_statement()
        self.check_critical_rules()
        self.check_anti_patterns()
        self.check_flowchart()
        self.check_examples()
        self.check_improvement_loop()
        self.measure_word_count()
        self.measure_readability()
        self.check_section_structure()

        return self.results

    def generate_report(self, verbose=False):
        """Generate audit report."""
        results = self.results

        # Score calculation
        checks = {
            "metadata_present": (10, results.get("metadata_present", False)),
            "purpose_statement_present": (10, results.get("purpose_statement_present", False)),
            "purpose_concise": (5, results.get("purpose_concise", False)),
            "critical_rules_present": (15, results.get("critical_rules_present", False)),
            "critical_rules_optimal": (10, results.get("critical_rules_optimal", False)),
            "anti_patterns_present": (15, results.get("anti_patterns_present", False)),
            "anti_patterns_optimal": (10, results.get("anti_patterns_optimal", False)),
            "flowchart_present": (10, results.get("flowchart_present", False)),
            "examples_present": (10, results.get("examples_present", False)),
            "improvement_loop_present": (5, results.get("improvement_loop_present", False)),
            "within_budget": (5, results.get("within_budget", True)),  # Default to True if no budget
            "readability_acceptable": (5, results.get("readability_acceptable", False)),
        }

        total_score = sum(weight for weight, passed in checks.values() if passed)
        max_score = sum(weight for weight, _ in checks.values())
        percentage = (total_score / max_score * 100) if max_score > 0 else 0

        # Print report
        print(f"\n{'='*70}")
        print(f"INSTRUCTION AUDIT REPORT: {self.name}")
        print(f"{'='*70}\n")

        print(f"📊 OVERALL SCORE: {total_score}/{max_score} ({percentage:.0f}%)\n")

        if percentage >= 80:
            status = "✅ PASS - Ready for production"
        elif percentage >= 60:
            status = "⚠️  REVIEW - Needs improvements"
        else:
            status = "❌ FAIL - Requires restructuring"

        print(f"STATUS: {status}\n")

        # Detailed results
        print("CHECKLIST:")
        for check_name, (weight, passed) in checks.items():
            symbol = "✅" if passed else "❌"
            print(f"  {symbol} {check_name.replace('_', ' ').title()} ({weight}pts)")

        print(f"\nMETRICS:")
        print(f"  📝 Word Count: {results.get('word_count', 'N/A')} words")
        print(f"  🔤 Estimated Tokens: {results.get('estimated_tokens', 'N/A')} tokens", end="")
        budget = results.get("token_budget")
        if budget:
            within = "✓" if results.get("within_budget") else "✗"
            print(f" (Budget: {budget}) {within}")
        else:
            print()
        print(f"  📖 Readability (FK Grade): {results.get('flesch_kincaid_grade', 'N/A')} (target: <11)")
        print(f"  🏗️  Sections: {results.get('section_count', 'N/A')} total")
        print(f"  📋 Critical Rules: {results.get('critical_rules_count', 0)} (target: 3-5)")
        print(f"  ⛔ Anti-Patterns: {results.get('anti_patterns_count', 0)} (target: 3-5)")
        print(f"  📊 Key Sections Found: {results.get('key_sections_found', 0)}/{results.get('key_sections_target', 0)}")

        if verbose:
            print(f"\nSECTIONS FOUND:")
            for section in results.get("sections", []):
                print(f"  - {section}")

            if results.get("purpose_statement_present"):
                print(f"\nPURPOSE STATEMENT:")
                print(f"  {results.get('purpose_statement', 'N/A')}")

            if results.get("metadata_present"):
                print(f"\nMETADATA:")
                for key, value in results.get("metadata", {}).items():
                    print(f"  {key}: {value}")

        print(f"\n{'='*70}\n")

        return {"score": total_score, "max_score": max_score, "percentage": percentage, "status": status, "checks": checks, "results": results}


def audit_all_instructions(directory):
    """Audit all instructions in a directory."""
    instruction_dir = Path(directory)
    if not instruction_dir.exists():
        print(f"❌ Directory not found: {instruction_dir}")
        return

    md_files = sorted(instruction_dir.glob("*.md"))
    if not md_files:
        print(f"❌ No .md files found in {instruction_dir}")
        return

    print(f"\n🔍 Auditing {len(md_files)} instruction file(s) in {instruction_dir}...\n")

    all_reports = []
    for md_file in md_files:
        audit = InstructionAudit(md_file)
        audit.run_full_audit()
        report = audit.generate_report(verbose=False)
        all_reports.append(report)

    # Summary
    avg_score = sum(r["percentage"] for r in all_reports) / len(all_reports)
    print(f"\n📊 SUMMARY: Average Score {avg_score:.0f}%")
    print(f"   Pass (≥80%): {sum(1 for r in all_reports if r['percentage'] >= 80)}")
    print(f"   Review (60-79%): {sum(1 for r in all_reports if 60 <= r['percentage'] < 80)}")
    print(f"   Fail (<60%): {sum(1 for r in all_reports if r['percentage'] < 60)}")


if __name__ == "__main__":
    # Default target is .agents/instructions/ relative to THIS file's location
    # (scripts/ -> simplifyhit/ -> skills/ -> .agents/), so this works no matter
    # where the repo is cloned or which user's home it lives under.
    _DEFAULT_INSTRUCTIONS_DIR = Path(__file__).resolve().parents[3] / "instructions"

    parser = argparse.ArgumentParser(description="Audit system instruction health and quality metrics.")
    parser.add_argument("--file", type=str, help="Path to instruction file to audit")
    parser.add_argument("--audit-all", action="store_true", help="Audit all instructions in --directory")
    parser.add_argument(
        "--directory",
        type=str,
        default=str(_DEFAULT_INSTRUCTIONS_DIR),
        help="Directory to audit (with --audit-all); defaults to .agents/instructions/ next to this script",
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.audit_all:
        audit_all_instructions(args.directory)
    elif args.file:
        audit = InstructionAudit(Path(args.file))
        audit.run_full_audit()
        if args.json:
            print(json.dumps(audit.results, indent=2))
        else:
            audit.generate_report(verbose=args.verbose)
    else:
        parser.print_help()
