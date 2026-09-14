"""
orchestrate.py - projectHITs v4 Workflow Orchestrator

Orchestrate the complete mirror → fill → check workflow in one command.

Usage:
    python orchestrate.py <template_path> <brief_path> [--format markdown|latex|text] [--project-name MyProject]

This script:
    1. Analyzes template structure (template_analyzer.py)
    2. Generates mirror (mirror_generator.py)
    3. Auto-fills from brief (auto_filler.py)
    4. Checks completion + generates checklist (completion_checker.py)
    5. Creates session folder and archives all artifacts

Output:
    Organized session folder with:
    - {project}_mirror.md (structure mirror)
    - {project}_mirror_filled.md (filled mirror)
    - {project}_completion_checklist.md (human-readable checklist)
    - Various JSON mapping files
"""

import json
import sys
import subprocess
from pathlib import Path
from typing import Optional
from datetime import datetime


class Orchestrator:
    """Orchestrate the complete v4 workflow."""
    
    def __init__(self, template_path: str, brief_path: str, 
                 editable_format: str = 'markdown', project_name: Optional[str] = None):
        self.template_path = Path(template_path)
        self.brief_path = Path(brief_path)
        self.editable_format = editable_format
        self.project_name = project_name or self.template_path.stem
        
        # Create session folder
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        self.session_folder = Path(f"{self.project_name}_{editable_format}_{timestamp}")
        self.session_folder.mkdir(exist_ok=True)
        
        print(f"📁 Session folder: {self.session_folder}")
    
    def run(self) -> bool:
        """Run complete workflow."""
        try:
            # Phase 1: Analyze template
            print("\n[1/4] Analyzing template structure...")
            if not self._run_analyzer():
                return False
            
            # Phase 2: Generate mirror
            print("\n[2/4] Generating mirror...")
            mirror_file = self._run_mirror_generator()
            if not mirror_file:
                return False
            
            # Phase 3: Auto-fill from brief
            print("\n[3/4] Auto-filling from project brief...")
            filled_file = self._run_auto_filler(mirror_file)
            if not filled_file:
                return False
            
            # Phase 4: Check completion
            print("\n[4/4] Checking completion and generating checklist...")
            if not self._run_completion_checker(filled_file):
                return False
            
            # Create summary
            self._create_summary()
            
            print(f"\n✅ Workflow complete!")
            print(f"📁 All outputs saved to: {self.session_folder}")
            
            return True
        
        except Exception as e:
            print(f"❌ Workflow failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _run_analyzer(self) -> bool:
        """Run template analyzer."""
        output_file = self.session_folder / f"{self.project_name}_analysis.json"
        
        cmd = [
            'python', 'template_analyzer.py',
            str(self.template_path),
            '--output', str(output_file)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Analyzer failed: {result.stderr}")
            return False
        
        print(result.stdout)
        return True
    
    def _run_mirror_generator(self) -> Optional[str]:
        """Run mirror generator."""
        output_file = self.session_folder / f"{self.project_name}_mirror.md"
        
        cmd = [
            'python', 'mirror_generator.py',
            str(self.template_path),
            '--format', self.editable_format,
            '--output', str(output_file)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Mirror generator failed: {result.stderr}")
            return None
        
        print(result.stdout)
        return str(output_file)
    
    def _run_auto_filler(self, mirror_file: str) -> Optional[str]:
        """Run auto-filler."""
        output_file = self.session_folder / f"{self.project_name}_mirror_filled.md"
        
        cmd = [
            'python', 'auto_filler.py',
            mirror_file,
            str(self.brief_path),
            '--output', str(output_file)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Auto-filler failed: {result.stderr}")
            return None
        
        print(result.stdout)
        return str(output_file)
    
    def _run_completion_checker(self, filled_file: str) -> bool:
        """Run completion checker."""
        output_file = self.session_folder / f"{self.project_name}_completion_checklist.md"
        
        cmd = [
            'python', 'completion_checker.py',
            filled_file,
            '--output', str(output_file)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Completion checker failed: {result.stderr}")
            return False
        
        print(result.stdout)
        return True
    
    def _create_summary(self):
        """Create workflow summary."""
        summary = {
            'project_name': self.project_name,
            'session_timestamp': datetime.now().isoformat(),
            'template_path': str(self.template_path),
            'brief_path': str(self.brief_path),
            'editable_format': self.editable_format,
            'session_folder': str(self.session_folder),
            'artifacts': {
                'mirror': f"{self.project_name}_mirror.md",
                'filled': f"{self.project_name}_mirror_filled.md",
                'checklist': f"{self.project_name}_completion_checklist.md",
                'analysis': f"{self.project_name}_analysis.json",
                'fill_mapping': f"{self.project_name}_mirror_fill_mapping.json",
                'completion_json': f"{self.project_name}_completion_checklist.json",
            },
            'next_steps': [
                "1. Review the generated mirror file",
                "2. Verify structure matches original template",
                "3. Review completion_checklist.md for missing information",
                "4. Provide director input for priority gaps",
                "5. Agent refills mirror and updates checklist",
            ],
        }
        
        summary_file = self.session_folder / 'workflow_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n📋 Workflow Summary:")
        print(json.dumps(summary, indent=2))


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    
    template_path = sys.argv[1]
    brief_path = sys.argv[2]
    editable_format = 'markdown'
    project_name = None
    
    if '--format' in sys.argv:
        idx = sys.argv.index('--format')
        if idx + 1 < len(sys.argv):
            editable_format = sys.argv[idx + 1]
    
    if '--project-name' in sys.argv:
        idx = sys.argv.index('--project-name')
        if idx + 1 < len(sys.argv):
            project_name = sys.argv[idx + 1]
    
    try:
        orchestrator = Orchestrator(template_path, brief_path, editable_format, project_name)
        success = orchestrator.run()
        sys.exit(0 if success else 1)
    
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
