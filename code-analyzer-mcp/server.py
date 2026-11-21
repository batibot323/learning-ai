"""
Code Analyzer MCP Server

Gives Kiro tools to analyze Python code structure.
"""

import ast
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
