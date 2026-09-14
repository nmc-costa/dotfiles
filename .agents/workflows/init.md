---
description: Analyzes the project and creates a tailored GEMINI.md file
---

1. **Analyze the Project**:
   - List the files in the root directory to identify project type (Node, Python, etc.).
   - Read `README.md` (if present) to understand the project goal.
   - Read configuration files like `package.json`, `requirements.txt`, `pyproject.toml`, `cargo.toml` to identify dependencies.
   - Identify key directories (e.g., `src`, `app`, `lib`).

2. **Generate GEMINI.md**:
   - Create a file named `GEMINI.md` in the root directory.
   - The file MUST contain the following sections:
     - **Project Overview**: A summary of what the project does.
     - **Tech Stack**: Languages, frameworks, and key libraries used.
     - **Key Files**: Important files and their purposes.
     - **Setup & Run**: Instructions on how to install dependencies and run the project.
     - **Conventions**: Any coding styles or patterns observed (or standard ones for the stack).
   - **CRITICAL**: The content must be specific to *this* project, not generic placeholders.

3. **Confirmation**:
   - Output a message confirming the file has been created and asking the user to review it.
