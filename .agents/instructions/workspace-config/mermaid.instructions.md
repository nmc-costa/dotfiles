---
applyTo: "**"
---
# Mermaid AI Skills

When the user asks to create, edit, or visualize any diagram, use the Mermaid
VS Code extension tools and commands described below.

## Scope

These rules apply to **diagrams the user requests as a deliverable** (a
diagram file, a diagram for a doc, "draw me X"). They do **not** apply to the
inline `## Flow` diagram in an Output Frame footer
(`output-frame.instructions.md`): that one needs no `.mmd` file and no
preview, and must still use the Output Frame's Mermaid safe subset. Where
`mermaid-diagram-validator` exists (VS Code Copilot), still call it on the
footer diagram; elsewhere the safe subset stands in for it. The LM tools and
commands below only exist in VS Code Copilot — other harnesses skip them.

## Workflow

1. Determine the diagram type and generate Mermaid syntax.
2. Write the diagram to a `.mmd` file in the project.
3. Validate syntax: correct first-line keyword, arrow types, balanced brackets.
4. Preview via the Mermaid extension — open the `.mmd` file (auto-preview) or run
   **MermaidChart: Preview Diagram** (`mermaidChart.preview`).

## LM Tools — call these for every diagram interaction

- `mermaid-diagram-validator` — validate Mermaid syntax before presenting any diagram
- `mermaid-diagram-preview` — render a live preview inside VS Code after generating
- `get-syntax-docs-mermaid` — fetch correct syntax docs for any diagram type

## VS Code Commands

Invoke via Command Palette or the VS Code command API (GitHub Copilot in VS Code only).
Do not invent command IDs. Prefer writing/editing `.mmd` files when a command is not needed.

### Diagram editing & preview
- **Preview** (`mermaidChart.preview`) — preview the active Mermaid editor (`.mmd` / `.mermaid` must be open).
- **Create Diagram** (`mermaidChart.createMermaidFile`) — creates a demo flowchart and opens preview side by side.
- **Repair Diagram** (`mermaidChart.repairDiagram`) — Mermaid AI repair for the active diagram; uses Mermaid AI credits — tell the user before running.
- **Improve Diagram** (`mermaidChart.improveDiagram`) — uses Copilot / LM API; suggests layout + styling variants for the active diagram.

### Generate diagrams (GitHub Copilot required)
- **Generate Diagram from Code** (`mermaidChart.generateDiagramFromCode`)
- **Generate Cloud Diagram** (`mermaidChart.generateCloudDiagram`)
- **Generate ER Diagram** (`mermaidChart.generateERDiagram`)
- **Generate Docker Diagram** (`mermaidChart.generateDockerDiagram`)
- **Open AI Chat** (`mermaidChart.openCopilotChat`)

### Mermaid Chart cloud
- **Login** (`mermaidChart.login`) / **Logout** (`mermaidChart.logout`)
- **Connect Diagram** (`mermaidChart.connectDiagramToMermaidChart`) — link a local diagram to Mermaid Chart.
- **Sync Diagram** (`mermaidChart.syncDiagramWithMermaid`) — only for diagrams already connected (frontmatter has `id:`). Example:
  ```yaml
  ---
  id: cbd9e9ba-a2cb-47c5-a98e-8c28a753428d
  ---
  ```

### Review Mermaid Sync
For diagrams updated by the Mermaid Chart GitHub Sync app (or pre-commit regenerate):
- **Review Mermaid Sync** (`mermaidChart.reviewAppCommits`) — start / open the review flow.
- **Regenerate with Mermaid AI** (`mermaidChart.regenerateDiagramWithMermaidAI`) — regenerate from source references.
Do not manually rewrite diagrams managed by this workflow. Accept/reject/diff UI actions stay in the extension UI.

### Install / update this pack
- **MermaidChart: Install AI Skills…** (`mermaidChart.installAiSkills`)

## @mermaid-chart slash commands

| Command | Purpose |
|---|---|
| `/generate_diagram_from_code` | General diagram from any source file |
| `/generate_execution_sequence` | Sequence diagram from code flow |
| `/generate_er_diagram` | ER diagram from schema / models |
| `/generate_cloud_architecture_diagram` | Cloud / CI-CD architecture |
| `/generate_docker_diagram` | Architecture from Dockerfiles |
| `/generate_c4_topdown_architecture` | C4 top-down architecture |
| `/analyze_code_ownership` | Code ownership diagram |
| `/generate_dependency_diagram` | Dependency / security visualisation |

## Rules

1. Always call `mermaid-diagram-validator` before showing any deliverable diagram (and on inline Output Frame Flow diagrams too, where the tool exists — see "Scope").
2. Always call `mermaid-diagram-preview` after generating a deliverable diagram.
3. Use `get-syntax-docs-mermaid` before generating an unfamiliar diagram type.
4. Prefer `@mermaid-chart` slash commands for complex generation.
5. Write deliverable diagrams to `.mmd` files; never return unvalidated Mermaid syntax (inline Output Frame Flow diagrams are exempt from the `.mmd` file and count as validated by the safe subset where no validator tool exists — see "Scope").
6. Warn the user before Repair (Mermaid AI credits).
7. Cooperate with the Sync workflow — do not manually regenerate managed diagrams.

## Docs

More commands and features: https://marketplace.visualstudio.com/items?itemName=MermaidChart.vscode-mermaid-chart
