"""
completion_checker.py - projectHITs v4 Completion Checker

Scan filled mirror files for [TODO] markers and generate completion
checklists with prioritized director asks.

Usage:
    python completion_checker.py <mirror_path> [--output output.md]

Output:
    completion_checklist.md (human-readable)
    completion_checklist.json (machine-readable)
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any
from datetime import datetime


class CompletionChecker:
    """Check mirror completion and generate checklists."""
    
    def __init__(self, mirror_path: str):
        self.mirror_path = Path(mirror_path)
        with open(self.mirror_path, 'r', encoding='utf-8') as f:
            self.mirror_content = f.read()
        
        self.sections = self._extract_sections()
        self.todos = self._extract_todos()
        self.completion_data = {}
    
    def _extract_sections(self) -> Dict[str, str]:
        """Extract all sections from mirror."""
        sections = {}
        
        # Pattern for markdown headers
        pattern = r'^(#{1,6})\s+(.+)$'
        matches = re.finditer(pattern, self.mirror_content, re.MULTILINE)
        
        for match in matches:
            level = len(match.group(1))
            title = match.group(2).strip()
            sections[title] = {
                'level': level,
                'content': self._get_section_content(title),
            }
        
        return sections
    
    def _get_section_content(self, section_title: str) -> str:
        """Get content for a specific section."""
        # Find section and extract until next heading
        pattern = rf'(^##\s+{re.escape(section_title)}.*?)(?=^##|$)'
        match = re.search(pattern, self.mirror_content, re.MULTILINE | re.DOTALL)
        return match.group(1) if match else ''
    
    def _extract_todos(self) -> List[Dict[str, Any]]:
        """Extract all TODO markers from mirror."""
        todos = []
        
        pattern = r'\[TODO:\s*(.+?)\]'
        for match in re.finditer(pattern, self.mirror_content):
            todo_text = match.group(1).strip()
            
            # Find which section this TODO belongs to
            section = self._find_section_for_position(match.start())
            
            todos.append({
                'text': todo_text,
                'section': section,
                'position': match.start(),
                'impact': self._estimate_impact(todo_text),
                'priority': self._estimate_priority(section),
            })
        
        # Sort by priority (high first)
        todos.sort(key=lambda x: x['priority'], reverse=True)
        
        return todos
    
    def _find_section_for_position(self, position: int) -> str:
        """Find section name for a given position in the file."""
        # Find the last heading before this position
        heading_pattern = r'^(#{1,6})\s+(.+)$'
        last_section = 'General'
        
        for match in re.finditer(heading_pattern, self.mirror_content[:position], re.MULTILINE):
            last_section = match.group(2).strip()
        
        return last_section
    
    def _estimate_impact(self, todo_text: str) -> str:
        """Estimate impact level of missing information."""
        todo_lower = todo_text.lower()
        
        high_impact_keywords = [
            'objectives', 'success', 'kpi', 'metrics', 'scope', 'timeline',
            'deliverable', 'budget', 'architecture', 'technical', 'budget'
        ]
        
        for keyword in high_impact_keywords:
            if keyword in todo_lower:
                return 'HIGH'
        
        if any(kw in todo_lower for kw in ['optional', 'nice-to-have', 'future']):
            return 'LOW'
        
        return 'MEDIUM'
    
    def _estimate_priority(self, section: str) -> int:
        """Estimate priority score based on section."""
        section_lower = section.lower()
        
        priority_map = {
            'executive': 10,
            'objective': 9,
            'scope': 8,
            'success': 8,
            'kpi': 7,
            'timeline': 7,
            'budget': 7,
            'team': 6,
            'risk': 5,
            'stakeholder': 4,
        }
        
        for keyword, score in priority_map.items():
            if keyword in section_lower:
                return score
        
        return 3
    
    def check(self) -> Dict[str, Any]:
        """Perform completion check."""
        total_sections = len(self.sections)
        completed_sections = []
        partial_sections = []
        incomplete_sections = []
        
        for section_title, section_data in self.sections.items():
            content = section_data['content']
            
            # Count TODOs in section
            todos_in_section = len(re.findall(r'\[TODO:', content))
            review_items = len(re.findall(r'\[REVIEW:', content))
            
            if todos_in_section == 0 and review_items == 0:
                completed_sections.append(section_title)
            elif todos_in_section == 0:
                partial_sections.append({
                    'section': section_title,
                    'review_items': review_items,
                    'status': 'flagged_for_review',
                })
            else:
                incomplete_sections.append({
                    'section': section_title,
                    'todos': todos_in_section,
                    'review_items': review_items,
                    'status': 'incomplete',
                })
        
        # Calculate completion percentage
        completion_percent = int(
            (len(completed_sections) + 0.5 * len(partial_sections)) 
            / total_sections * 100
        ) if total_sections > 0 else 0
        
        self.completion_data = {
            'timestamp': datetime.now().isoformat(),
            'mirror_file': str(self.mirror_path),
            'total_sections': total_sections,
            'completed_sections': completed_sections,
            'partial_sections': partial_sections,
            'incomplete_sections': incomplete_sections,
            'completed_count': len(completed_sections),
            'partial_count': len(partial_sections),
            'incomplete_count': len(incomplete_sections),
            'completion_percent': completion_percent,
            'todos': self.todos,
            'prioritized_gaps': self._get_prioritized_gaps(),
        }
        
        return self.completion_data
    
    def _get_prioritized_gaps(self) -> List[Dict[str, Any]]:
        """Get prioritized list of gaps director should address."""
        prioritized = []
        
        for todo in self.todos:
            prioritized.append({
                'section': todo['section'],
                'description': todo['text'],
                'impact': todo['impact'],
                'priority_score': todo['priority'],
                'suggested_question': self._generate_question(todo),
            })
        
        # Return top 5 by priority
        return prioritized[:5]
    
    def _generate_question(self, todo: Dict[str, Any]) -> str:
        """Generate a specific question for the director."""
        section = todo['section']
        todo_text = todo['text'].lower()
        
        # Generate contextual questions
        if 'objective' in todo_text:
            return f"For {section}: Please provide 3-5 SMART objectives aligned with project goals."
        elif 'success' in todo_text or 'metric' in todo_text or 'kpi' in todo_text:
            return f"For {section}: Define 5-7 success metrics with targets and measurement methods."
        elif 'timeline' in todo_text or 'schedule' in todo_text:
            return f"For {section}: Provide key milestones and dependencies (dates, blockers)."
        elif 'team' in todo_text or 'resource' in todo_text:
            return f"For {section}: List team members, roles, and responsibilities."
        elif 'budget' in todo_text or 'cost' in todo_text:
            return f"For {section}: Break down budget by category (labor, tools, infrastructure, etc.)."
        elif 'risk' in todo_text:
            return f"For {section}: Identify top 3-5 risks with likelihood, impact, and mitigation strategies."
        elif 'scope' in todo_text or 'deliverable' in todo_text:
            return f"For {section}: List specific deliverables, what's included, and what's explicitly excluded."
        elif 'stakeholder' in todo_text:
            return f"For {section}: Name key stakeholders, their interests, and communication frequency."
        elif 'architecture' in todo_text or 'technical' in todo_text:
            return f"For {section}: Describe system architecture (components, integrations, technology stack)."
        else:
            return f"For {section}: {todo_text}"
    
    def generate_markdown_checklist(self) -> str:
        """Generate markdown checklist."""
        lines = [
            "# Completion Status Report",
            "",
            f"**Overall: {self.completion_data['completion_percent']}% Complete**",
            "",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
        ]
        
        # Completed sections
        if self.completion_data['completed_sections']:
            lines.append("## ✅ Filled Sections")
            for section in self.completion_data['completed_sections']:
                lines.append(f"- [x] {section}")
            lines.append("")
        
        # Partial sections
        if self.completion_data['partial_sections']:
            lines.append("## 🔍 Partial / Flagged for Review")
            for item in self.completion_data['partial_sections']:
                lines.append(f"- [~] {item['section']} ({item['review_items']} review(s))")
            lines.append("")
        
        # Incomplete sections
        if self.completion_data['incomplete_sections']:
            lines.append("## ❓ Missing Information — Director Input Required")
            for item in self.completion_data['incomplete_sections']:
                lines.append(f"- [ ] {item['section']} ({item['todos']} TODO(s))")
            lines.append("")
        
        # Priority queue
        lines.append("## 📋 Director Priority Queue")
        lines.append("")
        lines.append("**Address these items in order to unblock progress:**")
        lines.append("")
        
        for idx, gap in enumerate(self.completion_data['prioritized_gaps'], 1):
            lines.append(f"### {idx}. {gap['section']} [Impact: {gap['impact']}]")
            lines.append("")
            lines.append(f"**Missing:** {gap['description']}")
            lines.append("")
            lines.append(f"**Question:** {gap['suggested_question']}")
            lines.append("")
        
        # Summary stats
        lines.append("## 📊 Summary")
        lines.append("")
        lines.append(f"- **Total Sections:** {self.completion_data['total_sections']}")
        lines.append(f"- **Completed:** {self.completion_data['completed_count']}/{self.completion_data['total_sections']}")
        lines.append(f"- **Partial:** {self.completion_data['partial_count']}")
        lines.append(f"- **Incomplete:** {self.completion_data['incomplete_count']}")
        lines.append(f"- **Total TODOs:** {len(self.completion_data['todos'])}")
        lines.append("")
        
        # Next steps
        lines.append("## ✨ Next Steps")
        lines.append("")
        lines.append("1. Review the Priority Queue above")
        lines.append("2. Provide answers to the suggested questions")
        lines.append("3. Agent will refill the mirror with your answers")
        lines.append("4. Repeat until all sections complete or director approves current state")
        lines.append("")
        
        return "\n".join(lines)
    
    def save_checklist(self, output_path: str = None) -> str:
        """Save markdown checklist."""
        if not output_path:
            stem = self.mirror_path.stem.replace('_filled', '')
            output_path = f"{stem}_completion_checklist.md"
        
        checklist = self.generate_markdown_checklist()
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(checklist)
        
        print(f"✅ Checklist saved to {output_path}")
        return output_path
    
    def save_json(self, output_path: str = None) -> str:
        """Save completion data as JSON."""
        if not output_path:
            stem = self.mirror_path.stem.replace('_filled', '')
            output_path = f"{stem}_completion_checklist.json"
        
        with open(output_path, 'w') as f:
            json.dump(self.completion_data, f, indent=2, default=str)
        
        print(f"✅ JSON checklist saved to {output_path}")
        return output_path


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    mirror_path = sys.argv[1]
    output_path = None
    
    if '--output' in sys.argv:
        idx = sys.argv.index('--output')
        if idx + 1 < len(sys.argv):
            output_path = sys.argv[idx + 1]
    
    try:
        print(f"\n📋 Checking Mirror Completion")
        print(f"Mirror: {mirror_path}")
        
        checker = CompletionChecker(mirror_path)
        completion = checker.check()
        
        # Save outputs
        checker.save_checklist(output_path)
        checker.save_json()
        
        # Print summary
        print(f"\n📊 Completion Summary:")
        print(f"Completion: {completion['completion_percent']}%")
        print(f"Completed: {completion['completed_count']}/{completion['total_sections']} sections")
        print(f"Partial: {completion['partial_count']}")
        print(f"Missing: {completion['incomplete_count']}")
        print(f"Total TODOs: {len(completion['todos'])}")
        
        # Show priority queue
        if completion['prioritized_gaps']:
            print(f"\n📋 Top Priority Gaps:")
            for idx, gap in enumerate(completion['prioritized_gaps'], 1):
                print(f"  {idx}. [{gap['impact']}] {gap['section']}: {gap['description'][:50]}...")
    
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
