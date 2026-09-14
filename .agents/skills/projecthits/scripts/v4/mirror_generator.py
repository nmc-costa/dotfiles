"""
mirror_generator.py - projectHITs v4 Mirror Generation Helper

Generate exact-structure mirrors of templates in editable format
(default: Markdown, or LaTeX/TXT per director choice).

Mirrors replicate 100% of structure (headings, tables, sections)
with zero content (only placeholders).

Usage:
    python mirror_generator.py <template_path> [--format markdown|latex|text] [--output output.md]

Output:
    Mirror file in requested format + mirror_analysis.json (structure map)
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
import re
from template_analyzer import TemplateAnalyzer


class MirrorGenerator:
    """Generate editable mirrors from templates."""
    
    def __init__(self, template_path: str, editable_format: str = 'markdown'):
        self.template_path = Path(template_path)
        self.editable_format = editable_format.lower()
        self.analyzer = TemplateAnalyzer(template_path)
        self.analysis = self.analyzer.analyze()
        self.mirror_content = ""
        self.structure_map = {}
        
    def generate(self) -> str:
        """Generate mirror based on template format and editable format."""
        if self.analysis['format'] == 'docx':
            self.mirror_content = self._generate_from_docx()
        elif self.analysis['format'] == 'latex':
            self.mirror_content = self._generate_from_latex()
        elif self.analysis['format'] == 'markdown':
            self.mirror_content = self._generate_from_markdown()
        elif self.analysis['format'] == 'pdf':
            self.mirror_content = self._generate_from_pdf()
        elif self.analysis['format'] == 'text':
            self.mirror_content = self._generate_from_text()
        
        return self.mirror_content
    
    def _generate_from_docx(self) -> str:
        """Generate mirror from DOCX (output in editable format)."""
        content = self.analyzer.content
        
        if self.editable_format == 'markdown':
            return self._docx_to_markdown(content)
        elif self.editable_format == 'latex':
            return self._docx_to_latex(content)
        else:
            return self._docx_to_text(content)
    
    def _docx_to_markdown(self, content: Dict) -> str:
        """Convert DOCX structure to Markdown mirror."""
        lines = []
        
        # Header with metadata
        lines.append(f"# Project Document (Mirrored from DOCX)")
        lines.append("")
        lines.append("*This is a structure-only mirror. Replace placeholders with actual content.*")
        lines.append("")
        
        if content['metadata'].get('title'):
            lines.append(f"**Template Title:** {content['metadata']['title']}")
        if content['metadata'].get('author'):
            lines.append(f"**Template Author:** {content['metadata']['author']}")
        lines.append("")
        
        # Process paragraphs
        heading_map = {}
        section_idx = 1
        
        for para in content['paragraphs']:
            text = para['text'].strip()
            style = para['style']
            
            if not text:
                continue
            
            # Detect headings and replicate hierarchy
            if 'Heading 1' in style:
                lines.append(f"\n# {text}")
                self.structure_map[section_idx] = {'type': 'heading1', 'text': text, 'line': len(lines)}
                section_idx += 1
            elif 'Heading 2' in style:
                lines.append(f"\n## {text}")
                self.structure_map[section_idx] = {'type': 'heading2', 'text': text, 'line': len(lines)}
                section_idx += 1
            elif 'Heading 3' in style:
                lines.append(f"\n### {text}")
                self.structure_map[section_idx] = {'type': 'heading3', 'text': text, 'line': len(lines)}
                section_idx += 1
            elif 'Title' in style or 'Subtitle' in style:
                pass  # Skip title/subtitle (already in header)
            elif text:
                # Regular paragraph → placeholder
                lines.append("")
                lines.append(f"[Content: {text[:50]}...]")
        
        # Add tables
        if content['tables']:
            lines.append("\n\n## Tables\n")
            for table_idx, table in enumerate(content['tables']):
                lines.append(f"\n### Table {table_idx + 1}")
                lines.append("")
                
                # Create markdown table structure
                cols = table['cols']
                rows = table['rows']
                
                # Header row
                header = "| " + " | ".join([f"Col {i+1}" for i in range(cols)]) + " |"
                separator = "| " + " | ".join(["---" for _ in range(cols)]) + " |"
                
                lines.append(header)
                lines.append(separator)
                
                # Content rows
                for row_idx in range(rows):
                    if row_idx < len(table['content']):
                        row_cells = table['content'][row_idx]
                        row_content = [cell if cell else "[Content]" for cell in row_cells]
                        row = "| " + " | ".join(row_content[:cols]) + " |"
                        lines.append(row)
                    else:
                        lines.append("| " + " | ".join(["[Content]" for _ in range(cols)]) + " |")
        
        return "\n".join(lines)
    
    def _docx_to_latex(self, content: Dict) -> str:
        """Convert DOCX structure to LaTeX mirror."""
        lines = [
            r"\documentclass{article}",
            r"\usepackage[utf-8]{inputenc}",
            r"\title{Mirrored Document}",
            r"\author{}",
            r"\date{}",
            r"\begin{document}",
            r"\maketitle",
            "",
        ]
        
        section_idx = 1
        for para in content['paragraphs']:
            text = para['text'].strip()
            style = para['style']
            
            if not text:
                continue
            
            if 'Heading 1' in style:
                lines.append(f"\\section{{{text}}}")
                self.structure_map[section_idx] = {'type': 'section', 'text': text}
                section_idx += 1
            elif 'Heading 2' in style:
                lines.append(f"\\subsection{{{text}}}")
                self.structure_map[section_idx] = {'type': 'subsection', 'text': text}
                section_idx += 1
            elif 'Heading 3' in style:
                lines.append(f"\\subsubsection{{{text}}}")
                self.structure_map[section_idx] = {'type': 'subsubsection', 'text': text}
                section_idx += 1
            elif text:
                lines.append(f"\n[Content: {text[:40]}...]")
        
        # Add tables
        if content['tables']:
            lines.append("\n\\section{Tables}\n")
            for table_idx, table in enumerate(content['tables']):
                lines.append(f"\\subsection{{Table {table_idx + 1}}}")
                lines.append(f"\\begin{{tabular}}{{{'|'.join(['c'] * table['cols'])}}}")
                lines.append(" \\hline")
                
                # Header row
                header = " & ".join([f"Col {i+1}" for i in range(table['cols'])]) + " \\\\"
                lines.append(header)
                lines.append(" \\hline")
                
                # Content rows
                for row_idx in range(table['rows']):
                    row_content = " & ".join(["[Content]" for _ in range(table['cols'])])
                    lines.append(row_content + " \\\\")
                
                lines.append(" \\hline")
                lines.append("\\end{tabular}\n")
        
        lines.append(r"\end{document}")
        return "\n".join(lines)
    
    def _docx_to_text(self, content: Dict) -> str:
        """Convert DOCX structure to plain text mirror."""
        lines = []
        lines.append("=" * 60)
        lines.append("PROJECT DOCUMENT (Structure Mirror)")
        lines.append("=" * 60)
        lines.append("")
        
        section_idx = 1
        for para in content['paragraphs']:
            text = para['text'].strip()
            style = para['style']
            
            if not text:
                continue
            
            if 'Heading 1' in style:
                lines.append("")
                lines.append(text.upper())
                lines.append("=" * len(text))
                self.structure_map[section_idx] = {'type': 'section', 'text': text}
                section_idx += 1
            elif 'Heading 2' in style:
                lines.append("")
                lines.append(text)
                lines.append("-" * len(text))
                self.structure_map[section_idx] = {'type': 'subsection', 'text': text}
                section_idx += 1
            elif 'Heading 3' in style:
                lines.append("")
                lines.append(f"• {text}")
                self.structure_map[section_idx] = {'type': 'subsubsection', 'text': text}
                section_idx += 1
            elif text:
                lines.append(f"[Content: {text}]")
        
        if content['tables']:
            lines.append("\n" + "=" * 60)
            lines.append("TABLES")
            lines.append("=" * 60)
            for table_idx, table in enumerate(content['tables']):
                lines.append(f"\nTable {table_idx + 1} ({table['rows']} rows × {table['cols']} cols)")
                lines.append("[Content: Table data]")
        
        return "\n".join(lines)
    
    def _generate_from_latex(self) -> str:
        """Generate mirror from LaTeX."""
        content = self.analyzer.content
        
        if self.editable_format == 'markdown':
            return self._latex_to_markdown(content)
        else:
            return self._latex_to_text(content)
    
    def _latex_to_markdown(self, content: Dict) -> str:
        """Convert LaTeX structure to Markdown mirror."""
        lines = ["# Mirrored Document (from LaTeX)\n"]
        
        section_map = {
            'chapter': '# ',
            'section': '# ',
            'subsection': '## ',
            'subsubsection': '### ',
        }
        
        for section in content['sections']:
            level = section['level']
            title = section['title']
            prefix = section_map.get(level, '# ')
            lines.append(f"{prefix}{title}\n")
            lines.append(f"[Content: {title} content]\n")
        
        return "\n".join(lines)
    
    def _latex_to_text(self, content: Dict) -> str:
        """Convert LaTeX structure to plain text mirror."""
        lines = ["=" * 60, "MIRRORED DOCUMENT (from LaTeX)", "=" * 60, ""]
        
        for section in content['sections']:
            title = section['title']
            lines.append(f"\n{title}")
            lines.append("-" * len(title))
            lines.append(f"[Content: {title} content]")
        
        return "\n".join(lines)
    
    def _generate_from_markdown(self) -> str:
        """Generate mirror from Markdown."""
        with open(self.template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract heading structure and replicate
        lines = []
        lines.append("# Document Mirror (from Markdown)\n")
        
        # Parse headings
        heading_pattern = r'^(#{1,6})\s+(.+)$'
        for match in re.finditer(heading_pattern, content, re.MULTILINE):
            prefix = match.group(1)
            title = match.group(2)
            lines.append(f"{prefix} {title}")
            lines.append(f"[Content: {title}]\n")
        
        return "\n".join(lines)
    
    def _generate_from_pdf(self) -> str:
        """Generate mirror from PDF (best-effort)."""
        lines = [
            "# Document Mirror (from PDF)\n",
            "[Content: Extracted from PDF]\n",
            f"**Pages:** {self.analysis['pages']}",
        ]
        
        if self.analysis['table_count'] > 0:
            lines.append(f"**Tables:** {self.analysis['table_count']}")
        
        return "\n".join(lines)
    
    def _generate_from_text(self) -> str:
        """Generate mirror from plain text."""
        with open(self.template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if self.editable_format == 'markdown':
            lines = ["# Mirrored Document (from Text)\n"]
            for section in self.analysis['sections']:
                lines.append(f"## {section}\n")
                lines.append("[Content: Section content]\n")
            return "\n".join(lines)
        else:
            return content  # Return as-is for text format
    
    def save(self, output_path: str = None):
        """Save mirror to file."""
        if not output_path:
            stem = self.template_path.stem
            ext = '.md' if self.editable_format == 'markdown' else \
                  '.tex' if self.editable_format == 'latex' else '.txt'
            output_path = f"{stem}_mirror{ext}"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(self.mirror_content)
        
        print(f"✅ Mirror saved to {output_path}")
        return output_path
    
    def save_structure_map(self, output_path: str = None):
        """Save structure map as JSON."""
        if not output_path:
            stem = self.template_path.stem
            output_path = f"{stem}_mirror_analysis.json"
        
        data = {
            'template_path': str(self.template_path),
            'template_format': self.analysis['format'],
            'editable_format': self.editable_format,
            'structure_map': self.structure_map,
            'analysis': self.analysis,
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"✅ Structure map saved to {output_path}")
        return output_path


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    template_path = sys.argv[1]
    editable_format = 'markdown'
    output_path = None
    
    if '--format' in sys.argv:
        idx = sys.argv.index('--format')
        if idx + 1 < len(sys.argv):
            editable_format = sys.argv[idx + 1]
    
    if '--output' in sys.argv:
        idx = sys.argv.index('--output')
        if idx + 1 < len(sys.argv):
            output_path = sys.argv[idx + 1]
    
    try:
        generator = MirrorGenerator(template_path, editable_format)
        
        print(f"\n🪞 Generating Mirror")
        print(f"Template: {template_path}")
        print(f"Format: {editable_format}")
        
        mirror_content = generator.generate()
        mirror_file = generator.save(output_path)
        generator.save_structure_map()
        
        print(f"\n📊 Mirror Analysis:")
        print(f"Sections: {len(generator.structure_map)}")
        print(f"Template Format: {generator.analysis['format']}")
        print(f"Editable Format: {generator.editable_format}")
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
