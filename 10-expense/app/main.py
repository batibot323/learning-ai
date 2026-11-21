"""
Expense Tracker API

Minimal skeleton - agent will implement the rest.
"""
from fastapi import FastAPI

app = FastAPI(title="Expense Tracker", version="0.1.0")


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}


# TODO: Agent will implement:
# - POST /expenses
# - GET /expenses
# - GET /expenses/{id}
# - PUT /expenses/{id}
# - DELETE /expenses/{id}
# - GET /expenses/summary/{year}/{month}
