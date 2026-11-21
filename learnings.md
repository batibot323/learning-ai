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
- When does multi-agent help vs. just adding complexity?

---

*Last updated: Week 2*
