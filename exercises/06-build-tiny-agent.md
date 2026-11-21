# Exercise 6: Build a Tiny Agent (Kiro Custom Agents) ✅ COMPLETED

Build your own specialized agent using Kiro's Custom Agents feature.

## Goal

Learn how agents work by **actually building one**:
1. ✅ **Observe** Kiro's agent loop in action (Part 1 - DONE)
2. ✅ **Extend** capabilities with MCP tools (Part 2 - DONE)
3. ✅ **Test** multi-step agent behavior (Part 3 - DONE)
4. ✅ **Build** your own custom agent (Part 4 - DONE)

---

## Part 1: Observe the Agent Loop ✅ COMPLETED

### What We Did
- Created `agent-test/calculator.py` with a bug
- Asked Kiro to fix it
- Observed the agent loop: Read → Think → Edit → Done

### Key Insight
The agent loop is: `Task → LLM thinks → Tool Call → Execute → Result → LLM thinks → ... → Done`

---

## Part 2: Extend Kiro with Custom Tools ✅ COMPLETED

### What We Did
- Built `code-analyzer-mcp` with 3 tools:
  - `list_functions` — lists functions in a Python file
  - `find_todos` — finds TODO comments
  - `count_lines` — counts lines of code
- Connected it to Kiro via `mcp.json`
- Tested: "List all functions in calculator.py" → worked!

### Key Insight
MCP tools extend what an agent can do. You define **what** the tool does; the agent decides **when** to use it.

---

## Part 3: Multi-Step Agent Challenge ✅ COMPLETED

### What We Did
- Created `broken-repo/` with buggy `math_utils.py` and `test_math.py`
- Asked Kiro to fix tests one by one
- Watched the iterative loop: Run tests → Fix → Verify → Repeat

### Key Insight
Agents iterate until the goal is achieved. Tests provide the stop condition.

---

## Part 4: Build a Custom Agent ✅ COMPLETED

We **actually built agents** — not just observed Kiro, but created specialized agents with custom tools, permissions, and behavior.

### What We Built

**1. test-fixer agent** (`.kiro/agents/test-fixer.md`)
- Fixes failing tests one at a time
- Auto-runs pytest, auto-writes .py files
- Iterates: run tests → fix → verify → repeat

**2. bug-bounty agent** (`.kiro/agents/bug-bounty.md`)
- Goofy agent that charges for bug fixes
- Uses DragonPay MCP to create payment requests
- 1 line of code = 1 peso
- Demonstrates using `@mcp` tools with `includeMcpJson: true`

### Key Learnings from Part 4

| What We Learned | Example |
|-----------------|---------|
| Agent file structure | Frontmatter (YAML) + Prompt (Markdown) |
| Using MCP in agents | `tools: ["@mcp"]` + `includeMcpJson: true` |
| Invoking as subagent | `/agent-name` slash commands |
| Permissions | Auto-approve specific shell commands |

### What is a Kiro Custom Agent?

A custom agent is a configuration file that defines:
- **Tools** — what the agent can do
- **Permissions** — what it's allowed to do automatically
- **Prompt** — how it should behave
- **Resources** — what context it automatically includes

### Step 1: Create the Agent File

Create `.kiro/agents/test-fixer.md`:

```powershell
mkdir .kiro\agents
```

Then create the file with this content:

```markdown
---
name: test-fixer
description: Fixes failing tests one at a time, verifying each fix
model: claude-sonnet-4.6
tools: ["read", "write", "shell"]
permissions:
  rules:
    - capability: shell
      match: ["uv run pytest*", "python -m pytest*"]
      effect: allow
    - capability: fs_write
      match: ["*.py"]
      effect: allow
resources:
  - "file://broken-repo/**/*.py"
---

You are a test-fixing agent. Your workflow:

1. Run `uv run pytest -v` to see which tests fail
2. Read the failing test and the code it tests
3. Fix ONE bug at a time
4. Run tests again to verify
5. Repeat until all tests pass

Rules:
- Fix only one bug per iteration
- Always run tests after each fix
- Explain what you fixed and why
- Stop when all tests pass
```

