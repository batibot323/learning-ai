# Exercise 5: Tool Use / MCP — Kiro Edition

This exercise adapts Anthropic's "Writing effective tools for agents" to work with Kiro IDE.

## What You'll Learn

The Anthropic article teaches three things:
1. **How to build and test tool prototypes** (Claude Code-specific)
2. **How to evaluate tools with agents** (evaluation framework)
3. **Principles for effective tool design** (universal)

In Kiro, you can do all three — just with different mechanics.

---

## Part 1: Understand MCP in Kiro

**Read first:**
- [MCP Introduction](https://modelcontextprotocol.io/)
- [Anthropic — Writing Effective Tools for AI Agents](https://www.anthropic.com/engineering/writing-tools-for-ag    ents)

**Key concept:** MCP (Model Context Protocol) is how AI agents connect to external tools. Kiro supports MCP natively — you configure MCP servers in `.kiro/settings/mcp.json`.

---

## Part 2: Build a Prototype MCP Server

### Option A: Use an existing MCP server

Kiro comes with access to community MCP servers. Try connecting one:

1. Open Command Palette → "MCP" → Open MCP settings
2. Or create/edit `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "uvx",
      "args": ["mcp-server-filesystem", "/path/to/allowed/directory"],
      "disabled": false
    }
  }
}
```

3. Test it by asking Kiro to use the tool (e.g., "list files in /path/to/directory")

**Note:** You need `uv` installed. See: https://docs.astral.sh/uv/getting-started/installation/

### Option B: Build your own MCP server

Create a simple MCP server in Python or TypeScript. Here's a minimal Python example:

**File: `my-mcp-server/server.py`**
```python
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

server = Server("my-tools")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="get_project_status",
            description="Returns the current status of a project by name. Use this when the user asks about project health, progress, or blockers.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": "The name of the project (e.g., 'backend-api', 'mobile-app')"
                    }
                },
                "required": ["project_name"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get_project_status":
        # Mock implementation — replace with real logic
        project = arguments.get("project_name", "unknown")
        return [TextContent(
            type="text",
            text=f"Project '{project}': On track. 3 tasks remaining. No blockers."
        )]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with mcp.server.stdio.stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

**Connect it to Kiro:**
```json
{
  "mcpServers": {
    "my-tools": {
      "command": "python",
      "args": ["my-mcp-server/server.py"],
      "disabled": false
    }
  }
}
```

---

## Part 3: Test Your Tools

### Manual testing in Kiro

Once connected, test by prompting Kiro:
- "What's the status of the backend-api project?"
- "Get me the project status for mobile-app"

Observe:
- Did Kiro call the right tool?
- Did it pass the right parameters?
- How did it interpret the response?

### Structured testing

Create test cases like the article suggests. Document them:

| Prompt | Expected tool call | Expected behavior |
|--------|-------------------|-------------------|
| "How's the backend-api project doing?" | `get_project_status(project_name="backend-api")` | Returns status, Kiro summarizes |
| "Is mobile-app on track?" | `get_project_status(project_name="mobile-app")` | Returns status, Kiro answers yes/no |
| "What are the blockers on frontend?" | `get_project_status(project_name="frontend")` | Returns status, Kiro extracts blockers |

Run each prompt, note results, identify failures.

---

## Part 4: Apply Tool Design Principles

The article's principles apply directly. Practice them:

### 1. Choose the right tools (don't wrap everything)

❌ Bad: `list_all_projects`, `get_project_by_id`, `get_project_tasks`, `get_task_blockers`  
✅ Good: `get_project_status` (consolidates useful info)

**Exercise:** For a system you know, list 10 API endpoints. Now design 3-5 tools that would actually help an agent accomplish tasks.

### 2. Namespace your tools

If you have multiple tools, prefix them:
- `project_get_status`
- `project_create`
- `calendar_schedule_meeting`
- `calendar_find_availability`

### 3. Return meaningful context

❌ Bad response:
```json
{"id": "a1b2c3d4", "status_code": 1, "updated_at": 1699488000}
```

✅ Good response:
```
Project 'backend-api': On track. 3 tasks remaining. Last updated: Nov 8.
No blockers reported.
```

### 4. Optimize for tokens

- Paginate large results
- Offer `response_format` parameter ("concise" vs "detailed")
- Truncate with helpful messages: "Showing first 10 results. Use `search_projects(query='...')` to narrow down."

### 5. Prompt-engineer descriptions

Your tool description IS the documentation for the agent. Make it explicit:

❌ Vague:
```
"description": "Gets project info"
```

✅ Clear:
```
"description": "Returns the current status of a project including progress, remaining tasks, and blockers. Use this when the user asks about project health or what's blocking a project. Pass the project name exactly as it appears in the system (e.g., 'backend-api', 'mobile-app')."
```

---

## Part 5: Design Exercise

**Your task:** Design 5-10 AI-facing tools for a system you know well.

Pick something real:
- Your team's deployment pipeline
- Your incident response process
- A microservice you own
- Your sprint/project management workflow

For each tool, document:

### Tool 1: [name]
- **Name:** `[tool_name]`
- **Description:** [What an agent needs to know to use it correctly]
- **Parameters:**
  - `param_name` (type, required/optional): description
- **Returns:** [What the agent gets back]
- **Example call:** `tool_name(param="value")`
- **Example response:** [sample output]
- **Failure modes:** [What can go wrong, how agent should handle it]

### Why this tool?
- What task does it enable?
- What existing API/endpoints does it consolidate?
- How is it better than just exposing raw APIs?

---

## Part 6: Optional — Build One for Real

Take your best tool design and actually implement it as an MCP server. Connect it to Kiro. Test it with real prompts.

This is where the learning becomes concrete.

---

## Reflection Questions

After completing this exercise:

1. What's the difference between designing a tool for a developer vs. for an AI agent?
2. Why do consolidated, task-oriented tools work better than thin API wrappers?
3. How does context window limitation change how you design tool responses?
4. What makes a good tool description?

---

## Resources

- [MCP Specification](https://modelcontextprotocol.io/specification/2025-06-18)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Kiro MCP Configuration](https://kiro.dev/docs/mcp) (check current docs)
- [Anthropic Tool Use Docs](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview)
