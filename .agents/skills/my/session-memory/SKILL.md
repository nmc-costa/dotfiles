---
name: session-memory
description: Cross-chat session persistence with VS Code's built-in compaction
commands:
  - /memorize
  - /recall
---

# Session Memory Skill

Bridges VS Code's built-in `/compact` command with persistent storage for seamless context recovery **across different chat sessions**. This skill handles only what VS Code's built-in features don't: cross-chat persistence.

## Commands

### /memorize
Saves compacted session state to `my/agentic_instructions/memories/CURRENT_SESSION.md` for reuse in future chats.

**Usage:**
```
/memorize
```

**Workflow:**
1. Use `/compact [optional instructions]` in current chat (VS Code built-in)
2. Then type `/memorize` to save the compacted summary
3. This stores your work for the next chat session

**What it saves:**
- Compacted task summary (from `/compact`)
- Active file list and current progress
- Key decisions and design rationale
- Token-efficient context for next session

**When to use:**
- After compacting a long conversation with `/compact`
- Before ending a session to save for later
- When switching between projects in new chats

### /recall
Loads the last saved compacted state from `my/agentic_instructions/memories/CURRENT_SESSION.md`.

**Usage:**
```
/recall
```

**Workflow:**
1. Start a new chat
2. Type `/recall` to load previous context
3. Decide to continue work or start fresh

**What it restores:**
- Previous session's compacted summary
- Task context and progress status
- File locations and next steps
- Minimal but complete information

**When to use:**
- At the start of a new chat session
- When resuming work from a previous session
- To avoid re-explaining context

## How It Works

**Within-Session Compaction (VS Code Built-in):**
- Type `/compact [optional instructions]` to summarize earlier chat history
- Reduces token usage by freeing up context window space
- VS Code does this automatically when context fills

**Cross-Chat Persistence (This Skill):**
- After compacting, use `/memorize` to save for future chats
- Use `/recall` in new chats to restore compacted context
- Stores only what you need: ~60% token reduction on restart

## Architecture

```
Session A (long conversation)
    ↓ type: /compact focus on design decisions
    ↓ [conversation summarized in-place]
    ↓ type: /memorize
    → Saved to: my/agentic_instructions/memories/CURRENT_SESSION.md
                
Session B (new chat, fresh context window)
    ↓ type: /recall
    → Loaded from: my/agentic_instructions/memories/CURRENT_SESSION.md
    ↓ [agent displays compacted summary]
    ↓ Continue work with minimal token overhead
```

## Integration

- **Complement, not replacement:** Uses VS Code's built-in `/compact` for within-chat compression
- **Single source:** Stores compacted state in `my/agentic_instructions/memories/` (workspace-tracked, organized)
- **Token-efficient:** Only stores compacted summaries, not full conversation history
- **Workspace-local:** No reliance on session-scoped temporary storage

## Example Workflow

**Session 1 - Compacting:**
```
[Long conversation about bibliography validation...]

User: /compact focus on decisions and validation results
[VS Code summarizes and compresses history]

User: /memorize
Agent: ✅ Compacted session saved to my/agentic_instructions/memories/CURRENT_SESSION.md
  - Task: Bibliography validation (DriverCast Springer)
  - Progress: 20/20 entries validated
  - Decisions: Schema changes, format standardization
  - Next: Commit to repository
```

**Session 2 - Resuming:**
```
User: /recall
Agent: 📋 Found compacted session: Bibliography validation (DriverCast).
  Compacted summary shows 20/20 entries validated, ready to commit.
  Continue with this task?

User: Yes, let's commit
Agent: [continues with minimal re-context overhead]
```
