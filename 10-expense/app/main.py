"""
Expense Tracker API
"""
import os
import sqlite3
import re
from datetime import datetime, timezone
from typing import Optional
from contextlib import contextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

# ---------------------------------------------------------------------------
# Database setup
# ---------------------------------------------------------------------------

def get_db_path() -> str:
    return os.environ.get("DATABASE_URL", "expenses.db")


def get_connection():
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            description TEXT,
            date        TEXT    NOT NULL,
            created_at  TEXT    NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

ALLOWED_CATEGORIES = {"food", "transport", "entertainment", "utilities", "other"}
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class ExpenseCreate(BaseModel):
    amount: float = Field(..., gt=0, description="Must be > 0")
    category: str
    description: Optional[str] = Field(None, max_length=200)
    date: str

    @field_validator("category")
    @classmethod
    def validate_category(cls, v):
        if v not in ALLOWED_CATEGORIES:
            raise ValueError(f"Category must be one of: {', '.join(sorted(ALLOWED_CATEGORIES))}")
        return v

    @field_validator("date")
    @classmethod
    def validate_date(cls, v):
        if not DATE_PATTERN.match(v):
            raise ValueError("Date must be in YYYY-MM-DD format")
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
        return v


class ExpenseResponse(BaseModel):
    id: int
    amount: float
    category: str
    description: Optional[str]
    date: str
    created_at: str


class SummaryResponse(BaseModel):
    month: str
    total: float
    count: int
    by_category: dict
    average: float


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(title="Expense Tracker", version="0.1.0")


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# REQ-6: Monthly summary - MUST come before /{id} to avoid route conflict
# ---------------------------------------------------------------------------

@app.get("/expenses/summary/{year}/{month}", response_model=SummaryResponse)
def monthly_summary(year: int, month: int):
    month_str = f"{year}-{month:02d}"
    conn = get_connection()
    init_db()
    rows = conn.execute(
        "SELECT amount, category FROM expenses WHERE date LIKE ?",
        (f"{month_str}-%",)
    ).fetchall()
    conn.close()

    total = sum(r["amount"] for r in rows)
    count = len(rows)
    by_category: dict = {}
    for r in rows:
        by_category[r["category"]] = by_category.get(r["category"], 0.0) + r["amount"]
    average = total / count if count else 0.0

    return SummaryResponse(
        month=month_str,
        total=total,
        count=count,
        by_category=by_category,
        average=average,
    )


# ---------------------------------------------------------------------------
# REQ-1: Create Expense
# ---------------------------------------------------------------------------

@app.post("/expenses", response_model=ExpenseResponse, status_code=201)
def create_expense(expense: ExpenseCreate):
    init_db()
    created_at = datetime.now(timezone.utc).isoformat()
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO expenses (amount, category, description, date, created_at) VALUES (?, ?, ?, ?, ?)",
        (expense.amount, expense.category, expense.description, expense.date, created_at)
    )
    conn.commit()
    expense_id = cursor.lastrowid
    row = conn.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
    conn.close()
    return dict(row)


# ---------------------------------------------------------------------------
# REQ-2: List Expenses
# ---------------------------------------------------------------------------

@app.get("/expenses", response_model=list[ExpenseResponse])
def list_expenses():
    init_db()
    conn = get_connection()
    rows = conn.execute("SELECT * FROM expenses ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# REQ-3: Get Single Expense
# ---------------------------------------------------------------------------

@app.get("/expenses/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: int):
    init_db()
    conn = get_connection()
    row = conn.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return dict(row)


# ---------------------------------------------------------------------------
# REQ-4: Update Expense
# ---------------------------------------------------------------------------

@app.put("/expenses/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, expense: ExpenseCreate):
    init_db()
    conn = get_connection()
    row = conn.execute("SELECT id FROM expenses WHERE id = ?", (expense_id,)).fetchone()
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Expense not found")
    conn.execute(
        "UPDATE expenses SET amount=?, category=?, description=?, date=? WHERE id=?",
        (expense.amount, expense.category, expense.description, expense.date, expense_id)
    )
    conn.commit()
    updated = conn.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
    conn.close()
    return dict(updated)


# ---------------------------------------------------------------------------
# REQ-5: Delete Expense
# ---------------------------------------------------------------------------

@app.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int):
    init_db()
    conn = get_connection()
    row = conn.execute("SELECT id FROM expenses WHERE id = ?", (expense_id,)).fetchone()
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Expense not found")
    conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
