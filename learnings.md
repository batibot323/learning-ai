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

---

*Last updated: Week 4*
