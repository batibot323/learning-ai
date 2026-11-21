# Expense Tracker Specs

A simple expense tracking API for the multi-agent E2E verification exercise.

---

## Overview

Track personal expenses with categories, amounts, and dates. Generate monthly summaries.

**Tech Stack:**
- FastAPI (Python)
- SQLite (file-based, no setup)
- Pydantic (validation)

---

## Data Model

### Expense

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| id | int | auto | Primary key |
| amount | float | ✅ | > 0 |
| category | string | ✅ | One of: food, transport, entertainment, utilities, other |
| description | string | ❌ | Max 200 chars |
| date | string | ✅ | Format: YYYY-MM-DD |
| created_at | datetime | auto | UTC timestamp |

---

## API Endpoints

### REQ-1: Create Expense

```
POST /expenses
```

**Request Body:**
```json
{
  "amount": 50.00,
  "category": "food",
  "description": "Lunch with team",
  "date": "2024-01-15"
}
```

**Success Response (201):**
```json
{
  "id": 1,
  "amount": 50.00,
  "category": "food",
  "description": "Lunch with team",
  "date": "2024-01-15",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Validation Errors (422):**
- amount <= 0
- category not in allowed list
- date missing or invalid format
- description > 200 chars

---

### REQ-2: List Expenses

```
GET /expenses
```

**Query Parameters:**
- `category` (optional) — filter by category
- `month` (optional) — filter by month (YYYY-MM format)

**Success Response (200):**
```json
[
  {
    "id": 1,
    "amount": 50.00,
    "category": "food",
    "description": "Lunch",
    "date": "2024-01-15",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

Returns empty array `[]` if no expenses.

---

### REQ-3: Get Single Expense

```
GET /expenses/{id}
```

**Success Response (200):**
```json
{
  "id": 1,
  "amount": 50.00,
  "category": "food",
  "description": "Lunch",
  "date": "2024-01-15",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Not Found (404):**
```json
{
  "detail": "Expense not found"
}
```

---

### REQ-4: Update Expense

```
PUT /expenses/{id}
```

**Request Body:** Same as create (all fields required)

**Success Response (200):** Updated expense object

**Not Found (404):** If ID doesn't exist

---

### REQ-5: Delete Expense

```
DELETE /expenses/{id}
```

**Success Response (204):** No content

**Not Found (404):** If ID doesn't exist

---

### REQ-6: Monthly Summary

```
GET /expenses/summary/{year}/{month}
```

Example: `GET /expenses/summary/2024/01`

**Success Response (200):**
```json
{
  "month": "2024-01",
  "total": 350.00,
  "count": 5,
  "by_category": {
    "food": 150.00,
    "transport": 100.00,
    "entertainment": 100.00
  },
  "average": 70.00
}
```

**Empty Month (200):**
```json
{
  "month": "2024-01",
  "total": 0,
  "count": 0,
  "by_category": {},
  "average": 0
}
```

---

## Validation Rules

| Rule | Error Code | Message |
|------|------------|---------|
| amount <= 0 | 422 | "Amount must be greater than 0" |
| invalid category | 422 | "Category must be one of: food, transport, entertainment, utilities, other" |
| missing date | 422 | "Date is required" |
| invalid date format | 422 | "Date must be in YYYY-MM-DD format" |
| description too long | 422 | "Description must be 200 characters or less" |

---

## Non-Functional Requirements

### NFR-1: Health Check

```
GET /health
```

Response: `{"status": "ok"}`

### NFR-2: Data Persistence

- SQLite database file: `expenses.db`
- Data survives server restarts
- Tests use separate test database (reset between tests)

### NFR-3: Error Responses

All errors return JSON with `detail` field:
```json
{
  "detail": "Error message here"
}
```

---

## E2E Test Scenarios

These are the scenarios the human will write tests for:

### Happy Path
1. ✅ Create expense with valid data
2. ✅ List expenses returns created items
3. ✅ Get single expense by ID
4. ✅ Update expense changes values
5. ✅ Delete expense removes it
6. ✅ Monthly summary calculates correctly

### Edge Cases
7. ✅ List expenses when empty returns []
8. ✅ Get non-existent expense returns 404
9. ✅ Delete non-existent expense returns 404
10. ✅ Summary for month with no expenses returns zeros

### Validation
11. ✅ Negative amount rejected
12. ✅ Zero amount rejected
13. ✅ Invalid category rejected
14. ✅ Missing date rejected
15. ✅ Invalid date format rejected
16. ✅ Description over 200 chars rejected

---

## Implementation Priority

For the multi-agent exercise, implement in this order:

1. **Phase 1:** Health check + Create expense
2. **Phase 2:** List expenses + Get single
3. **Phase 3:** Delete expense
4. **Phase 4:** Update expense
5. **Phase 5:** Monthly summary

Each phase = one implement → verify cycle.
