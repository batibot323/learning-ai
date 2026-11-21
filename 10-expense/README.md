# Expense Tracker

Multi-agent E2E verification exercise project.

## Setup

```bash
cd 10-expense
uv sync
uv pip install -e ".[dev]"
```

## Run Tests

```bash
uv run pytest tests/e2e/ -v
```

## Run Server

```bash
uv run uvicorn app.main:app --reload
```

## Exercise Flow

1. Human writes E2E tests (defines contract)
2. Implementer agent makes tests pass
3. Verifier agent runs tests (blackbox)
4. Iterate until all tests pass

See `specs.md` for API specification.
