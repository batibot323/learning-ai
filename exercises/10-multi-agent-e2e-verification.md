# Exercise 10: Multi-Agent E2E Verification System

Build a multi-agent system where agents collaborate to implement features with E2E test verification. This exercises the **verification subagent pattern** with real integration tests.

---

## Learning Goals

1. **Orchestrator-subagent pattern** — lead agent coordinates specialized workers
2. **Verification subagent** — blackbox testing with fresh context
3. **Context-centric decomposition** — keep related work in the same agent
4. **E2E testing** — test what users see, not implementation details
5. **Iteration loops** — implement → test → fix → repeat

---

## The System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        HUMAN (You)                               │
│  - Create specs (requirements)                                   │
│  - Verify E2E test quality                                       │
│  - Approve major decisions                                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR AGENT                            │
│  - Reads specs                                                   │
│  - Breaks down into tasks                                        │
│  - Dispatches to implementer                                     │
│  - Dispatches to verifier                                        │
│  - Handles iteration loop                                        │
└─────────────────────────────────────────────────────────────────┘
                    │                       │
                    ▼                       ▼
┌──────────────────────────┐    ┌──────────────────────────┐
│   IMPLEMENTER AGENT      │    │   VERIFIER AGENT         │
│                          │    │                          │
│  - Writes code           │    │  - Runs E2E tests        │
│  - Has full context      │    │  - NO implementation     │
│  - Creates + modifies    │    │    context               │
│    files                 │    │  - Reports pass/fail     │
│                          │    │  - Provides failure      │
│                          │    │    details               │
└──────────────────────────┘    └──────────────────────────┘
```

**Why this split?**
- **Implementer** needs full context (specs, existing code, design decisions)
- **Verifier** should NOT have that context — it's a blackbox tester
- This prevents the "I know I wrote it correctly so I'll assume it works" bias

---

## Part 0: Choose Your MVP Product

Pick something simple with clear user flows. Suggestions:

| Product | Pros | Cons |
|---------|------|------|
| **Expense Tracker** | CRUD + validation + calculations | Slightly more complex |
| **Todo App** | Simple, well-understood | Boring, less to test |
| **URL Shortener** | Simple API, redirect logic | Less UI to test |
| **Note-taking App** | CRUD + search + tags | Good middle ground |

**Recommended: Expense Tracker**
- Add/edit/delete expenses
- Categories, amounts, dates
- Monthly summary report
- Clear validation rules (amount > 0, date required, etc.)

---

## Part 1: Setup the Project

### 1.1 Create Project Structure

```
expense-tracker/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app
│   ├── models.py        # Pydantic models
│   ├── database.py      # SQLite for simplicity
│   └── routes/
│       └── expenses.py
├── tests/
│   └── e2e/
│       ├── conftest.py  # Pytest fixtures
│       └── test_expenses.py
├── .kiro/
│   ├── specs/
│   │   └── expense-tracker/
│   │       ├── requirements.md
│   │       ├── design.md
│   │       └── tasks.md
│   └── agents/
│       ├── implementer.md
│       └── verifier.md
├── pyproject.toml
└── README.md
```

### 1.2 Minimal MVP (You Build This First)

Before agents can iterate, you need a working skeleton:

```python
# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Expense Tracker")

@app.get("/health")
def health():
    return {"status": "ok"}

# TODO: Agent will implement the rest
```

```python
# tests/e2e/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)
```

```python
# tests/e2e/test_expenses.py
"""
E2E tests for expense tracker.
These tests verify user-visible behavior, not implementation details.
"""

