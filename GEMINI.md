# GEMINI.md

## Project Overview

This repository is a collection of Python-based projects, primarily focused on data science, machine learning, and MLOps. The projects are organized into subdirectories, with `my` and `dtx` being the main project folders.

The repository emphasizes a structured approach to code management and collaboration, with the `HIcode` framework being a central piece. This framework promotes best practices like DRY, KISS, consistency, and testing.

### Key Projects

*   **`my/HIcode`**: A foundational framework for structuring Python projects, particularly in data science and data engineering. It provides guidelines and a template for creating maintainable and scalable codebases.
*   **`dtx/repos/mobai`**: A data-intensive project that utilizes the `HIcode` framework. It incorporates `pyspark` and `tensorflow`, suggesting a focus on large-scale data processing and machine learning.
*   **`dtx/repos/sp_xai_nos`**: A proof-of-concept (PoC) for an explainable AI (XAI) framework focused on soccer highlight detection. It uses Streamlit for the user interface and integrates various XAI techniques (SHAP, LIME) and Large Language Models (LLMs).

## Building and Running

The projects in this repository are Python-based and generally follow a similar setup and execution process.

### Dependencies

Each project has a `requirements.txt` file that lists its dependencies. You can install them using `pip`:

```bash
pip install -r path/to/project/requirements.txt
```

### Installation

The projects are designed to be installed as editable packages. This allows you to make changes to the code and have them reflected immediately. To install a project, navigate to its root directory and run:

```bash
pip install -e .
```

### Running the Projects

The execution method varies depending on the project:

*   **`my/HIcode`**: This is a framework and not a runnable application itself. You can explore the `prototype/tutorial.ipynb` notebook to understand its usage.
*   **`dtx/repos/mobai`**: Similar to `HIcode`, this project is likely a library or a collection of scripts. Refer to its documentation for specific usage instructions.
*   **`dtx/repos/sp_xai_nos`**: This is a Streamlit application. To run it, execute the following command from the project's root directory:

    ```bash
    streamlit run src/deployment/user_interfaces/main.py
    ```

## Development Conventions

The repository promotes a set of development conventions, largely defined by the `HIcode` framework:

*   **DRY (Don't Repeat Yourself)**: Minimize code duplication.
*   **KISS (Keep It Simple)**: Keep the code as simple as possible.
*   **Consistency**: Follow consistent coding styles and project structures.
*   **Testing**: Write tests to ensure code quality and prevent regressions.

The `.github/prompts/agents_base_intructions.prompt.md` file also provides a set of instructions for AI agents and automated workflows, which can be a good source of information on the expected development practices.