### Step 2: Understand What You Built

| Field | What it does |
|-------|--------------|
| `name` | How you'll select this agent |
| `description` | Shows in agent picker |
| `model` | Which LLM to use |
| `tools` | `read`, `write`, `shell` — the capabilities |
| `permissions` | Auto-approve pytest and .py file writes |
| `resources` | Auto-include broken-repo files in context |
| `prompt` | The agent's personality and workflow |

### Step 3: Reset the Broken Repo

First, let's re-break the code so you can test your agent:

```python
# broken-repo/math_utils.py
def add(a, b):
    return a - b  # BUG: wrong operator

def divide(a, b):
    return a / b  # BUG: no zero check
```

### Step 4: Switch to Your Custom Agent

1. Look at the bottom of the chat input — you'll see "Default" or similar
2. Click it to open the agent picker
3. Select **test-fixer**
4. Your custom agent is now active!

### Step 5: Test Your Agent

Now just say:

> "Fix the failing tests"

Watch your custom agent:
1. Automatically run pytest (because of permissions)
2. Read the test file (because of resources)
3. Fix bugs one by one
4. Verify each fix

**You built this behavior!**

---

## Part 5: Advanced — Agent Variations (SKIPPED - Read Only)

Reviewed the patterns but skipped hands-on. Key takeaways:

- **Security Reviewer**: read-only agent, reports but doesn't modify
- **Documentation Agent**: write access only to .md files

These show how permissions shape agent behavior.

### Security Reviewer Agent

```markdown
---
name: security-reviewer
description: Reviews code for security issues
model: claude-sonnet-4.6
tools: ["read"]
permissions:
  rules:
    - capability: fs_read
      effect: allow
---

You are a security-focused code reviewer. Look for:
- SQL injection
- XSS vulnerabilities  
- Hardcoded secrets
- Insecure dependencies

Report issues but DO NOT modify code.
```

### Documentation Agent

```markdown
---
name: doc-writer
description: Generates documentation for code
model: claude-sonnet-4.6
tools: ["read", "write"]
permissions:
  rules:
    - capability: fs_write
      match: ["*.md", "docs/**"]
      effect: allow
---

You write documentation. For each function:
- Describe what it does
- Document parameters and return values
- Provide usage examples

Write docs in markdown format.
```

---

## Key Learnings

| Concept | What You Learned |
|---------|------------------|
| **Agent Definition** | Tools + Permissions + Prompt + Resources |
| **Tools** | What the agent CAN do |
| **Permissions** | What it can do WITHOUT asking |
| **Prompt** | How it SHOULD behave |
| **Resources** | What context it STARTS with |

---

## Reflection Questions

1. **What's the difference between MCP tools and agent tools?**
   - MCP tools = new capabilities you build
   - Agent tools = which built-in/MCP tools this agent can access

2. **Why are permissions important?**
   - Without them, agent asks for approval every action
   - With them, agent can work autonomously

3. **How does the prompt affect behavior?**
   - Same tools, different prompt = different workflow
   - The prompt is the agent's "personality"

---

## What You Actually Built

You didn't just observe an agent — you **configured** one:

| Component | You Defined |
|-----------|-------------|
| Capabilities | `tools: ["read", "write", "shell"]` |
| Autonomy | `permissions` for pytest and .py writes |
| Behavior | Prompt: "Fix one bug at a time" |
| Context | `resources` pointing to broken-repo |

This is **agent building** — defining what an agent can do, how it should behave, and what it knows about.

---

## Next Steps ✅ COMPLETED

- [x] Create the test-fixer agent
- [x] Test it on broken-repo
- [x] Create a second specialized agent (bug-bounty with DragonPay MCP)
- [x] Try combining agents with MCP tools you built
