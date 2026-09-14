"""
template_analyzer.py - projectHITs v4 Template Analysis Helper

Parse templates in any format (DOCX, LaTeX, Markdown, PDF, TXT) and extract
structure information (sections, tables, fields) for mirror generation.

Usage:
    python template_analyzer.py <template_path> [--output output.json]

Output:
    JSON with keys: format, sections, tables, fields, metadata, structure_map
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
import re


class TemplateAnalyzer:
    """Analyze templates across multiple formats."""
    
    def __init__(self, template_path: str):
        self.template_path = Path(template_path)
        self.format = self._detect_format()
        self.content = self._read_template()
        self.analysis = {}
        
    def _detect_format(self) -> str:
        """Detect template format from file extension."""
        ext = self.template_path.suffix.lower()
        format_map = {
            '.docx': 'docx',
            '.doc': 'docx',
            '.tex': 'latex',
            '.md': 'markdown',
            '.markdown': 'markdown',
            '.pdf': 'pdf',
            '.txt': 'text',
        }
        return format_map.get(ext, 'unknown')
    
    def _read_template(self) -> Any:
        """Read template content based on format."""
        if self.format == 'docx':
            return self._read_docx()
        elif self.format == 'latex':
            return self._read_latex()
        elif self.format == 'markdown':
            return self._read_markdown()
        elif self.format == 'pdf':
            return self._read_pdf()
        elif self.format == 'text':
            return self._read_text()
        else:
            raise ValueError(f"Unsupported format: {self.format}")
    
    def _read_docx(self) -> Dict:
        """Extract structure from DOCX file."""
        try:
            from docx import Document
        except ImportError:
            raise ImportError("python-docx required: pip install python-docx")
        
        doc = Document(self.template_path)
        result = {
            'paragraphs': [],
            'tables': [],
            'metadata': self._extract_docx_metadata(doc),
        }
        
        for para in doc.paragraphs:
            result['paragraphs'].append({
                'text': para.text,
                'style': para.style.name,
                'level': para.paragraph_format.outline_level if hasattr(para.paragraph_format, 'outline_level') else None,
            })
        
        for table_idx, table in enumerate(doc.tables):
            result['tables'].append({
                'index': table_idx,
                'rows': len(table.rows),
                'cols': len(table.columns),
                'content': [[cell.text for cell in row.cells] for row in table.rows],
            })
        
        return result
    
    def _read_latex(self) -> Dict:
        """Extract structure from LaTeX file."""
        with open(self.template_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        result = {
            'raw': content,
            'sections': [],
            'environments': [],
        }
        
        # Extract sections/subsections/subsubsections
        section_pattern = r'\\(chapter|section|subsection|subsubsection)\*?\{([^}]+)\}'
        for match in re.finditer(section_pattern, content):
            result['sections'].append({
                'level': match.group(1),
                'title': match.group(2),
            })
        
        # Extract environments (tables, figures, etc.)
        env_pattern = r'\\begin\{(\w+)\}'
        for match in re.finditer(env_pattern, content):
            result['environments'].append(match.group(1))
        
        return result
    
    def _read_markdown(self) -> Dict:
        """Extract structure from Markdown file."""
        with open(self.template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        result = {
            'raw': content,
            'headings': [],
            'tables': [],
        }
        
        # Extract headings
        heading_pattern = r'^(#{1,6})\s+(.+)$'
        for match in re.finditer(heading_pattern, content, re.MULTILINE):
            result['headings'].append({
                'level': len(match.group(1)),
                'title': match.group(2),
            })
        
        # Extract tables (markdown table syntax)
        table_pattern = r'\|(.+)\|'
        tables = re.findall(table_pattern, content)
        result['tables'] = [{'cols': len(t.split('|')) - 2} for t in tables if t]
        
        return result
    
    def _read_pdf(self) -> Dict:
        """Extract structure from PDF file (best-effort)."""
        try:
            import pdfplumber
        except ImportError:
            raise ImportError("pdfplumber required: pip install pdfplumber")
        
        result = {
            'pages': 0,
            'tables': [],
            'text_blocks': [],
        }
        
        with pdfplumber.open(self.template_path) as pdf:
            result['pages'] = len(pdf.pages)
            for page_idx, page in enumerate(pdf.pages):
                tables = page.extract_tables()
                if tables:
                    for table in tables:
                        result['tables'].append({
                            'page': page_idx,
                            'rows': len(table),
                            'cols': len(table[0]) if table else 0,
                        })
        
        return result
    
    def _read_text(self) -> Dict:
        """Extract structure from plain text file."""
        with open(self.template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        result = {
            'raw': content,
            'lines': len(content.split('\n')),
        }
        
        # Heuristic: look for section delimiters (===, ---, etc.)
        section_pattern = r'^([A-Z][A-Z\s]+)\n(={3,}|-{3,}|_{3,})'
        result['sections'] = [match.group(1).strip() for match in re.finditer(section_pattern, content, re.MULTILINE)]
        
        return result
    
    def _extract_docx_metadata(self, doc) -> Dict:
        """Extract metadata from DOCX document."""
        props = doc.core_properties
        return {
            'title': props.title or '',
            'author': props.author or '',
            'subject': props.subject or '',
            'created': str(props.created) if props.created else None,
            'modified': str(props.modified) if props.modified else None,
        }
    
    def analyze(self) -> Dict[str, Any]:
        """Perform complete analysis and return structured output."""
        if self.format == 'docx':
            self.analysis = self._analyze_docx()
        elif self.format == 'latex':
            self.analysis = self._analyze_latex()
        elif self.format == 'markdown':
            self.analysis = self._analyze_markdown()
        elif self.format == 'pdf':
            self.analysis = self._analyze_pdf()
        elif self.format == 'text':
            self.analysis = self._analyze_text()
        
        return self.analysis
    
    def _analyze_docx(self) -> Dict[str, Any]:
        """Analyze DOCX structure."""
        content = self.content
        
        # Extract heading hierarchy
        sections = []
        current_hierarchy = []
        
        for para in content['paragraphs']:
            style = para['style']
            if 'Heading' in style:
                level = int(style.replace('Heading ', '')) if 'Heading' in style else 1
                title = para['text']
                sections.append({
                    'level': level,
                    'title': title,
                    'type': 'heading',
                })
        
        return {
            'format': 'docx',
            'total_paragraphs': len(content['paragraphs']),
            'total_tables': len(content['tables']),
            'sections': sections,
            'tables': content['tables'],
            'metadata': content['metadata'],
            'field_count': len([p for p in content['paragraphs'] if '[' in p['text'] and ']' in p['text']]),
        }
    
    def _analyze_latex(self) -> Dict[str, Any]:
        """Analyze LaTeX structure."""
        content = self.content
        
        return {
            'format': 'latex',
            'section_count': len(content['sections']),
            'sections': content['sections'],
            'environments': list(set(content['environments'])),
            'environment_count': len(set(content['environments'])),
            'total_lines': len(content['raw'].split('\n')),
        }
    
    def _analyze_markdown(self) -> Dict[str, Any]:
        """Analyze Markdown structure."""
        content = self.content
        
        return {
            'format': 'markdown',
            'heading_count': len(content['headings']),
            'headings': content['headings'],
            'table_count': len(content['tables']),
            'tables': content['tables'],
            'total_lines': len(content['raw'].split('\n')),
        }
    
    def _analyze_pdf(self) -> Dict[str, Any]:
        """Analyze PDF structure."""
        content = self.content
        
        return {
            'format': 'pdf',
            'pages': content['pages'],
            'table_count': len(content['tables']),
            'tables': content['tables'],
        }
    
    def _analyze_text(self) -> Dict[str, Any]:
        """Analyze plain text structure."""
        content = self.content
        
        return {
            'format': 'text',
            'total_lines': content['lines'],
            'estimated_sections': len(content['sections']),
            'sections': content['sections'],
        }
    
    def to_json(self) -> str:
        """Export analysis as JSON."""
        return json.dumps(self.analysis, indent=2, default=str)
    
    def save(self, output_path: str):
        """Save analysis to JSON file."""
        with open(output_path, 'w') as f:
            f.write(self.to_json())
        print(f"Analysis saved to {output_path}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    template_path = sys.argv[1]
    output_path = None
    
    if '--output' in sys.argv:
        idx = sys.argv.index('--output')
        if idx + 1 < len(sys.argv):
            output_path = sys.argv[idx + 1]
    
    try:
        analyzer = TemplateAnalyzer(template_path)
        analysis = analyzer.analyze()
        
        print(f"\n📋 Template Analysis: {template_path}")
        print(f"Format: {analysis['format']}")
        
        # Summary
        if 'section_count' in analysis:
            print(f"Sections: {analysis['section_count']}")
        elif 'heading_count' in analysis:
            print(f"Headings: {analysis['heading_count']}")
        elif 'estimated_sections' in analysis:
            print(f"Estimated Sections: {analysis['estimated_sections']}")
        
        if 'table_count' in analysis:
            print(f"Tables: {analysis['table_count']}")
        elif 'total_tables' in analysis:
            print(f"Tables: {analysis['total_tables']}")
        
        print("\n" + json.dumps(analysis, indent=2, default=str))
        
        if output_path:
            analyzer.save(output_path)
    
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
