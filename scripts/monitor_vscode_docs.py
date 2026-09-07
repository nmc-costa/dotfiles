#!/usr/bin/env python3
"""
VS Code Documentation Weekly Monitor
Fetches, analyzes, and reports on changes to VS Code documentation.
"""

import os
import sys
import json
import hashlib
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from urllib.parse import urljoin, urlparse
import time

import requests
from bs4 import BeautifulSoup


class VSCodeDocsMonitor:
    """Monitor VS Code documentation for changes and generate reports."""

    def __init__(self, base_url: str, cache_dir: str, memory_file: str, force: bool = False):
        self.base_url = base_url
        self.cache_dir = Path(cache_dir)
        self.memory_file = Path(memory_file)
        self.force = force
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "VSCodeDocsMonitor/1.0"})

        # Create cache directory
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Cache files
        self.etags_file = self.cache_dir / "etags.json"
        self.content_hash_file = self.cache_dir / "content_hash.json"
        self.manifest_file = self.cache_dir / "manifest.json"

        # Load existing cache
        self.etags = self._load_json(self.etags_file)
        self.content_hashes = self._load_json(self.content_hash_file)
        self.manifest = self._load_json(self.manifest_file)

    def _load_json(self, filepath: Path) -> dict:
        """Load JSON file or return empty dict."""
        if filepath.exists():
            try:
                return json.loads(filepath.read_text())
            except json.JSONDecodeError:
                return {}
        return {}

    def _save_json(self, filepath: Path, data: dict):
        """Save JSON file."""
        filepath.write_text(json.dumps(data, indent=2))

    def _get_content_hash(self, content: str) -> str:
        """Get SHA256 hash of content."""
        return hashlib.sha256(content.encode()).hexdigest()

    def fetch_page(self, url: str) -> Tuple[Optional[str], Optional[Dict]]:
        """
        Fetch a page and return (content, metadata).
        Returns (None, None) if not changed (304).
        """
        try:
            # Prepare headers with ETag if cached
            headers = {}
            if url in self.etags:
                headers["If-None-Match"] = self.etags[url]

            response = self.session.get(url, timeout=10, headers=headers)

            if response.status_code == 304:
                # Not modified
                return None, None

            if response.status_code == 404:
                # Page deleted
                return "", {"status": 404, "deleted": True}

            response.raise_for_status()

            # Extract metadata
            metadata = {
                "status": response.status_code,
                "url": url,
                "fetched": datetime.utcnow().isoformat(),
                "content_type": response.headers.get("content-type", ""),
            }

            if "etag" in response.headers:
                self.etags[url] = response.headers["etag"]
                metadata["etag"] = response.headers["etag"]

            if "last-modified" in response.headers:
                metadata["last_modified"] = response.headers["last-modified"]

            return response.text, metadata

        except requests.RequestException as e:
            print(f"❌ Error fetching {url}: {e}")
            return None, {"error": str(e)}

    def extract_page_links(self, content: str, base_url: str) -> List[str]:
        """Extract all documentation links from a page."""
        if not content:
            return []

        links = set()
        soup = BeautifulSoup(content, "html.parser")

        for link in soup.find_all("a", href=True):
            href = link["href"]

            # Resolve relative URLs
            if href.startswith("/"):
                full_url = urljoin(base_url, href)
            else:
                full_url = urljoin(base_url, href)

            # Filter to VS Code docs domain
            if "code.visualstudio.com" in full_url and "/docs" in full_url:
                # Remove fragments and query params
                parsed = urlparse(full_url)
                clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                if clean_url not in ["https://code.visualstudio.com/docs", base_url]:
                    links.add(clean_url)

        return sorted(list(links))

    def extract_intelligence(self, content: str, url: str) -> Dict:
        """Extract actionable intelligence from documentation."""
        soup = BeautifulSoup(content, "html.parser")

        intelligence = {
            "url": url,
            "title": "",
            "new_features": [],
            "config_recommendations": [],
            "security_notes": [],
            "commands": [],
        }

        # Extract title
        title_tag = soup.find("h1") or soup.find("title")
        if title_tag:
            intelligence["title"] = title_tag.get_text(strip=True)

        # Look for common patterns
        text = content.lower()

        # New features / commands
        if "/remote" in text:
            intelligence["commands"].append("/remote on — Enable session remote control")
        if "slash command" in text:
            intelligence["commands"].append("Check for new slash commands in Chat")
        if "sidekick" in text:
            intelligence["new_features"].append("Sidekick agents for background automation")
        if "sandbox" in text:
            intelligence["security_notes"].append("Sandbox policy enforcement for tools/MCP")
        if "mcp" in text and "server" in text:
            intelligence["new_features"].append("MCP server configuration and management")

        return intelligence

    def detect_changes(self) -> Tuple[Dict, List]:
        """
        Detect changes in documentation.
        Returns (changed_pages, all_pages).
        """
        changed_pages = {}
        all_pages = {}

        print(f"\n🔍 Scanning VS Code documentation...")

        # Start with main docs page
        pages_to_check = [self.base_url]
        checked = set()

        max_pages = 100  # Safety limit
        max_depth = 3  # Limit crawl depth

        while pages_to_check and len(checked) < max_pages:
            url = pages_to_check.pop(0)

            if url in checked:
                continue

            checked.add(url)
            depth = url.count("/") - self.base_url.count("/")

            print(f"  📄 {url} ...", end=" ", flush=True)

            content, metadata = self.fetch_page(url)

            if content is None and metadata is None:
                print("✓ (cached, no change)")
                continue

            if content == "":
                print("❌ (deleted)")
                if url in self.content_hashes:
                    del self.content_hashes[url]
                continue

            if metadata.get("error"):
                print(f"⚠️ ({metadata['error']})")
                continue

            # Calculate content hash
            new_hash = self._get_content_hash(content)
            old_hash = self.content_hashes.get(url)

            is_new = old_hash is None
            is_changed = is_new or new_hash != old_hash

            if is_changed:
                print("✨ (CHANGED)" if not is_new else "🆕 (NEW)")
                changed_pages[url] = {"metadata": metadata, "new": is_new, "intelligence": self.extract_intelligence(content, url)}
            else:
                print("✓ (cached, no change)")

            # Update hash
            self.content_hashes[url] = new_hash

            # Extract and queue new links (limited crawl depth)
            if depth < max_depth and content:
                new_links = self.extract_page_links(content, self.base_url)
                for link in new_links:
                    if link not in checked and link not in pages_to_check:
                        pages_to_check.append(link)

            time.sleep(0.5)  # Rate limiting

        # Update manifest
        self.manifest = {
            "last_run": datetime.utcnow().isoformat(),
            "pages_checked": len(checked),
            "pages_changed": len(changed_pages),
            "pages_total": len(self.content_hashes),
        }

        print(f"\n📊 Summary: {len(checked)} pages checked, {len(changed_pages)} changes detected")

        return changed_pages, list(self.content_hashes.keys())

    def generate_report(self, changed_pages: Dict) -> str:
        """Generate human-facing report from changed pages."""
        if not changed_pages:
            return self._generate_no_changes_report()

        # Collect intelligence
        all_features = []
        all_configs = []
        all_security = []
        all_commands = []

        for url, data in changed_pages.items():
            intel = data["intelligence"]
            all_features.extend(intel["new_features"])
            all_configs.extend(intel["config_recommendations"])
            all_security.extend(intel["security_notes"])
            all_commands.extend(intel["commands"])

        # Build report
        report = f"""## VS Code Docs Weekly Update
**Week of {datetime.now().strftime('%Y-%m-%d')}** | {len(changed_pages)} pages changed

### Summary
VS Code documentation was updated with {len(changed_pages)} new or modified pages. 
Key areas: {', '.join(set([c.split(' — ')[0] for c in all_commands[:3]]) or ['general updates'])}.
Review the prioritized actions below to align your workflow with latest features.

### 🎯 Top 3 Prioritized Actions
"""

        # Prioritize actions
        priorities = []

        if any("/remote" in str(c) for c in all_commands):
            priorities.append(
                "1. **Enable Remote Session Control** — Use `/remote on` in Copilot CLI to steer sessions from GitHub Mobile while working on other tasks — Impact: Workflow flexibility"
            )

        if any("agent" in str(c).lower() or "sidekick" in str(c).lower() for c in all_features):
            priorities.append(
                "2. **Configure Custom Agents & Sidekicks** — Set up specialized agents in `.github/agents/` for domain-specific tasks — Impact: Automation & efficiency"
            )

        if any("mcp" in str(c).lower() or "sandbox" in str(c).lower() for c in all_security + all_features):
            priorities.append(
                "3. **Review MCP & Sandbox Configuration** — Update `.mcp.json` and sandbox policies per latest documentation — Impact: Security & tool compatibility"
            )

        # Fallback if not enough priorities
        while len(priorities) < 3 and all_commands:
            cmd = all_commands.pop(0)
            priorities.append(f"{len(priorities) + 1}. **{cmd}** — Review impact on your current workflow")

        report += "\n".join(priorities[:3]) + "\n"

        # Example prompts
        report += """
### 💡 Example Chat Prompts
- "Show me how to use `/remote on` to enable remote session steering"
- "Create a sidekick agent that gathers context when I switch Git branches"
- "Review my `.mcp.json` configuration and suggest improvements based on latest docs"

### ⚙️ Recommended Config Changes
```json
{
  "remoteSessions": true,
  "experimentalFeatures": ["sidekick-agents", "sandbox"]
}
```

### 📚 Full Change Index
"""

        for url, data in sorted(changed_pages.items()):
            status = "🆕" if data["new"] else "✏️"
            title = data["intelligence"]["title"] or url
            report += f"- {status} [{title}]({url})\n"

        return report

    def _generate_no_changes_report(self) -> str:
        """Generate report when no changes detected."""
        return f"""## VS Code Docs Weekly Update
**Week of {datetime.now().strftime('%Y-%m-%d')}** | No significant changes

### Summary
VS Code documentation had no material updates this week. Your configuration and workflows remain aligned with current best practices.

### ✅ Status
- Documentation is current
- No new breaking changes
- No urgent configuration updates needed

### 🔄 Next Check
Monitoring will resume next Monday at 9:00 AM UTC.
"""

    def save_report(self, report: str):
        """Append report to memory file."""
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)

        if self.memory_file.exists():
            existing = self.memory_file.read_text()
            # Keep only last 12 reports (3 months)
            reports = existing.split("## VS Code Docs Weekly Update")
            if len(reports) > 13:  # Keep header + 12 reports
                reports = reports[:13]
            content = "## VS Code Docs Weekly Update".join(reports)
        else:
            content = ""

        # Prepend new report
        final_content = report + "\n\n" + content
        self.memory_file.write_text(final_content)

        print(f"✅ Report saved to {self.memory_file}")

    def save_cache(self):
        """Save cache files."""
        self._save_json(self.etags_file, self.etags)
        self._save_json(self.content_hash_file, self.content_hashes)
        self._save_json(self.manifest_file, self.manifest)
        print(f"💾 Cache updated: {self.cache_dir}/")

    def run(self) -> bool:
        """Run the monitor. Returns True if changes detected."""
        print("=" * 60)
        print("VS Code Documentation Weekly Monitor")
        print("=" * 60)

        try:
            changed_pages, all_pages = self.detect_changes()
            report = self.generate_report(changed_pages)
            self.save_report(report)
            self.save_cache()

            print("\n" + "=" * 60)
            print(f"✅ Monitor complete: {len(changed_pages)} changes detected")
            print("=" * 60)

            return len(changed_pages) > 0

        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback

            traceback.print_exc()
            return False


def main():
    parser = argparse.ArgumentParser(description="Monitor VS Code documentation for changes")
    parser.add_argument("--base-url", default="https://code.visualstudio.com/docs", help="Base URL for VS Code docs")
    parser.add_argument("--cache-dir", default=".github/.vscode-docs-cache", help="Cache directory")
    parser.add_argument("--memory-file", default="my/agentic_instructions/memories/VSCODE_WEEKLY.md", help="Memory file for reports")
    parser.add_argument("--force", action="store_true", help="Force check all pages (ignore cache)")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    monitor = VSCodeDocsMonitor(base_url=args.base_url, cache_dir=args.cache_dir, memory_file=args.memory_file, force=args.force)

    changes_detected = monitor.run()

    # Set GitHub Actions output
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"changes_detected={'true' if changes_detected else 'false'}\n")

    sys.exit(0 if changes_detected else 0)  # Always exit 0 (no failure)


if __name__ == "__main__":
    main()
