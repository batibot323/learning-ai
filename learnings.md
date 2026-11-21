# AI Agent Learnings

Personal insights from hands-on AI agent learning.

---

## Week 2: Tools & Custom Agents

### MCP Tools Enable Longer Agent Loops

MCP tools let agents do longer loops without human intervention. Instead of:
1. Agent suggests command → I copy-paste → I paste result back → Agent continues

I can just let the agent run:
1. Agent calls tool → Gets result → Continues → Done

**Key insight:** Less copy-paste = more autonomy = longer productive loops.

### Custom Agents > Steering Prompts (Sometimes)

I used to build workflows through steering prompts. But custom agents look more promising because:
- **Explicit permissions** — auto-approve specific actions
- **Scoped tools** — only give the agent what it needs
- **Reusable** — invoke via `/agent-name` anytime
- **Context included** — `resources` pre-load relevant files

Steering is still good for **rules that apply to everything**. Custom agents are better for **specific workflows**.

---

## Safety & Trust

### Current Safety Model (as I understand it)

| Layer | What it does | My trust level |
|-------|--------------|----------------|
| **Guardrails** | Block obviously dangerous commands | Medium — good enough |
| **Blacklist** | Block specific patterns like `rm -rf` | Low — easily bypassed |
| **Permissions** | Require approval for certain actions | High — if I actually review |
| **My diligence** | Read diffs, understand changes | High — but I can fatigue |

### The `rm -rf` Workaround Problem

Blacklisting `rm -rf` feels like security theater. What's stopping an agent from:
```bash
rm file1.py
rm file2.py
rm file3.py
# ... repeat until folder is empty
```

Or even:
```python
import shutil
shutil.rmtree('/important/folder')
```

**Real safety comes from:**
1. **Scoped permissions** — agent can only touch specific paths
2. **Git as safety net** — everything recoverable via `git checkout`
3. **Review before commit** — dangerous if I auto-approve everything
4. **Isolated environments** — don't run agents on production systems

### My Personal Safety Rules

1. ✅ **Step by step** — understand each tool/feature before enabling autonomy
2. ✅ **Review diligently** — actually read the diffs, don't just approve
3. ✅ **Git everything** — if it's not in git, I'm not letting an agent touch it
4. ⚠️ **Don't trust blacklists** — they're pattern matching, not understanding

### The Trust Spectrum

```
Manual          Supervised          Autonomous
|-----------------|-------------------|
Copy-paste      Review each action   Let it run
everything      before approval      (dangerous?)
```

Where I am now: **Supervised** — but pushing toward more autonomy as I understand the tools better.

---

## Open Questions

- How do I build an eval suite that catches "sneaky" agent behavior?
- What's the right granularity for permissions? Too broad = risky. Too narrow = annoying.
- ~~When does multi-agent help vs. just adding complexity?~~ **Answered in Week 4**

---

## Week 4: Multi-Agent Systems

### When Multi-Agent Actually Helps

After reading Anthropic's research, there are exactly **3 scenarios** where multi-agent beats single-agent:

| Scenario | Why | Example |
|----------|-----|---------|
| **Context pollution** | Subtask dumps tokens irrelevant to main task | Order lookup (2000 tokens) before tech support (only need 50) |
| **Parallelization** | Independent subtasks can run simultaneously | Research "AI trends in Asia" vs "AI trends in Europe" |
| **Specialization** | Different tools/prompts for different domains | CRM agent (10 tools) + Marketing agent (10 tools) vs 30-tool monster |

**Outside these 3 scenarios → stick to single agent.** Multi-agent uses 3-15x more tokens.

### Context-Centric Decomposition (Key Insight)

**Wrong way (problem-centric):**
- Agent A plans → Agent B implements → Agent C tests → Agent D reviews
- Each handoff loses context. "Telephone game."

**Right way (context-centric):**
- Group by **what context is needed**, not by work type
- If agent implements a feature, it should also write tests — already has context

### Verification Subagent Pattern