def test_health_check(client):
    """App should respond to health check."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

# TODO: You write more E2E tests here (Part 2)
```

### 1.3 Run the Skeleton

```bash
cd expense-tracker
uv init
uv add fastapi uvicorn pytest httpx
uv run pytest tests/e2e/ -v
```

Verify: Health check test should pass.

---

## Part 2: Write E2E Tests (Human Task)

**You write these tests. The agent will make them pass.**

This is critical: E2E tests define the contract. Write tests for user-visible behavior:

```python
# tests/e2e/test_expenses.py

class TestCreateExpense:
    """Tests for creating expenses."""
    
    def test_create_expense_success(self, client):
        """User can create an expense with valid data."""
        response = client.post("/expenses", json={
            "amount": 50.00,
            "category": "food",
            "description": "Lunch",
            "date": "2024-01-15"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["amount"] == 50.00
        assert data["category"] == "food"
        assert "id" in data
    
    def test_create_expense_negative_amount_fails(self, client):
        """Negative amounts should be rejected."""
        response = client.post("/expenses", json={
            "amount": -10.00,
            "category": "food",
            "description": "Invalid",
            "date": "2024-01-15"
        })
        assert response.status_code == 422  # Validation error
    
    def test_create_expense_missing_category_fails(self, client):
        """Category is required."""
        response = client.post("/expenses", json={
            "amount": 50.00,
            "description": "No category",
            "date": "2024-01-15"
        })
        assert response.status_code == 422


class TestListExpenses:
    """Tests for listing expenses."""
    
    def test_list_expenses_empty(self, client):
        """Empty database returns empty list."""
        response = client.get("/expenses")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_list_expenses_returns_created(self, client):
        """Created expenses appear in list."""
        # Create an expense
        client.post("/expenses", json={
            "amount": 25.00,
            "category": "transport",
            "description": "Bus fare",
            "date": "2024-01-15"
        })
        
        # List should include it
        response = client.get("/expenses")
        assert response.status_code == 200
        expenses = response.json()
        assert len(expenses) >= 1
        assert any(e["description"] == "Bus fare" for e in expenses)


class TestMonthlySummary:
    """Tests for monthly summary report."""
    
    def test_monthly_summary_calculates_total(self, client):
        """Summary should show total for the month."""
        # Create expenses for January 2024
        client.post("/expenses", json={
            "amount": 100.00, "category": "food",
            "description": "Groceries", "date": "2024-01-10"
        })
        client.post("/expenses", json={
            "amount": 50.00, "category": "transport",
            "description": "Uber", "date": "2024-01-15"
        })
        
        # Get January summary
        response = client.get("/expenses/summary/2024/01")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 150.00
        assert data["month"] == "2024-01"
```

### Guidelines for E2E Tests

1. **Test user behavior, not implementation**
   - ✅ "User can create expense" 
   - ❌ "Database insert works"

2. **Be specific about expected responses**
   - Status codes, response shapes, error messages

3. **Cover happy path AND edge cases**
   - Valid input, invalid input, boundary conditions

4. **Each test should be independent**
   - Use fixtures to reset state between tests

---

## Part 3: Create the Specs

Use Kiro's spec workflow to create requirements:

```markdown
<!-- .kiro/specs/expense-tracker/requirements.md -->

# Expense Tracker Requirements

## Overview
A simple expense tracking application with CRUD operations and monthly summaries.

## Functional Requirements

### REQ-1: Create Expense
- User can create an expense with: amount, category, description, date
- Amount must be positive (> 0)
- Category is required (one of: food, transport, entertainment, utilities, other)
- Date is required, format: YYYY-MM-DD
- Returns created expense with generated ID

### REQ-2: List Expenses
- User can list all expenses
- Returns array of expenses, empty array if none
- Ordered by date descending (newest first)

### REQ-3: Monthly Summary
- User can get summary for a specific month
- Returns: total amount, breakdown by category, expense count
- Format: GET /expenses/summary/{year}/{month}

### REQ-4: Delete Expense
- User can delete an expense by ID
- Returns 204 on success, 404 if not found

## Non-Functional Requirements

### NFR-1: Validation
- All validation errors return 422 with descriptive messages

### NFR-2: Data Persistence
- Use SQLite for simplicity (file-based, no setup)
```

---

## Part 4: Create the Agents

### 4.1 Implementer Agent

```markdown
<!-- .kiro/agents/implementer.md -->

---
description: Implements features based on specs and makes E2E tests pass
tools:
  - filesystem
  - shell
autoApprove:
  - read_file
  - write_file
  - list_directory
---

# Implementer Agent

You implement features for the expense tracker application.

## Your Role
- Read specs from `.kiro/specs/expense-tracker/`
- Write code to implement requirements
- You have FULL CONTEXT of the codebase

## Rules
1. Follow the existing code patterns
2. Use FastAPI best practices
3. Implement ONE requirement at a time
4. After implementing, report what you did

## Output Format
After implementing, output:
```
IMPLEMENTED: [requirement ID]
FILES CHANGED: [list of files]
READY FOR VERIFICATION
```
```

### 4.2 Verifier Agent

```markdown
<!-- .kiro/agents/verifier.md -->

---
description: Runs E2E tests and reports results - NO implementation context
tools:
  - shell
autoApprove:
  - execute_command
---

# Verifier Agent

You are a blackbox tester. You run E2E tests and report results.

## Your Role
- Run the E2E test suite
- Report pass/fail status
- Provide failure details if tests fail

## Rules
1. You have NO knowledge of the implementation
2. You ONLY run tests and report results
3. You MUST run the COMPLETE test suite (avoid "early victory")
4. Do NOT look at implementation code

## Process
1. Run: `uv run pytest tests/e2e/ -v --tb=short`
2. Report results in this format:

```
VERIFICATION RESULT: [PASS/FAIL]
TESTS RUN: [number]
PASSED: [number]
FAILED: [number]

[If failed, list each failure:]
FAILURE 1: test_name
  Expected: ...
  Got: ...
```

## Critical
- Do NOT assume tests pass
- Do NOT skip tests
- Report the ACTUAL output from pytest
```

### 4.3 Orchestrator Agent

```markdown
<!-- .kiro/agents/e2e-orchestrator.md -->

---
description: Orchestrates the implement-verify loop
tools:
  - filesystem
  - shell
autoApprove:
  - read_file
  - list_directory
---

# E2E Orchestrator Agent

You coordinate the implementation and verification cycle.

## Workflow

1. **Read specs** from `.kiro/specs/expense-tracker/requirements.md`
2. **Read current test results** to see what's failing
3. **Dispatch to implementer** with specific requirement to implement
4. **Dispatch to verifier** to run E2E tests
5. **If tests fail**: Loop back to step 3 with failure context
6. **If tests pass**: Move to next requirement

## Dispatching

To dispatch to another agent, output:

```
DISPATCH TO: [implementer/verifier]
CONTEXT: [what they need to know]
```

## Loop Control

- Maximum 3 attempts per requirement
- If still failing after 3 attempts, report to human:
  ```
  STUCK ON: [requirement]
  ATTEMPTS: 3
  LAST ERROR: [error details]
  NEED HUMAN HELP
  ```

## Progress Tracking

Keep track of:
- ✅ Completed requirements
- 🔄 In progress
- ❌ Blocked
```

---

## Part 5: Run the Multi-Agent Loop

### 5.1 Manual Orchestration (Start Here)

Before automating, run the loop manually to understand it:

1. **Check current state:**
   ```bash
   uv run pytest tests/e2e/ -v
   ```
   Note which tests are failing.

2. **Invoke implementer:**
   ```
   /implementer
   
   Implement REQ-1: Create Expense. 
   The test `test_create_expense_success` should pass.
   ```

3. **Invoke verifier:**
   ```
   /verifier
   
   Run all E2E tests and report results.
   ```

4. **If tests fail**, give failure context to implementer:
   ```
   /implementer
   
   The verifier reported this failure:
   [paste failure details]
   
   Fix the implementation.
   ```

5. **Repeat** until tests pass, then move to next requirement.

### 5.2 Semi-Automated with Hooks (Advanced)

Create a hook that triggers verification after file edits:

```json
// .kiro/hooks/verify-on-change.json
{
  "name": "Verify on Change",
  "version": "1.0.0",
  "when": {
    "type": "fileEdited",
    "patterns": ["app/**/*.py"]
  },
  "then": {
    "type": "runCommand",
    "command": "uv run pytest tests/e2e/ -v --tb=short"
  }
}
```

This runs E2E tests whenever app code changes — not fully automated multi-agent, but gives fast feedback.

---

## Part 6: Reflection Questions

After completing the exercise, answer these:

### On the Pattern

1. **Why did we give the verifier NO implementation context?**
   - What bugs might it catch that an implementer-with-tests would miss?

2. **What would happen if we used ONE agent for both implementing and testing?**
   - How does context pollution affect verification quality?

3. **When would you add MORE agents to this system?**
   - At what point does the complexity become worth it?

### On E2E vs Unit Tests

4. **What did the E2E tests catch that unit tests might miss?**
   - Think about integration issues, API contracts, validation.

5. **What are the downsides of E2E-only testing?**
   - Speed? Debugging? Coverage granularity?

### On the Loop

6. **How many iterations did it take for each requirement?**
   - What caused extra iterations?

7. **Where did you (human) need to intervene?**
   - What decisions couldn't be automated?

---

## Bonus Challenges

### Challenge A: Add Browser Testing

Replace API tests with actual browser tests using Playwright:

```python
# tests/e2e/test_ui.py
from playwright.sync_api import sync_playwright

def test_create_expense_via_ui():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:8000")
        
        # Fill form
        page.fill("#amount", "50.00")
        page.select_option("#category", "food")
        page.fill("#description", "Lunch")
        page.click("#submit")
        
        # Verify
        assert page.locator(".expense-item").count() == 1
        browser.close()
```

This requires:
- Adding a simple HTML frontend
- Running the server during tests
- More realistic user simulation

### Challenge B: Parallel Subagents

Modify the orchestrator to dispatch MULTIPLE implementers in parallel for independent requirements (e.g., REQ-1 and REQ-4 don't depend on each other).

### Challenge C: Add a Reporter Agent

Add a third agent that generates a progress report:
- What's implemented
- What's tested
- What's pending
- Estimated time to completion

---

## Success Criteria

You've completed this exercise when:

- [ ] MVP skeleton is running
- [ ] You wrote 5+ E2E tests (human task)
- [ ] Implementer agent made at least 2 tests pass
- [ ] Verifier agent caught at least 1 failure
- [ ] You ran the implement → verify loop at least 3 times
- [ ] You can explain why the verifier has no implementation context
- [ ] You documented learnings in `learnings.md`

---

## Key Takeaways

1. **Verification subagent = blackbox tester** — no implementation context
2. **E2E tests define the contract** — human writes these, agent makes them pass
3. **Iteration loop is the core pattern** — implement → test → fix → repeat
4. **Context isolation prevents bias** — verifier can't assume "I know it works"
5. **Human stays in the loop** — writes specs, writes tests, approves decisions
