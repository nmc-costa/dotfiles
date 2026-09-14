# 🔌 OpenAI API Reference

**Status:** Reference for building a custom app — not a drop-in harness like Claude Code.
Unlike Claude Code, GitHub Copilot, or Gemini CLI, there is no OpenAI product that auto-reads
`.agents/skills/`. This document is for *when you build your own app* that calls the OpenAI
API and want it to use the personas/skills in this repo.

The previous version of this guide used `openai.ChatCompletion.create(..., system=...)` —
that's the pre-2023 SDK, and `system` was never a valid top-level parameter of that call even
then; the system prompt always goes in `messages` as a `{"role": "system", ...}` entry. The
examples below use the current (`openai>=1.0`) Python SDK and correct message structure.

---

## Key Files (in this repo)

- **Master Persona:** `.agents/instructions/base-personas/archi.md`
- **Task Personas:** `.agents/instructions/task-personas/`
- **Skills:** `.agents/skills/<name>/SKILL.md`

There is no `config/openai-config.json` or `config/harness-config.json` in this repo — those
were part of the old `agentic_instructions` repo and were confirmed broken/aspirational
(never-referenced trigger map) by the source-repo audit, and were not migrated.

## Loading a Persona into a System Prompt

```python
from pathlib import Path
from openai import OpenAI

client = OpenAI()  # reads OPENAI_API_KEY from env

REPO = Path.home() / "dotfiles"

def load_persona(task_persona_name: str | None = None) -> str:
    master = (REPO / ".agents/instructions/base-personas/archi.md").read_text()
    if not task_persona_name:
        return master
    task_path = REPO / ".agents/instructions/task-personas" / f"{task_persona_name}.md"
    return f"{master}\n\n---\n\n{task_path.read_text()}"

system_prompt = load_persona("projectHITs")

response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input},
    ],
)
print(response.choices[0].message.content)
```

## Persona Trigger via Function Calling (optional)

If you want the model itself to choose which persona to load (rather than your app deciding
up front), define a tool and let the model call it:

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "load_persona",
            "description": "Load a task-specific persona for the current task",
            "parameters": {
                "type": "object",
                "properties": {
                    "persona": {
                        "type": "string",
                        "enum": ["projectHITs", "presentHITs", "reviewHITs",
                                 "diagramHITs", "mockupHITs", "documentHITs"],
                    }
                },
                "required": ["persona"],
            },
        },
    }
]

response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=messages,
    tools=tools,
    tool_choice="auto",
)
```

Your app is responsible for handling the resulting `tool_calls`, reading the matching file
from `.agents/instructions/task-personas/`, and feeding it back into the conversation — the
OpenAI API does not read your filesystem for you.

## Model Selection

| Task | Suggested model | Reason |
|------|-------|--------|
| Complex reasoning (charter, architecture) | a frontier-tier model | Higher-quality long-form output |
| Fast classification / routing | a smaller/faster model | Speed + cost efficiency |
| Code generation | a frontier-tier model | Quality and accuracy |
| Simple formatting | a smaller/faster model | Cost optimization |

(Deliberately not pinning exact model IDs here — check current OpenAI model docs; `gpt-4-turbo`/
`gpt-3.5-turbo` as named in the old guide may already be superseded by the time you read this.)

## Cost Optimization

1. Use a cheaper/faster model for simple formatting, routing/classification, fast turnaround.
2. Cache system prompts where the SDK/API supports prompt caching, rather than re-sending
   `archi.md` in full on every call.
3. Reference personas by name and load on demand (function calling above) rather than
   concatenating every persona into every request.

## Environment Variables

```bash
OPENAI_API_KEY=sk-...
OPENAI_ORG_ID=org-...   # optional
```

## Deployment Checklist

- [ ] `OPENAI_API_KEY` set in environment
- [ ] Your app reads `.agents/instructions/base-personas/archi.md` and the relevant
      `.agents/instructions/task-personas/*.md` directly (no config file needed)
- [ ] System prompt passed as a `{"role": "system", ...}` message, not a `system=` kwarg
- [ ] Using `openai>=1.0` SDK syntax (`client.chat.completions.create`, not the removed
      `openai.ChatCompletion.create`)
- [ ] Model routing matches actual task complexity (see table above)
- [ ] Cost/token logging in place if this becomes a production integration
