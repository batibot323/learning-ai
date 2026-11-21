# AI Agent Learning Plan

## Week 1 — Agent Fundamentals ✅

### 1. Building Effective Agents ✅
- **Read:** [Anthropic — Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- **Focus:** workflows vs agents, agent loops, tools, orchestration
- **Do:** Classify 5 real engineering tasks as workflow vs agent

### 2. Barry Zhang Talk ✅
- **Watch:** [How We Build Effective Agents](https://www.youtube.com/watch?v=D7_ipDqhtwk)
- **Focus:** How agents reason + use tools
- **Do:** Explain the difference between an LLM and an agent loop

### 3. Use Your Coding Agent ✅
- Pick a real medium-sized task
- Run it 3 ways:
  - Minimal instructions
  - Detailed instructions
  - Mostly autonomous
- Note where/why it succeeds or fails

---

## Week 2 — Context + Tools ✅ COMPLETED

### 4. Context Engineering ✅ (read/learn — observed through daily work)
- **Read:** [Anthropic — Effective Context Engineering for AI Agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)
- **Learn:** context window, tool results, retrieval, progressive disclosure, context pollution
- **Do:** Solve the same task with different amounts/types of context and compare results

### 5. Tool Use / MCP ✅
- **Read:** [MCP Introduction](https://modelcontextprotocol.io/) + [Anthropic — Writing Effective Tools for AI Agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
- **Learn:** tools, resources, prompts; tool design and permissions
- **Do:** Design 5–10 AI-facing tools for a system you know well
- **Done:**
  - Connected `fetch` and `filesystem` MCP servers
  - Built custom `time-tools` MCP server (get_current_time, convert_time)
  - Built custom `dragonpay-test` MCP server (create_payment, check_payment_status)
  - Learned: MCP SDK v2 API changes, `.env` credential handling, mcp.json config
- **Note:** DragonPay isn't an ideal MCP use case. Better MCP ideas to explore:
  1. **Transaction search API** — search txns based on filters
  2. **Azure SQL audit logs** — query using KQL
  3. **GitHub reviewer** — read through PRs/issues needing my review

### 6. Build a Tiny Agent ✅
- **Guide:** [exercises/06-build-tiny-agent.md](exercises/06-build-tiny-agent.md)
- **Progression:**
  1. ✅ **Part 1:** Observed agent loop — `Read → Think → Edit → Done`
  2. ✅ **Part 2:** Built `code-analyzer-mcp` with `list_functions`, `find_todos`, `count_lines`
  3. ✅ **Part 3:** Multi-step agent challenge — iterative test fixing
  4. ✅ **Part 4:** Built custom Kiro agents:
     - `test-fixer` — fixes failing tests one at a time
     - `bug-bounty` — charges for bug fixes via DragonPay MCP (goofy!)
  5. ✅ **Part 5:** Reviewed security-reviewer and doc-writer patterns (read only)
- **Key learnings:**
  - Agent = Tools + Permissions + Prompt + Resources
  - Use `@mcp` + `includeMcpJson: true` to access MCP servers in custom agents
  - Invoke via `/agent-name` slash commands
- **Core pattern:** `LLM → Tool Call → Execute → Result → LLM → Done`

---

## Week 3 — Evals

### 7. Study Evals ✅
- **Read:** [Anthropic — Demystifying Evals for AI Agents](https://www.anthropic.com/research/demystifying-evals-for-ai-agents)
- **Learn:** test cases, graders, result vs trajectory evaluation
- **Key concepts:**
  - Task, trial, grader, transcript, outcome
  - Code-based vs model-based vs human graders
  - pass@k (at least 1 success) vs pass^k (all succeed)
  - Capability evals (what can it do?) vs regression evals (does it still work?)
  - 8-step roadmap: start early, unambiguous tasks, balanced sets, robust harness, thoughtful graders, check transcripts, monitor saturation, maintain long-term

### 8. Build an Eval Suite — DEFERRED
- **Status:** Skipping hands-on for now
- **Why:** Not yet building full AI agent bots for users. For internal coding agents, existing tests/CI/PR reviews serve as the eval.
- **When to revisit:** If/when building AI features for customers or chatbots at scale
- **Note:** Good knowledge to have — there's a team building AI chatbot, this will be relevant for them
- **Guide created:** [exercises/08-build-eval-suite.md](exercises/08-build-eval-suite.md) (ready when needed)

### 9. Compare Strategies — DEFERRED
- **Status:** Skipping hands-on for now
- **Why:** Depends on having an eval suite first
- **When to revisit:** After building eval suite if/when needed

---

## Week 4 — Advanced Agents

### 10. Multi-Agent Systems
- **Read:** [Anthropic — How We Built Our Multi-Agent Research System](https://www.anthropic.com/research/multi-agent-research-system)
- **Do:** Build planner → coder → reviewer
- **Ask:** When does multiple agents actually help?

### 11. Long-Running Agents
- **Read:** [Anthropic — Effective Harnesses for Long-Running Agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents)
- **Learn:** state, checkpoints, summaries, recovery
- **Do:** Make your agent stop/resume a multi-step task

### 12. AI-Native SDLC
- Map your team's current SDLC
- For each stage ask:
  - What can agents automate?
  - What becomes more important?
  - Where does verification need to happen?
- Produce your own proposed AI-assisted SDLC
