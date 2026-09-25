// chronicle-chain — D7 chain bridge (opencode server plugin).
//
// Watches each finished assistant reply for the chain-suggestion footer
// defined in .agents/instructions/workspace-config/output-frame.instructions.md
// ("Next: /skill <args>" — at most one line, only when a chain from the
// executed skill's ## Chains section applies) and stages it into the TUI
// prompt input via the tui.prompt.append endpoint, so the owner confirms
// the next skill with a single Enter instead of retyping it.
//
// Propose-only: this never submits a prompt, it only appends text to the
// input box; the human still reads and presses Enter. Errors are swallowed
// by design — a headless run (no TUI) or a transient API failure must never
// break the turn (same contract as .agents/hooks/precompact_handoff.py).
//
// Deployed by sync.sh to ~/.config/opencode/plugins/ — plural: that's the
// global plugin dir opencode auto-discovers (the singular plugin/ is never
// scanned); no opencode.json entry needed. Spec: card dotfiles-tsk-chronicle-d7;
// real sidebar panels are opencode FR #5971 (still open as of 2026-09-25).

// Matches the footer line after markdown decoration is stripped: bold,
// backticks, blockquote markers, list dashes and trailing punctuation are
// all allowed, but the suggestion itself must start with "/" — prose like
// "Next: owner picks whether..." is deliberately ignored.

function parseNextFooter(text) {
  if (!text) return null
  const lines = text.split("\n")
  for (let i = lines.length - 1; i >= 0; i--) {
    const line = lines[i].replace(/[`*_>"']/g, "").replace(/^\s*[-*+]\s+/, "").trim().replace(/\.+$/, "").trim()
    const m = line.match(/^next\b\s*:?\s*(.+)$/i)
    if (!m) continue
    const candidate = m[1].trim()
    if (/^\/[\w-]+(\s+.*)?$/.test(candidate)) return candidate
    return null // a "Next:" line that isn't a slash command ends the scan
  }
  return null
}

function lastAssistantText(messages) {
  const list = Array.isArray(messages) ? messages : []
  for (let i = list.length - 1; i >= 0; i--) {
    const msg = list[i] ?? {}
    const info = msg.info ?? msg
    if (info.role !== "assistant" || info.error) continue
    const parts = Array.isArray(msg.parts) ? msg.parts : []
    const text = parts
      .filter((p) => p.type === "text" && !p.synthetic && !p.ignored && p.text)
      .map((p) => p.text)
      .join("\n")
      .trim()
    if (text) return text
  }
  return null
}

export default async ({ client }) => {
  // One entry per session: the last command we staged, so a re-delivered
  // idle event (or an unchanged footer across turns) never double-appends.
  const lastStaged = new Map()

  return {
    event: async ({ event }) => {
      try {
        if (event?.type !== "session.idle") return
        const sessionID = event.properties?.sessionID
        if (!sessionID || typeof client?.session?.messages !== "function") return

        const res = await client.session.messages({ path: { id: sessionID } })
        const messages = res?.data ?? res
        const next = parseNextFooter(lastAssistantText(messages))
        if (!next || lastStaged.get(sessionID) === next) return
        lastStaged.set(sessionID, next)

        if (typeof client?.tui?.appendPrompt === "function") {
          await client.tui.appendPrompt({ body: { text: next } })
        }
      } catch {
        // Never break the turn: headless sessions, TUI-less servers and
        // API hiccups all land here on purpose.
      }
    },
  }
}
