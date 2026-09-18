---
name: [TOOL_NAME]
description: "[Brief description of what this tool does]"
version: "1.0"
type: "[api|library|script|service]"
language: "[python|javascript|bash|multi]"
dependencies:
  - "[package-name]"
  - "[another-package]"
---

# [Tool Name]

**Purpose**: [One-sentence description of what this tool integrates]

**Type**: External service / Library / API  
**Integration**: How agents access this tool

---

## What This Tool Provides

[Description of the tool's capabilities and what agents can do with it]

### Key Features

- **Feature 1**: [Description]
- **Feature 2**: [Description]
- **Feature 3**: [Description]

---

## Installation

### Prerequisites
```bash
# What needs to be installed first
python >= 3.9
pip install [package-name]
```

### Setup
```bash
# How to set up the tool
git clone [repo-url]
cd [tool-name]
pip install -r requirements.txt
```

### Configuration
```bash
# Environment variables or config files needed
export API_KEY="your-key-here"
export API_ENDPOINT="https://api.example.com"
```

---

## Usage

### Basic Example
```python
from tools.tool_name import ToolClass

tool = ToolClass(api_key="your-key")
result = tool.do_something(input_data)
print(result)
```

### Advanced Example
```python
# More complex usage pattern
tool = ToolClass(api_key="your-key", config="advanced.json")
result = tool.complex_operation(
    param_1="value_1",
    param_2="value_2",
    streaming=True
)
```

---

## API Reference

### Methods

#### `method_name(param1, param2)`
```
Description of what this method does

Parameters:
  - param1 (type): Description
  - param2 (type): Description

Returns:
  - type: Description of return value

Example:
  result = tool.method_name("value1", "value2")
```

---

## Error Handling

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `AuthError` | API key invalid | Check environment variable |
| `ConnectionError` | API endpoint down | Check service status |
| `RateLimitError` | Too many requests | Implement exponential backoff |

---

## Agents That Use This Tool

This tool is used by:
 HEAD
- `agent-name` (see `../../agents/{agent-name}/`) — For {capability}
- `agent-name-2` (see `../../agents/{agent-name-2}/`) — For {capability}
 origin/main

---

## Related Resources

- Documentation: [Official docs](https://docs.example.com)
- GitHub: [Repository](https://github.com/example/tool-name)
 HEAD
- Examples: `examples/` (see `./examples/`)
 origin/main
- Registry: `.agents/skills/` (no central registry file in this repo; browse skill directories directly)

---

**Status**: Template (Customize for your tool)  
**Version**: 1.0  
**Last Updated**: 2026-08-25
