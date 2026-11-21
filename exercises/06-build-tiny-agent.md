# Exercise 6: Build a Tiny Agent (Kiro IDE)

Understand the **agent loop** by observing and extending Kiro's behavior — no raw API calls needed.

## Goal

Learn how agents work by:
1. **Observing** Kiro's agent loop in action
2. **Building tools** (MCP servers) that Kiro uses
3. **Designing tasks** that exercise multi-step agent behavior

---

## Part 1: Observe the Agent Loop (20 min)

### The Core Pattern

Every AI agent follows this loop:
```
User Task → LLM thinks → Tool Call → Execute → Result → LLM thinks → ... → Done
```

Kiro does this automatically. Let's observe it.

### Exercise: Watch Kiro Work

1. Create a simple broken file:

```powershell
# In Kiro terminal
mkdir c:\Source\personal\learning-ai\agent-test
cd c:\Source\personal\learning-ai\agent-test
```

2. Create `calculator.py` with a bug:
```python
def add(a, b):
    return a - b  # BUG: should be +

def multiply(a, b):
    return a * b

if __name__ == "__main__":
    print(f"2 + 3 = {add(2, 3)}")  # Will print -1, should be 5
```

3. Ask Kiro: *"Read calculator.py and fix the bug"*

4. **Observe in chat:**
   - Kiro reads the file (tool call: `read_file`)
   - Kiro analyzes the code (LLM thinking)
   - Kiro edits the file (tool call: `str_replace` or `fs_write`)
   - Kiro may verify (tool call: read again or run)

**Key insight:** You didn't write the loop — Kiro IS the loop.

---

## Part 2: Extend Kiro with Custom Tools (45 min)

Since you can't call raw LLM APIs, extend Kiro's capabilities by building MCP tools it can use.

### Build a "Code Analyzer" MCP Server

This MCP gives Kiro tools to analyze Python code:

```powershell
mkdir c:\Source\personal\learning-ai\code-analyzer-mcp
cd c:\Source\personal\learning-ai\code-analyzer-mcp
uv init
uv add mcp ast-grep
```

Create `server.py`:
```python
"""
Code Analyzer MCP Server

Gives Kiro tools to analyze Python code structure.
"""

import ast
import os
from pathlib import Path
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("code-analyzer")


@mcp.tool()
def list_functions(file_path: str) -> str:
    """
    List all function names in a Python file.
    
    Use this to understand the structure of a Python file
    before making changes.
    
    Args:
        file_path: Path to the Python file to analyze
    """
    try:
        with open(file_path, 'r') as f:
            tree = ast.parse(f.read())
        
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                args = [arg.arg for arg in node.args.args]
                functions.append(f"{node.name}({', '.join(args)})")
        
        if not functions:
            return "No functions found in this file."
        
        return "Functions found:\n" + "\n".join(f"- {fn}" for fn in functions)
    except Exception as e:
        return f"Error analyzing file: {e}"


@mcp.tool()
def find_todos(directory: str = ".") -> str:
    """
    Find all TODO comments in Python files.
    
    Use this to discover incomplete work in a codebase.
    
    Args:
        directory: Directory to search (default: current directory)
    """
    todos = []
    
    for path in Path(directory).rglob("*.py"):
        try:
            with open(path, 'r') as f:
                for i, line in enumerate(f, 1):
                    if "TODO" in line or "FIXME" in line:
                        todos.append(f"{path}:{i}: {line.strip()}")
        except Exception:
            continue
    
    if not todos:
        return "No TODOs found."
    
    return "TODOs found:\n" + "\n".join(todos)


@mcp.tool()
def count_lines(file_path: str) -> str:
    """
    Count lines of code, comments, and blanks in a file.
    
    Args:
        file_path: Path to the file to analyze
    """
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        total = len(lines)
        blank = sum(1 for l in lines if not l.strip())
        comments = sum(1 for l in lines if l.strip().startswith('#'))
        code = total - blank - comments
        
        return f"File: {file_path}\n- Total lines: {total}\n- Code: {code}\n- Comments: {comments}\n- Blank: {blank}"
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    mcp.run()
```

### Connect to Kiro

Add to `.kiro/settings/mcp.json`:
```json
{
  "code-analyzer": {
    "command": "uv",
    "args": [
      "run",
      "--directory",
      "C:/Source/personal/learning-ai/code-analyzer-mcp",
      "python",
      "server.py"
    ],
    "disabled": false,
    "autoApprove": []
  }
}
```

### Test It

Ask Kiro:
- *"List all functions in calculator.py"*
- *"Find all TODOs in this project"*
- *"How many lines of code in server.py?"*

**You've extended the agent's capabilities!**

---

## Part 3: Multi-Step Agent Challenge (45 min)

### The Broken Repo Challenge

Create a project with multiple bugs. Challenge Kiro to fix them all.

```powershell
mkdir c:\Source\personal\learning-ai\broken-repo
cd c:\Source\personal\learning-ai\broken-repo
```

Create `math_utils.py`:
```python
# math_utils.py
def add(a, b):
    return a - b  # BUG 1: wrong operator

def divide(a, b):
    return a / b  # BUG 2: no zero check

def average(numbers):
    return sum(numbers) / len(numbers  # BUG 3: syntax error - missing )
```

Create `test_math.py`:
```python
# test_math.py  
import pytest
from math_utils import add, divide, average

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

def test_divide():
    assert divide(10, 2) == 5
    assert divide(9, 3) == 3

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(5, 0)

def test_average():
    assert average([1, 2, 3]) == 2.0
    assert average([10, 20]) == 15.0
```

### Challenge Kiro

Give Kiro this task:

> "Fix all bugs in the broken-repo folder. Run the tests after each fix to verify. The tests should all pass when you're done."

**Watch the agent loop:**
1. Kiro reads the files
2. Kiro runs tests → sees failures
3. Kiro fixes bug 1 → runs tests
4. Kiro fixes bug 2 → runs tests
5. Kiro fixes bug 3 → runs tests
6. All tests pass → done

---

## Key Learnings

| Concept | What You Learned |
|---------|------------------|
| **Agent Loop** | `Task → Think → Tool → Result → Think → ... → Done` |
| **Tools** | MCP servers extend what Kiro can do |
| **Multi-step** | Agent iterates until the goal is achieved |
| **Verification** | Running tests is how agents know they're done |

---

## Reflection Questions

1. **How did Kiro decide which tool to use?** (The LLM chooses based on tool descriptions)
2. **What happens if Kiro's fix doesn't work?** (It sees the error and tries again)
3. **How is this different from a simple script?** (Agent adapts; script is static)

---

## What's Missing From Kiro That You'd Build?

If you WERE building from scratch, you'd need:
- Tool definitions (JSON schema) ← *You did this in MCP*
- Agent loop (LLM → tool → result → LLM) ← *Kiro does this*
- Stop condition (when to finish) ← *Kiro decides*
- Error handling ← *Kiro retries*

**The core insight:** Building an agent is mostly about the loop + good tools. Kiro handles the loop; you focus on tools.
