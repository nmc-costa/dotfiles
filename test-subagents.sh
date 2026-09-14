#!/bin/bash
# Quick verification script for subagent setup

echo "=== Subagents Verification ==="
echo ""

# Check .agents structure
echo "✓ Checking .agents structure..."
if [[ -d .agents/skills ]]; then
  echo "  - .agents/skills/ exists"
  ls .agents/skills/ | sed 's/^/    /' || echo "    (empty)"
fi

if [[ -d .agents/workflows ]]; then
  echo "  - .agents/workflows/ exists"
  ls .agents/workflows/ | sed 's/^/    /' || echo "    (empty)"
fi

echo ""

# Check for SKILL.md
echo "✓ Checking SKILL.md files..."
find .agents/skills -name "SKILL.md" -exec dirname {} \; | sed 's/^/  /' || echo "  (none found)"

echo ""

# Check MDs for .agents/ reference
echo "✓ Checking root MDs mention .agents/..."
for md in README.md AGENTS.md CLAUDE.md GEMINI.md; do
  if grep -q "\.agents" "$md"; then
    echo "  ✓ $md"
  else
    echo "  ✗ $md (missing .agents reference)"
  fi
done

echo ""

# Check .agent/ is gone
if [[ -d .agent ]]; then
  echo "⚠ .agent/ still exists (should be removed)"
else
  echo "✓ .agent/ folder removed"
fi

echo ""
echo "Done!"
