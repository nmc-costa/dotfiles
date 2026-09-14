#!/usr/bin/env python3
"""
DOCX Content Injector for Project Charters

Purpose:
  - Read approved markdown (charter_draft_approved.md) with generated content
  - Inject section-level content into DOCX template
  - Apply field-level replacements for VARIABLE and ADAPTIVE fields
  - Preserve RIGID sections unchanged
  - Maintain all formatting and styles

Usage:
  python docx_injector.py \
    --template <template.docx> \
    --content <charter_draft_approved.md> \
    --replacements <replacements.json> \
    --output <Final_Charter.docx>
"""

import json
import argparse
import re
from pathlib import Path
from datetime import datetime

try:
    from docx import Document
    from docx.shared import Pt, RGBColor
except ImportError as e:
    import sys

    print(f"ERROR: Failed to import python-docx: {e}")
    print(f"Python: {sys.executable}")
    sys.exit(1)


class DocxInjector:
    """Inject markdown content into DOCX template while preserving structure."""

    def __init__(self, template_path, content_path, replacements_path, output_path, log_path=None):
        """Initialize injector."""
        self.template_path = Path(template_path)
        self.content_path = Path(content_path)
        self.replacements_path = Path(replacements_path)
        self.output_path = Path(output_path)
        self.log_path = Path(log_path) if log_path else None

        self.doc = None
        self.markdown_sections = {}
        self.replacements = {}
        self.injection_log = {
            "timestamp": datetime.now().isoformat(),
            "template": str(template_path),
            "content": str(content_path),
            "replacements": str(replacements_path),
            "output": str(output_path),
            "injections": [],
            "replacements_applied": [],
            "errors": [],
            "statistics": {"sections_regenerated": 0, "fields_replaced": 0, "errors_encountered": 0},
        }

    def inject(self):
        """Execute full injection workflow."""
        print("[1/6] Loading template...")
        if not self._load_template():
            return False

        print("[2/6] Parsing markdown content...")
        if not self._parse_markdown():
            return False

        print("[3/6] Loading field replacements...")
        if not self._load_replacements():
            return False

        print("[4/6] Extracting section structure...")
        sections_to_regenerate = self._extract_sections()

        print("[5/6] Injecting content...")
        if not self._inject_content(sections_to_regenerate):
            return False

        print("[6/6] Saving document...")
        if not self._save_document():
            return False

        return True

    def _load_template(self):
        """Load template DOCX."""
        try:
            self.doc = Document(self.template_path)
            print(f"  ✅ Loaded template ({len(self.doc.paragraphs)} paragraphs)")
            return True
        except Exception as e:
            print(f"  ❌ Failed: {str(e)}")
            self.injection_log["errors"].append(f"Template load failed: {str(e)}")
            return False

    def _parse_markdown(self):
        """Parse markdown content by sections."""
        try:
            with open(self.content_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract sections marked with <!-- SECTION: ... -->
            pattern = r"<!-- SECTION:\s*(.+?)\s*-->(.*?)<!-- END SECTION -->"
            matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)

            if not matches:
                print(f"  ⚠️  No sections found in markdown (expected <!-- SECTION: ... --> format)")
                self.injection_log["errors"].append("No markdown sections found")
                return False

            for section_id, section_content in matches:
                section_id = section_id.strip()
                section_content = section_content.strip()
                self.markdown_sections[section_id] = section_content

            print(f"  ✅ Parsed {len(self.markdown_sections)} markdown sections")
            return True
        except Exception as e:
            print(f"  ❌ Failed: {str(e)}")
            self.injection_log["errors"].append(f"Markdown parse failed: {str(e)}")
            return False

    def _load_replacements(self):
        """Load field replacement mappings."""
        try:
            with open(self.replacements_path, "r", encoding="utf-8") as f:
                self.replacements = json.load(f)

            # Flatten replacements to simple old -> new mapping
            flat_replacements = {}
            if isinstance(self.replacements, dict):
                for key, value in self.replacements.items():
                    if isinstance(value, dict) and "old" in value and "new" in value:
                        flat_replacements[value["old"]] = value["new"]
                    elif isinstance(value, str):
                        flat_replacements[key] = value

            self.replacements = flat_replacements
            print(f"  ✅ Loaded {len(self.replacements)} field replacements")
            return True
        except Exception as e:
            print(f"  ❌ Failed: {str(e)}")
            self.injection_log["errors"].append(f"Replacements load failed: {str(e)}")
            return False

    def _extract_sections(self):
        """Extract section headings and their content ranges from template."""
        sections = {}
        current_section = None
        current_section_heading = None

        for para_idx, para in enumerate(self.doc.paragraphs):
            is_heading = para.style and para.style.name and "Heading" in para.style.name

            if is_heading:
                # Save previous section
                if current_section:
                    sections[current_section_heading] = current_section

                # Start new section
                current_section_heading = para.text
                current_section = {"start": para_idx, "heading_para": para}
            elif current_section:
                current_section["end"] = para_idx

        # Save last section
        if current_section:
            sections[current_section_heading] = current_section

        print(f"  ✅ Extracted {len(sections)} sections from template")
        return sections

    def _inject_content(self, sections):
        """Inject markdown content into sections."""
        try:
            # For each markdown section, find matching DOCX section and inject
            for section_id, content in self.markdown_sections.items():
                # Try to find matching section heading
                matched_heading = None
                for heading in sections.keys():
                    if section_id.lower() in heading.lower() or heading.lower() in section_id.lower():
                        matched_heading = heading
                        break

                if not matched_heading:
                    print(f"  ⚠️  No matching section found for: {section_id}")
                    continue

                # Inject content into this section
                section_info = sections[matched_heading]
                self._inject_section_content(section_info, content, section_id)

                self.injection_log["statistics"]["sections_regenerated"] += 1

            # Apply field replacements to all paragraphs and tables
            self._apply_field_replacements()

            return True
        except Exception as e:
            print(f"  ❌ Injection failed: {str(e)}")
            self.injection_log["errors"].append(f"Content injection failed: {str(e)}")
            return False

    def _inject_section_content(self, section_info, markdown_content, section_id):
        """Inject markdown content into a specific section."""
        try:
            # Parse markdown lines
            lines = markdown_content.split("\n")

            # Get section boundaries
            start_para_idx = section_info["start"]
            end_para_idx = section_info.get("end", len(self.doc.paragraphs) - 1)

            # Keep the heading, start replacing from the next paragraph
            insert_idx = start_para_idx + 1

            # Remove old content (but keep heading)
            for _ in range(insert_idx, end_para_idx):
                if insert_idx < len(self.doc.paragraphs):
                    p = self.doc.paragraphs[insert_idx]
                    # Remove paragraph by clearing its content
                    pPr = p._element.get_or_add_pPr()
                    pPr.getparent().remove(p._element)

            # Insert new content
            for line in lines:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                # Determine paragraph style based on markdown markers
                if line.startswith("- "):
                    style = "List Bullet"
                    text = line[2:].strip()
                elif line.startswith("* "):
                    style = "List Bullet"
                    text = line[2:].strip()
                else:
                    style = "Body Text"
                    text = line

                # Create new paragraph with appropriate style
                new_para = self.doc.paragraphs[insert_idx - 1]._element
                new_para_elem = self.doc.add_paragraph(text, style=style)._element
                new_para.addprevious(new_para_elem)

            self.injection_log["injections"].append(
                {
                    "section": section_id,
                    "matched_heading": section_info.get("matched_heading", section_id),
                    "status": "SUCCESS",
                    "lines_inserted": len([l for l in lines if l.strip() and not l.startswith("#")]),
                }
            )
            print(f"  ✅ Injected: {section_id}")

        except Exception as e:
            self.injection_log["errors"].append(f"Section injection failed for {section_id}: {str(e)}")
            self.injection_log["injections"].append({"section": section_id, "status": "FAILED", "error": str(e)})
            print(f"  ❌ Failed to inject {section_id}: {str(e)}")

    def _apply_field_replacements(self):
        """Apply VARIABLE and ADAPTIVE field replacements."""
        replacement_count = 0

        # Replace in all paragraphs
        for para in self.doc.paragraphs:
            for run in para.runs:
                original_text = run.text
                modified_text = original_text

                for old_val, new_val in self.replacements.items():
                    if old_val in modified_text:
                        modified_text = modified_text.replace(old_val, new_val)

                        if modified_text != original_text:
                            replacement_count += 1
                            self.injection_log["replacements_applied"].append({"old": old_val, "new": new_val, "location": "paragraph"})

                if modified_text != original_text:
                    run.text = modified_text

        # Replace in all table cells
        for table in self.doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for para in cell.paragraphs:
                        for run in para.runs:
                            original_text = run.text
                            modified_text = original_text

                            for old_val, new_val in self.replacements.items():
                                if old_val in modified_text:
                                    modified_text = modified_text.replace(old_val, new_val)

                            if modified_text != original_text:
                                run.text = modified_text
                                replacement_count += 1

        self.injection_log["statistics"]["fields_replaced"] = replacement_count
        print(f"  ✅ Applied {replacement_count} field replacements")

    def _save_document(self):
        """Save modified document."""
        try:
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
            self.doc.save(self.output_path)
            print(f"  ✅ Saved: {self.output_path}")

            # Save injection log
            if self.log_path:
                with open(self.log_path, "w", encoding="utf-8") as f:
                    json.dump(self.injection_log, f, indent=2, ensure_ascii=False)
                print(f"  ✅ Saved: {self.log_path}")

            return True
        except Exception as e:
            print(f"  ❌ Failed: {str(e)}")
            self.injection_log["errors"].append(f"Save failed: {str(e)}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Inject markdown content into charter DOCX template",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python docx_injector.py \\
    --template template.docx \\
    --content charter_draft_approved.md \\
    --replacements replacements.json \\
    --output Final_Charter.docx \\
    --log injection_log.json
        """,
    )
    parser.add_argument("--template", required=True, help="Path to template DOCX")
    parser.add_argument("--content", required=True, help="Path to approved markdown content")
    parser.add_argument("--replacements", required=True, help="Path to field replacements JSON")
    parser.add_argument("--output", required=True, help="Path to output DOCX")
    parser.add_argument("--log", help="Path to save injection log JSON")

    args = parser.parse_args()

    # Validate inputs
    for path_arg, label in [("template", args.template), ("content", args.content), ("replacements", args.replacements)]:
        if not Path(args.__dict__[path_arg]).exists():
            print(f"ERROR: {label} not found: {args.__dict__[path_arg]}")
            return 1

    # Run injector
    injector = DocxInjector(args.template, args.content, args.replacements, args.output, args.log)
    success = injector.inject()

    # Print summary
    print("\n" + "=" * 70)
    if success:
        stats = injector.injection_log["statistics"]
        print(f"✓ Injection completed successfully")
        print(f"  Sections regenerated: {stats['sections_regenerated']}")
        print(f"  Fields replaced: {stats['fields_replaced']}")
        print(f"  Output: {args.output}")
        if args.log:
            print(f"  Log: {args.log}")
    else:
        print(f"✗ Injection failed")
        print(f"  Errors: {len(injector.injection_log['errors'])}")
        for error in injector.injection_log["errors"]:
            print(f"    - {error}")
    print("=" * 70)

    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
