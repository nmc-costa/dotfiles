---
name: VS Code Docs Weekly Monitor
description: Automated weekly fetch and analysis of VS Code documentation updates with human-facing reports
scope: workspace
---

# VS Code Documentation Weekly Monitor

**Purpose:** Keep your workspace aligned with the latest VS Code documentation, features, and best practices through automated weekly analysis.

## Execution Schedule

- **Frequency:** Weekly (every Monday at 9:00 AM UTC)
- **Cron Expression:** `0 9 * * 1`
- **Timeout:** 5 minutes
- **Retry Policy:** Exponential backoff (1m → 2m → 4m) on failure

## Execution Flow

### Phase 1: Fetch & Detect Changes
1. **Fetch** `https://code.visualstudio.com/docs` and all linked documentation pages
2. **Compare** against cached version from previous run using:
   - HTTP ETag headers (primary)
   - Last-Modified headers (fallback)
   - Content text-diff (final verification)
3. **Identify** pages that are new or materially changed
4. **Extract** full content of changed pages for analysis

### Phase 2: Extract Actionable Intelligence
From changed documentation, identify and extract:

| Category | What to Extract | Example |
|----------|-----------------|---------|
| **New Tips** | Recently added user-facing features or workflows | "New: `/remote on` for session steering from mobile" |
| **Feature Changes** | API changes, deprecated features, new commands | "Chat slash commands now support `@filename` syntax" |
| **Recommended Settings** | Config changes aligned with new documentation | `"remoteSessions": true` in `~/.copilot/settings.json` |
| **Chat/Extension Workflows** | New agent patterns, skill examples, integration points | "Use custom agents for domain-specific code review" |
| **Security/Best Practices** | Policy changes, permission models, security guidance | "Sandbox policy enforcement for MCP servers" |

### Phase 3: Generate Human-Facing Report

**Output Format:** 5-bullet summary report

```
## VS Code Docs Weekly Update
**Week of [DATE]** | [N] pages analyzed | [M] changes detected

### Summary
[1 paragraph: What changed and why it matters to your workflow]

### 🎯 Top 3 Prioritized Actions
1. **[Action 1]** — [Why: impacts X workflow] — [How: do Y]
2. **[Action 2]** — [Why: enables Z feature]
3. **[Action 3]** — [Why: security/best-practice]

### 💡 Example Chat Prompts
- "Use `/remote on` to enable session steering from GitHub Mobile"
- "Create a sidekick agent to automatically gather context on `session.context_changed`"
- "Configure MCP servers in `.mcp.json` for your workspace"

### ⚙️ Recommended Config Changes
```json
{
  "remoteSessions": true,
  "experimentalFeatures": ["sandbox", "sidekick-agents"]
}
```

### 📚 Full Change Index
[List all changed pages with diff summaries]
```

### Phase 4: Persist & Notify

1. **Save Report:** Write output to `.agents/automation/VSCODE_WEEKLY.md`
   - Append new report with date header
   - Retain history (max 12 weeks = 3 months)
   - Include ETag/modification-date metadata for next run

2. **Notify:** Choose one or both:
   - **Option A (Recommended):** Open an Issue in the workspace repo
     - Title: `📚 VS Code Docs Update — Week of [DATE]`
     - Body: Full report + links to changed pages
     - Label: `documentation`, `automation`, `vscode-updates`
   - **Option B:** Post summary to chat (if running in agent context)
     - Format as brief 3-point summary
     - Link to full report in memory file

3. **Track Metadata:**
   - Store ETag/Last-Modified headers in `.github/.vscode-docs-cache.json`
   - Log execution time and pages processed
   - Record any fetch errors for debugging

## Implementation Options

### Option 1: GitHub Actions Workflow (Recommended)
- **File:** `.github/workflows/vscode-docs-monitor.yml`
- **Triggers:** Weekly schedule + manual dispatch
- **Secrets Required:** `GITHUB_TOKEN` (auto-provided)
- **Output:** Issues in current repo + memory file

