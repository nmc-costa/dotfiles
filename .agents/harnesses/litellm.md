# 🔌 LiteLLM Reference

**Status:** Reference for building a custom app — like the OpenAI guide, this is not a
drop-in harness; it's for when you build your own app on top of LiteLLM's multi-provider
abstraction and want it to use the personas/skills in this repo.

The previous version of this guide called `litellm.completion(model=..., system_prompt=...)`
— `system_prompt` is not a real LiteLLM/OpenAI-style parameter; the system prompt belongs in
`messages` as a `{"role": "system", ...}` entry, same as the underlying provider SDKs. Fixed
below. It also referenced `config/litellm-config.json` and `config/harness-config.json`,
neither of which exists in this repo (the old `agentic_instructions` repo's harness config was
confirmed broken/aspirational by the source-repo audit and was not migrated).

---

## Key Files (in this repo)

- **Master Persona:** `.agents/instructions/base-personas/archi.md`
- **Task Personas:** `.agents/instructions/task-personas/`
- **Skills:** `.agents/skills/<name>/SKILL.md`

## Install

```bash
pip install litellm
```

## Loading a Persona + Calling LiteLLM

```python
from pathlib import Path
import litellm

REPO = Path.home() / "dotfiles"

def load_persona(task_persona_name: str | None = None) -> str:
    master = (REPO / ".agents/instructions/base-personas/archi.md").read_text()
    if not task_persona_name:
        return master
    task_path = REPO / ".agents/instructions/task-personas" / f"{task_persona_name}.md"
    return f"{master}\n\n---\n\n{task_path.read_text()}"

# Route by task complexity — pick real, current model IDs for your providers;
# don't copy the ones below verbatim, they age quickly.
MODEL_ROUTING = {
    "complex_reasoning": "anthropic/claude-opus-4",
    "fast_tasks": "openai/gpt-4o-mini",
    "code_generation": "anthropic/claude-sonnet-4",
    "cost_optimized": "openai/gpt-4o-mini",
}

def call(user_message: str, persona: str | None = None, task_type: str = "cost_optimized"):
    system_prompt = load_persona(persona)
    model = MODEL_ROUTING.get(task_type, MODEL_ROUTING["cost_optimized"])
    response = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content
```

## Cost & Latency Tracking

LiteLLM supports success/failure callbacks — use them instead of hand-rolled logging:

```python
def log_success(kwargs, completion_response, start_time, end_time):
    usage = completion_response.usage
    print(f"✓ model={completion_response.model} tokens={usage.total_tokens}")

def log_failure(kwargs, exception, start_time, end_time):
    print(f"✗ model={kwargs.get('model')} failed: {exception}")

litellm.success_callback = [log_success]
litellm.failure_callback = [log_failure]
```

(Check LiteLLM's current docs for the exact callback signature for the version you install —
it has changed across releases.)

## Multi-Provider Routing

| Task | Suggested tier | Reason |
|------|-------|---|
| Complex charter/architecture | premium (e.g. a frontier Claude or GPT model) | Quality on long-form output |
| Quick brief / classification | budget (e.g. a small/fast model) | Cost + latency |
| Detailed presentation, thorough review, complex diagram | premium | Quality-sensitive |
| Documentation synthesis | premium | Quality-sensitive |

Don't pin exact model IDs in this doc long-term — check current provider docs; model names
and tiers shift often.

## Deployment Checklist

- [ ] `pip install litellm`, provider API keys set as environment variables
  (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, etc. — whichever providers you
  actually route to)
- [ ] Your app reads `.agents/instructions/base-personas/archi.md` and the relevant
      `.agents/instructions/task-personas/*.md` directly (no config file needed)
- [ ] System prompt passed via `messages=[{"role": "system", ...}, ...]`, not a
      `system_prompt=` kwarg
- [ ] Model routing table matches actual task complexity, using current model IDs
- [ ] Cost/latency callbacks wired up if this becomes a production integration
