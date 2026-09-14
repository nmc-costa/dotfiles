"""
auto_filler.py - projectHITs v4 Auto-fill Helper

Parse project briefs (text, JSON, email) and intelligently fill mirror files
with VARIABLE, ADAPTIVE, and REGENERATE content. Marks unknown/incomplete
sections with embedded [TODO] tags.

Usage:
    python auto_filler.py <mirror_path> <brief_path> [--output output.md]

Input:
    mirror_path: Path to mirror file (.md, .tex, .txt)
    brief_path: Path to project brief (text, JSON, email)

Output:
    Filled mirror + fill_mapping.json (what was filled, confidence scores)
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any
from datetime import datetime


class BriefParser:
    """Parse project briefs in various formats."""
    
    def __init__(self, brief_path: str):
        self.brief_path = Path(brief_path)
        self.format = self._detect_format()
        self.content = self._read_brief()
        self.extracted_data = {}
    
    def _detect_format(self) -> str:
        """Detect brief format."""
        ext = self.brief_path.suffix.lower()
        if ext == '.json':
            return 'json'
        elif ext == '.txt':
            return 'text'
        elif ext == '.md':
            return 'markdown'
        elif ext == '.eml':
            return 'email'
        else:
            return 'text'
    
    def _read_brief(self) -> Any:
        """Read brief content."""
        if self.format == 'json':
            with open(self.brief_path, 'r') as f:
                return json.load(f)
        else:
            with open(self.brief_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
    
    def extract_entities(self) -> Dict[str, Any]:
        """Extract structured entities from brief."""
        if self.format == 'json':
            return self._extract_from_json()
        else:
            return self._extract_from_text()
    
    def _extract_from_json(self) -> Dict[str, Any]:
        """Extract from JSON brief."""
        data = self.content
        extracted = {
            'project': data.get('project', {}).get('name', ''),
            'description': data.get('project', {}).get('description', ''),
            'start_date': data.get('timeline', {}).get('start_date', ''),
            'end_date': data.get('timeline', {}).get('end_date', ''),
            'budget': data.get('budget', {}).get('total', ''),
            'team': data.get('team', {}),
            'objectives': data.get('objectives', []),
            'scope': data.get('scope', ''),
            'risks': data.get('risks', []),
            'success_criteria': data.get('success_criteria', []),
            'stakeholders': data.get('stakeholders', []),
        }
        return extracted
    
    def _extract_from_text(self) -> Dict[str, Any]:
        """Extract entities from text brief using regex patterns."""
        text = self.content
        extracted = {}
        
        # Project name
        project_pattern = r'(?:project\s*:?|title\s*:?|name\s*:?)\s*([^\n]+)'
        match = re.search(project_pattern, text, re.IGNORECASE)
        extracted['project'] = match.group(1).strip() if match else ''
        
        # Description
        desc_pattern = r'(?:description|overview)\s*:?\s*([^\n]+(?:\n[^\n]+)*?)(?:\n\n|\n[A-Z]|$)'
        match = re.search(desc_pattern, text, re.IGNORECASE)
        extracted['description'] = match.group(1).strip() if match else ''
        
        # Timeline
        start_pattern = r'(?:start|begin)\s*(?:date|on)?\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|[A-Za-z]+\s*\d{1,2}(?:st|nd|rd|th)?,?\s*\d{4})'
        match = re.search(start_pattern, text, re.IGNORECASE)
        extracted['start_date'] = match.group(1).strip() if match else ''
        
        end_pattern = r'(?:end|due|completion|finish)\s*(?:date|on)?\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|[A-Za-z]+\s*\d{1,2}(?:st|nd|rd|th)?,?\s*\d{4})'
        match = re.search(end_pattern, text, re.IGNORECASE)
        extracted['end_date'] = match.group(1).strip() if match else ''
        
        # Budget
        budget_pattern = r'(?:budget|cost|investment)\s*:?\s*(?:\$|€|£)?\s*([0-9,]+(?:\.[0-9]{2})?)'
        match = re.search(budget_pattern, text, re.IGNORECASE)
        extracted['budget'] = match.group(1).strip() if match else ''
        
        # Team members
        team_pattern = r'(?:team|members|staff|personnel)\s*:?\s*([^\n]+(?:\n[^\n]+)*?)(?:\n\n|\n[A-Z]|$)'
        match = re.search(team_pattern, text, re.IGNORECASE)
        extracted['team'] = match.group(1).strip() if match else ''
        
        # Objectives/Goals
        objectives_pattern = r'(?:objective|goal|aim|target)s?\s*:?\s*([^\n]+(?:\n[^\n]+)*?)(?:\n\n|\n[A-Z]|$)'
        match = re.search(objectives_pattern, text, re.IGNORECASE)
        extracted['objectives'] = match.group(1).strip() if match else ''
        
        # Scope
        scope_pattern = r'(?:scope|included|deliverable)s?\s*:?\s*([^\n]+(?:\n[^\n]+)*?)(?:\n\n|\n[A-Z]|$)'
        match = re.search(scope_pattern, text, re.IGNORECASE)
        extracted['scope'] = match.group(1).strip() if match else ''
        
        # Risks
        risk_pattern = r'(?:risk|threat|issue)s?\s*:?\s*([^\n]+(?:\n[^\n]+)*?)(?:\n\n|\n[A-Z]|$)'
        match = re.search(risk_pattern, text, re.IGNORECASE)
        extracted['risks'] = match.group(1).strip() if match else ''
        
        # Success metrics
        metric_pattern = r'(?:success\s*(?:criteria|metric)|kpi|measurement)s?\s*:?\s*([^\n]+(?:\n[^\n]+)*?)(?:\n\n|\n[A-Z]|$)'
        match = re.search(metric_pattern, text, re.IGNORECASE)
        extracted['success_criteria'] = match.group(1).strip() if match else ''
        
        # Stakeholders
        stakeholder_pattern = r'(?:stakeholder)s?\s*:?\s*([^\n]+(?:\n[^\n]+)*?)(?:\n\n|\n[A-Z]|$)'
        match = re.search(stakeholder_pattern, text, re.IGNORECASE)
        extracted['stakeholders'] = match.group(1).strip() if match else ''
        
        return extracted
    
    def get_extracted_data(self) -> Dict[str, Any]:
        """Get all extracted data."""
        if not self.extracted_data:
            self.extracted_data = self.extract_entities()
        return self.extracted_data


class MirrorFiller:
    """Fill mirror files with data from project briefs."""
    
    def __init__(self, mirror_path: str, brief_path: str):
        self.mirror_path = Path(mirror_path)
        with open(self.mirror_path, 'r', encoding='utf-8') as f:
            self.mirror_content = f.read()
        
        self.parser = BriefParser(brief_path)
        self.brief_data = self.parser.get_extracted_data()
        
        self.filled_content = self.mirror_content
        self.fill_mapping = {}
        self.completion_status = {}
    
    def fill(self) -> str:
        """Fill mirror with brief data."""
        # Define section patterns and their corresponding brief data
        fills = [
            (r'(## Project|# Executive Summary|## Scope)(.*?)\n\n(?=##|$)',
             'scope', 'ADAPTIVE'),
            
            (r'(## Objectives|### Objectives)(.*?)\n\n(?=##|$)',
             'objectives', 'VARIABLE'),
            
            (r'(## Team|### Team Structure|## Resources)(.*?)\n\n(?=##|$)',
             'team', 'VARIABLE'),
            
            (r'(## Budget|### Budget Overview)(.*?)\n\n(?=##|$)',
             'budget', 'VARIABLE'),
            
            (r'(## Timeline|### Timeline|## Schedule)(.*?)\n\n(?=##|$)',
             'start_date,end_date', 'VARIABLE'),
            
            (r'(## Risks|### Risks?|## Risk Assessment)(.*?)\n\n(?=##|$)',
             'risks', 'ADAPTIVE'),
            
            (r'(## Success|### Success Criteria|## KPI|## Metrics)(.*?)\n\n(?=##|$)',
             'success_criteria', 'ADAPTIVE'),
            
            (r'(## Stakeholders|### Stakeholders?)(.*?)\n\n(?=##|$)',
             'stakeholders', 'VARIABLE'),
        ]
        
        for pattern, brief_key, field_type in fills:
            confidence = self._fill_section(pattern, brief_key, field_type)
            if brief_key not in self.fill_mapping:
                self.fill_mapping[brief_key] = {
                    'confidence': confidence,
                    'type': field_type,
                    'status': 'filled' if confidence > 50 else 'partial',
                }
        
        return self.filled_content
    
    def _fill_section(self, pattern: str, brief_key: str, field_type: str) -> float:
        """Fill a section and return confidence score."""
        if brief_key not in self.brief_data or not self.brief_data[brief_key]:
            # Mark as TODO if data not available
            replacement = r'\1\n\n[TODO: Provide ' + brief_key.replace('_', ' ') + ' information]'
            self.filled_content = re.sub(pattern, replacement, self.filled_content, flags=re.DOTALL)
            return 0.0
        
        data = self.brief_data[brief_key]
        
        # Determine confidence based on data quality
        confidence = self._calculate_confidence(data, field_type)
        
        # Build replacement content
        if isinstance(data, (list, dict)):
            content_str = self._format_complex_data(data)
        else:
            content_str = str(data)
        
        if confidence < 50:
            # Low confidence: add review marker
            replacement = r'\1\n\n' + content_str + f'\n\n[REVIEW: Confidence {confidence:.0f}%. Please verify and adjust as needed.]'
        else:
            replacement = r'\1\n\n' + content_str
        
        self.filled_content = re.sub(pattern, replacement, self.filled_content, flags=re.DOTALL)
        return confidence
    
    def _calculate_confidence(self, data: Any, field_type: str) -> float:
        """Calculate confidence score for filled data."""
        if not data:
            return 0.0
        
        base_confidence = 85.0 if field_type == 'VARIABLE' else 70.0
        
        # Reduce confidence if data is short/incomplete
        if isinstance(data, str):
            if len(data) < 10:
                base_confidence -= 20
            elif len(data) < 50:
                base_confidence -= 10
        elif isinstance(data, (list, dict)):
            if len(data) == 0:
                base_confidence -= 30
            elif len(data) == 1:
                base_confidence -= 15
        
        return max(0.0, min(100.0, base_confidence))
    
    def _format_complex_data(self, data: Any) -> str:
        """Format complex data (lists, dicts) as readable text."""
        if isinstance(data, list):
            return "\n".join([f"- {item}" for item in data if item])
        elif isinstance(data, dict):
            return "\n".join([f"**{k}:** {v}" for k, v in data.items() if v])
        return str(data)
    
    def mark_remaining_todos(self) -> int:
        """Scan mirror for remaining placeholder sections and mark as TODOs."""
        todo_pattern = r'\[Content: ([^\]]+)\]'
        todos = re.findall(todo_pattern, self.filled_content)
        
        for todo in todos:
            old = f'[Content: {todo}]'
            new = f'[TODO: Provide information for: {todo}]'
            self.filled_content = self.filled_content.replace(old, new)
        
        return len(todos)
    
    def generate_completion_status(self) -> Dict[str, Any]:
        """Generate completion status report."""
        # Count sections
        sections = re.findall(r'^##\s+(.+)$', self.filled_content, re.MULTILINE)
        total_sections = len(sections)
        
        # Count TODOs
        todos = re.findall(r'\[TODO: ([^\]]+)\]', self.filled_content)
        incomplete_sections = len(todos)
        completed_sections = total_sections - incomplete_sections
        
        completion_percent = int((completed_sections / total_sections * 100)) if total_sections > 0 else 0
        
        self.completion_status = {
            'total_sections': total_sections,
            'completed': completed_sections,
            'incomplete': incomplete_sections,
            'completion_percent': completion_percent,
            'todos': todos,
            'fill_mapping': self.fill_mapping,
        }
        
        return self.completion_status
    
    def save_filled_mirror(self, output_path: str = None) -> str:
        """Save filled mirror to file."""
        if not output_path:
            stem = self.mirror_path.stem
            output_path = f"{stem}_filled.md"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(self.filled_content)
        
        print(f"✅ Filled mirror saved to {output_path}")
        return output_path
    
    def save_fill_mapping(self, output_path: str = None) -> str:
        """Save fill mapping and completion status as JSON."""
        if not output_path:
            stem = self.mirror_path.stem
            output_path = f"{stem}_fill_mapping.json"
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'mirror_file': str(self.mirror_path),
            'brief_data': self.brief_data,
            'fill_mapping': self.fill_mapping,
            'completion_status': self.completion_status,
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"✅ Fill mapping saved to {output_path}")
        return output_path


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    
    mirror_path = sys.argv[1]
    brief_path = sys.argv[2]
    output_path = None
    
    if '--output' in sys.argv:
        idx = sys.argv.index('--output')
        if idx + 1 < len(sys.argv):
            output_path = sys.argv[idx + 1]
    
    try:
        print(f"\n📝 Auto-filling Mirror")
        print(f"Mirror: {mirror_path}")
        print(f"Brief: {brief_path}")
        
        filler = MirrorFiller(mirror_path, brief_path)
        
        # Fill the mirror
        filler.fill()
        
        # Mark remaining placeholders as TODOs
        todos_marked = filler.mark_remaining_todos()
        
        # Generate completion status
        status = filler.generate_completion_status()
        
        # Save outputs
        filler.save_filled_mirror(output_path)
        filler.save_fill_mapping()
        
        # Print summary
        print(f"\n📊 Auto-fill Summary:")
        print(f"Total Sections: {status['total_sections']}")
        print(f"Completed: {status['completed']}/{status['total_sections']}")
        print(f"Completion: {status['completion_percent']}%")
        print(f"Missing Sections (TODOs): {status['incomplete']}")
        
        if status['todos']:
            print(f"\n❓ Missing Information:")
            for todo in status['todos'][:5]:  # Show first 5
                print(f"  - {todo}")
            if len(status['todos']) > 5:
                print(f"  ... and {len(status['todos']) - 5} more")
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
