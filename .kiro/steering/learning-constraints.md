# Learning AI Project Constraints

## Environment
- **IDE:** Kiro IDE only — do NOT use Claude Code, Anthropic API directly, or OpenAI API
- **Can read:** Anthropic blogs, documentation, videos
- **Can run:** Only Kiro IDE

## When Creating Exercises
- All hands-on exercises must be doable within Kiro IDE
- Don't suggest installing `anthropic` or `openai` Python packages for direct API calls
- Use Kiro's built-in agent capabilities instead of building agents from scratch with raw APIs

## Learner Profile
- Engineering manager with technical chops
- Learns fast by reading and watching excellent videos
- Cadence: 1-2 weeks intensive, weekday evenings for reading, weekends for hands-on

---

## Step 10: Multi-Agent Systems — Loosened Constraints

For the verification subagent exercise, we're loosening constraints to allow:

### Allowed for This Exercise
- **Calling external APIs** that I explicitly approve (e.g., test endpoints, localhost services)
- **Integration/E2E testing** over unit tests — we care about user-visible behavior
- **Browser automation tools** (Playwright, Selenium) via MCP if needed
- **ngrok or localhost** for exposing services to test

### Exercise Plan: E2E UAT Verification Agent

**Goal:** Build a verification subagent that runs integration tests against a real app, not unit tests.

**Workflow:**
```
0. Create specs (human-agent loop)
1. Build simple MVP (product TBD)
2. Write integration tests (human verifies test quality)
3. Agent creates features → tasks from specs
4. Agent iterates: implement → run E2E tests → fix → repeat
5. Expose via localhost (ngrok if needed for external services)
```

**Why this approach:**
- **High-level testing** = test what user sees, not implementation details
- **Verification subagent pattern** = fresh context, blackbox testing
- **Avoids "early victory"** = E2E tests are harder to fake passing

### Product MVP Ideas (pick one)
1. **Todo app** — classic, boring, but well-understood domain
2. **Expense tracker** — slightly more interesting, has data validation
3. **Simple blog/CMS** — good for testing CRUD + auth flows
4. **Webhook receiver** — tests async behavior, good for MCP integration

### Tech Stack Suggestions
- **Backend:** FastAPI (Python, quick to prototype)
- **Frontend:** Simple HTML or htmx (avoid React complexity for learning)
- **Testing:** Playwright (can run headless, good Python bindings)
- **Exposure:** localhost first, ngrok if testing external callbacks