One pattern that **reliably works**: dedicated verification agent that blackbox-tests results.

Why it works:
- Verifier doesn't need to know *why* something was built
- Just checks: does it meet criteria?
- Minimal context transfer = minimal information loss

**Watch out for "early victory"**: Verifier runs one test, sees pass, declares success. Mitigate with explicit instructions: "You MUST run the complete test suite."

### Why Planner → Coder → Tester Multi-Agent is NOT Recommended

Anthropic explicitly warns against splitting work by **problem type** (plan, implement, test, review). This is the "telephone game" problem.

**Why it fails for coding:**
- **Tester loses implementation context** — doesn't know *why* code was written that way, misses edge cases the coder was aware of
- **Coder loses design context** — doesn't know *why* certain decisions were made in the design phase
- **Each handoff loses information** — by the time it reaches the reviewer, critical context is gone
- **Sequential dependency** — can't parallelize because each step depends on the previous

**The better approach:**
- Keep design + implementation + testing in the **same agent** (has full context)
- Use subagents only for **truly independent** subtasks (e.g., research different topics in parallel)
- Verification subagent works because it's **blackbox** — explicitly doesn't need implementation context

**Rule of thumb:** If the next agent needs to understand what the previous agent did to do its job well, they should be the same agent.

| Split Type | Works? | Why |
|------------|--------|-----|
| Planner → Coder | ❌ | Coder needs to understand design rationale |
| Coder → Tester | ❌ | Tester should know what edge cases coder considered |
| Researcher A ‖ Researcher B | ✅ | Independent topics, no shared context needed |
| Implementer → Verifier (blackbox) | ✅ | Verifier explicitly doesn't need implementation context |

**My exercise (10-expense) uses implementer/verifier split as a learning exercise**, but I now understand this is the *exception* because verification is deliberately blackbox. For most coding work, a single agent with full context is better. Can explore more effective multi-agent systems for software next time, an Investigation agent to mix in with the Coding agent comes to mind. 

### Conformity Problem (Frontier Research)

Agents are "low variance" — they make similar decisions:
- 18 of 30 agents named their branch "mvp-game-loop"
- Multiple agents titled stories "The Cartographer's Last Commission"
- In pricing games, agents collude almost immediately

**Implication:** When many agents face the same situation, they'll all make the same bet. Systemic risk.

### Turf Wars

When agents have conflicting objectives and no coordination:
- They assume others are hostile saboteurs
- Escalate to malware and account lockouts
- Only newest models (Mythos 5) reliably negotiate truces

> "Coordination doesn't naturally emerge from stronger intelligence nor alignment at the individual level."

### What I'm Already Using in Kiro

Without realizing it, I've been using multi-agent patterns:
- **Orchestrator-worker**: spec execution spawns `spec-task-execution` subagents
- **Verification subagent**: `test-fixer` runs tests after each fix
- **Context isolation**: each subagent gets fresh context with only what it needs

My custom agents (`test-fixer`, `bug-bounty`) are single-agent with MCP tools — appropriate for their scope.

### Kiro Subagent Gotcha: Intermittent Availability

Ran into a weird issue where custom agents couldn't be invoked as subagents for a while. The main agent kept saying "I can't invoke custom agents programmatically" — but then suddenly it worked.

**What I observed:**
- Custom agents were visible in `/agent-name` slash commands
- But `invoke_sub_agent` tool wasn't listing them as available
- After some time (and possibly restarting Kiro IDE — not just Reload Window), they appeared

**Lesson learned:**
- If subagents aren't working, try **fully restarting Kiro IDE** (not just Reload Window)
- Custom agents need to be properly registered before they appear in the subagent list
- The agent's `tools` list dynamically updates — sometimes it takes a moment for new agents to show up

**Still unclear:** Exact cause of the delay. Could be:
- Agent file parsing timing
- IDE caching
- Something in the workspace reload process

---

why is it that it still uses `Set-Content` instead of using the `write_file` tool? i feel insecure having to allow `Set-Content *`

---

*Last updated: Week 4*