**Pros:**
- No local setup required
- Automatic cross-device sync
- Built-in retry and error handling
- Easy to monitor/debug in Actions tab

**Cons:**
- Depends on GitHub Actions availability
- Slight delay (runs in queue)

### Option 2: Local Cron + Python Script (Development)
- **Script:** `scripts/monitor_vscode_docs.py`
- **Cron Setup:** Via `~/.crontab` or systemd timer
- **Output:** Memory file + optional local notifications

**Pros:**
- Immediate execution (no queue)
- Works offline (if docs already cached)
- Full control over timing/retry logic

**Cons:**
- Requires manual setup on each machine
- Depends on machine being online/awake
- No automatic cross-device sync

### Option 3: Hybrid (Best of Both)
- **Daily local check:** Fast cron run that updates cache
- **Weekly GitHub Action:** Final analysis and reporting
- **Sync:** Cache file committed to repo

## Configuration

### Environment Variables
```bash
VSCODE_DOCS_BASE_URL="https://code.visualstudio.com/docs"
VSCODE_DOCS_TIMEOUT=300  # seconds
VSCODE_DOCS_MAX_RETRIES=3
CACHE_DIR=".github/.vscode-docs-cache"
MEMORY_FILE=".agents/automation/VSCODE_WEEKLY.md"
GITHUB_REPO_OWNER=${OWNER}  # auto-filled
GITHUB_REPO_NAME=${REPO}    # auto-filled
```

### Cache Storage
```
.github/.vscode-docs-cache/
├── etags.json              # HTTP ETag values per URL
├── last-modified.json      # Last-Modified headers
├── content-hash.json       # SHA256 of full page content
└── manifest.json           # List of crawled pages + metadata
```

## Error Handling & Recovery

| Scenario | Fallback | Retry |
|----------|----------|-------|
| Network timeout | Use cached content from 2 weeks ago | Yes (3× exponential backoff) |
| Page not found (404) | Remove from manifest, note in report | No |
| Invalid JSON in report | Skip affected page, log error | Yes (fallback to text-diff) |
| Repo write fails | Store in temp buffer, retry next run | Yes |
| Issue creation fails | Append to memory file with note | Manual check |

## Monitoring & Debugging

### Check Last Run
```bash
cat .github/.vscode-docs-cache/manifest.json | jq '.last_run'
```

### View Report History
```bash
tail -50 .agents/automation/VSCODE_WEEKLY.md
```

### Manual Trigger (GitHub Actions)
1. Go to repo **Actions** tab
2. Select **VS Code Docs Monitor** workflow
3. Click **Run workflow** → **Run workflow**

### Manual Trigger (Local)
```bash
python scripts/monitor_vscode_docs.py --force --verbose
```

## Success Criteria

✅ **Report Generated:** Every Monday morning, new report appears in memory file  
✅ **Changes Detected:** Script identifies ≥1 new/changed page or reports "no significant changes"  
✅ **Actionable Output:** Report includes ≥3 specific actions tied to your workflows  
✅ **Notifications Working:** Issue/chat message delivered within 5 minutes of report generation  
✅ **Zero Errors:** No timeout, network, or parsing failures (or retry succeeds)

## Maintenance

- **Monthly:** Review memory file history, archive old reports (>3 months)
- **Quarterly:** Update documentation URL patterns if VS Code site structure changes
- **As Needed:** Add new keyword patterns to `config.yaml` for emerging features

## Related Files

- **Workflow:** `.github/workflows/vscode-docs-monitor.yml`
- **Script:** `scripts/monitor_vscode_docs.py`
- **Cache:** `.github/.vscode-docs-cache/`
- **Output:** `.agents/automation/VSCODE_WEEKLY.md`
- **Config:** `.github/vscode-docs-config.yaml`
