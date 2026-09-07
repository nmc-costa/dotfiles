# VS Code Docs Weekly Monitor — Quick Start

Your workspace now has an automated system to detect and report on VS Code documentation updates every week.

---

## 📋 What It Does

✅ **Every Monday at 9:00 AM** (UTC):
1. Fetches the latest VS Code documentation
2. Detects new/changed pages (using ETags + content hashing)
3. Extracts actionable intelligence (features, configs, commands)
4. Generates a human-facing report with:
   - 📝 Summary of changes
   - 🎯 Top 3 prioritized actions for your workflow
   - 💡 Example chat prompts to use
   - ⚙️ Recommended config updates
5. Saves report to `my/agentic_instructions/memories/VSCODE_WEEKLY.md`
6. Optionally opens a GitHub Issue to notify you

---

## 🚀 Setup (Choose One Option)

### **Option 1: GitHub Actions (Recommended — No Setup Required)**

✅ **Already installed!** The workflow is active at `.github/workflows/vscode-docs-monitor.yml`

**How to verify:**
1. Go to your repo → **Actions** tab
2. Look for **"VS Code Docs Monitor"** workflow
3. Check the **Schedule** section—it should run every Monday at 9:00 AM UTC

**Manual trigger (test):**
1. Actions tab → **VS Code Docs Monitor** workflow
2. Click **Run workflow** → **Run workflow**
3. Check the run output and the memory file

**Pros:**
- ✅ No local setup
- ✅ Automatic cross-device sync
- ✅ Built-in error handling & retry logic
- ✅ Issues opened automatically with reports

---

### **Option 2: Local Cron (Development/Custom Timing)**

Run on your local machine with custom schedule.

**1️⃣ Install dependencies:**
```bash
pip install requests beautifulsoup4 pyyaml
```

**2️⃣ Set up cron job:**
```bash
bash scripts/setup_vscode_monitor_cron.sh
```

This will:
- Create a wrapper script at `.scripts/run_vscode_monitor.sh`
- Add a cron entry to run every Monday at 9:00 AM
- Create log file at `.logs/vscode-docs-monitor.log`

**3️⃣ Verify it's installed:**
```bash
crontab -l | grep vscode
```

**4️⃣ Test it manually:**
```bash
bash .scripts/run_vscode_monitor.sh
```

**To remove the cron job:**
```bash
crontab -e
# Delete the line: "0 9 * * 1 ..."
```

**Pros:**
- ✅ Runs immediately (no GitHub queue)
- ✅ Works offline if docs are cached
- ✅ Full control over timing
- ⚠️ Requires machine to be online & awake

---

### **Option 3: Hybrid (Best of Both)**

- **Daily cron locally:** Quick cache refresh
- **Weekly GitHub Action:** Final analysis + issue creation
- **Sync:** Cache committed to repo for cross-device sharing

Add this to your local crontab:
```bash
# Daily refresh of cache (local)
0 6 * * * cd /path/to/repo && python3 scripts/monitor_vscode_docs.py --cache-dir .github/.vscode-docs-cache 2>&1 >> .logs/vscode-docs-monitor.log
```

---

## 📂 Files Created

```
.github/
├── workflows/
│   └── vscode-docs-monitor.yml          # GitHub Actions workflow
├── .vscode-docs-cache/                  # Cache directory (auto-created)
│   ├── etags.json                       # HTTP ETag values
│   ├── content_hash.json                # SHA256 hashes of pages
│   └── manifest.json                    # Metadata & last run info

scripts/
├── monitor_vscode_docs.py               # Main monitoring script
├── setup_vscode_monitor_cron.sh         # Local cron setup

my/agentic_instructions/
└── memories/
    └── VSCODE_WEEKLY.md                 # Weekly reports (auto-created)

my/agentic_instructions/instructions/automation/
└── vscode-docs-monitor.instructions.md  # Full documentation
```

---

## 📊 View Reports

**Latest report:**
```bash
head -50 my/agentic_instructions/memories/VSCODE_WEEKLY.md
```

