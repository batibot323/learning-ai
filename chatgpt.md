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

## Week 2 — Context + Tools (in progress)

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

### 6. Build a Tiny Agent
- **Guide:** [exercises/06-build-tiny-agent.md](exercises/06-build-tiny-agent.md)
- **No framework** — just the core loop
- **Progression:**
  1. **Part 1 (30 min):** Single tool (`read_file`) + agent loop
  2. **Part 2 (30 min):** Add `list_files`, `write_file`
  3. **Part 3 (1 hour):** Fix a deliberately broken repo
- **Core pattern:** `LLM → Tool Call → Execute → Result → LLM → Done`
- **Tools:** `read_file`, `list_files`, `write_file`, `run_tests`

---

## Week 3 — Evals

### 7. Study Evals
- **Read:** [Anthropic — Demystifying Evals for AI Agents](https://www.anthropic.com/research/demystifying-evals-for-ai-agents)
- **Learn:** test cases, graders, result vs trajectory evaluation

### 8. Build an Eval Suite
- Create 10–20 coding tasks for your agent
- **Measure:**
  - Success rate
  - Tests passing
  - Unnecessary changes
  - Tool misuse

### 9. Compare Strategies
- Test different prompts/context
- Measure rather than judging subjectively
- Find out what actually improves agent performance

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
