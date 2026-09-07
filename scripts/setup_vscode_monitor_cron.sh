#!/bin/bash
# Setup local cron job for VS Code docs monitoring
# Usage: bash setup_cron.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/scripts/monitor_vscode_docs.py"
LOG_FILE="$SCRIPT_DIR/.logs/vscode-docs-monitor.log"

echo "🔧 Setting up local cron job for VS Code docs monitoring..."
echo "Script: $SCRIPT_PATH"
echo "Log: $LOG_FILE"

# Create log directory
mkdir -p "$(dirname "$LOG_FILE")"

# Make script executable
chmod +x "$SCRIPT_PATH"

# Create a wrapper script
WRAPPER_SCRIPT="$SCRIPT_DIR/.scripts/run_vscode_monitor.sh"
mkdir -p "$(dirname "$WRAPPER_SCRIPT")"

cat > "$WRAPPER_SCRIPT" << 'EOF'
#!/bin/bash
# Wrapper script for cron execution

cd "$(dirname "$0")/.."
export PATH="/usr/local/bin:/usr/bin:/bin"

# Activate Python environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Install dependencies if needed
python3 -m pip install -q requests beautifulsoup4 pyyaml 2>/dev/null || true

# Run monitor
python3 scripts/monitor_vscode_docs.py \
    --cache-dir .github/.vscode-docs-cache \
    --memory-file my/agentic_instructions/memories/VSCODE_WEEKLY.md \
    --base-url https://code.visualstudio.com/docs

exit $?
EOF

chmod +x "$WRAPPER_SCRIPT"

# Get current crontab (or create empty if doesn't exist)
TEMP_CRON=$(mktemp)
crontab -l > "$TEMP_CRON" 2>/dev/null || true

# Check if job already exists
if grep -q "run_vscode_monitor.sh" "$TEMP_CRON"; then
    echo "⚠️ Cron job already exists. Skipping addition."
    cat "$TEMP_CRON"
    rm "$TEMP_CRON"
    exit 0
fi

# Add new cron job (Monday 9:00 AM)
echo "" >> "$TEMP_CRON"
echo "# VS Code Docs Monitor - Every Monday at 9:00 AM" >> "$TEMP_CRON"
echo "0 9 * * 1 $WRAPPER_SCRIPT >> $LOG_FILE 2>&1" >> "$TEMP_CRON"

# Install new crontab
crontab "$TEMP_CRON"
rm "$TEMP_CRON"

echo "✅ Cron job installed successfully!"
echo ""
echo "📅 Schedule: Every Monday at 9:00 AM"
echo "📝 Log: $LOG_FILE"
echo ""
echo "To view cron jobs:"
echo "  crontab -l"
echo ""
echo "To remove cron job:"
echo "  crontab -e  # and delete the VS Code Docs Monitor line"
echo ""
echo "To test manually:"
echo "  bash $WRAPPER_SCRIPT"