**Full history:**
```bash
cat my/agentic_instructions/memories/VSCODE_WEEKLY.md
```

**Last execution details:**
```bash
cat .github/.vscode-docs-cache/manifest.json | jq .
```

---

## 🧪 Manual Testing

**Test the script:**
```bash
python3 scripts/monitor_vscode_docs.py \
  --force \
  --verbose \
  --base-url https://code.visualstudio.com/docs \
  --cache-dir .github/.vscode-docs-cache \
  --memory-file my/agentic_instructions/memories/VSCODE_WEEKLY.md
```

**Test GitHub Actions locally:**
```bash
# Install act: https://github.com/nektos/act
act schedule -j monitor-vscode-docs
```

---

## 🔄 How It Works

### **Change Detection Strategy**

1. **HTTP ETag Check** (fastest)
   - Compares `ETag` header with cached value
   - If ETags match → page unchanged, skip

2. **Last-Modified Check** (fallback)
   - If no ETag, compares `Last-Modified` header
   - Skip if timestamp is same

3. **Content Hash Check** (comprehensive)
   - SHA256 hash of full page content
   - Detects changes even if headers don't update
   - Used as final verification

### **Intelligence Extraction**

For each changed page, the script looks for:
- **Commands:** `/remote`, `/task`, `/agent`, etc.
- **Features:** "sidekick", "MCP", "sandbox", "agent", etc.
- **Config:** Recommended settings and `.json` structures
- **Security:** Permission models, policy enforcement

### **Report Generation**

Reports prioritize:
1. **Workflow impact** — Features/commands that change how you work
2. **Actionability** — Things you should do immediately
3. **Examples** — Concrete prompts to use in chat

---

## ⚙️ Configuration

To customize the monitor, edit:

**`.github/workflows/vscode-docs-monitor.yml`:**
- Change schedule (cron expression)
- Modify issue labels
- Adjust retry policy

**`scripts/monitor_vscode_docs.py`:**
- `max_pages = 100` — Limit crawled pages
- `max_depth = 3` — Limit crawl depth (prevents infinite loops)
- `time.sleep(0.5)` — Rate limiting between requests

---

## 🐛 Troubleshooting

**Issue: Cron job doesn't run**
```bash
# Check cron logs
log show --predicate 'process == "cron"' --last 1h  # macOS
sudo grep CRON /var/log/syslog | tail -20           # Linux
```

**Issue: GitHub Actions workflow doesn't trigger**
- Check Actions tab → Workflows → VS Code Docs Monitor
- Verify schedule is enabled
- Try manual trigger: **Run workflow**

**Issue: Report not generated**
1. Check `.github/.vscode-docs-cache/manifest.json` for last run
2. Check logs: `.logs/vscode-docs-monitor.log`
3. Run manual test with `--verbose` flag

**Issue: Memory file not updating**
- Verify write permissions on `my/agentic_instructions/memories/`
- Check GitHub Actions permissions (needs `contents: write`)

---

## 📞 Support

- **Full Documentation:** `my/agentic_instructions/instructions/automation/vscode-docs-monitor.instructions.md`
- **Workflow Logs:** GitHub Actions tab → VS Code Docs Monitor → Run history
- **Local Logs:** `.logs/vscode-docs-monitor.log`
- **Cache Debug:** `cat .github/.vscode-docs-cache/manifest.json | jq`

---

## ✅ Next Steps

1. **GitHub Actions:** Monitor should run next Monday at 9:00 AM UTC
2. **Local Cron (optional):** Run `bash scripts/setup_vscode_monitor_cron.sh`
3. **Test (now):** Run `python3 scripts/monitor_vscode_docs.py --force --verbose`
4. **Check Report:** `head -50 my/agentic_instructions/memories/VSCODE_WEEKLY.md`

---

**Questions?** Check the full instruction file: `my/agentic_instructions/instructions/automation/vscode-docs-monitor.instructions.md`
