"""
E2E tests for Expense Tracker API.

These tests define the contract. The agent will make them pass.
Tests verify user-visible behavior, not implementation details.
"""


# =============================================================================
# REQ-1: Create Expense
# =============================================================================

class TestCreateExpense:
    """Tests for POST /expenses"""

    def test_create_expense_success(self, client):
        """User can create an expense with valid data."""
        response = client.post("/expenses", json={
            "amount": 50.00,
            "category": "food",
            "description": "Lunch with team",
            "date": "2024-01-15"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["amount"] == 50.00
        assert data["category"] == "food"
        assert data["description"] == "Lunch with team"
        assert data["date"] == "2024-01-15"
        assert "id" in data
        assert isinstance(data["id"], int)

    def test_create_expense_minimal(self, client):
        """Can create expense without optional description."""
        response = client.post("/expenses", json={
            "amount": 25.00,
            "category": "transport",
            "date": "2024-01-15"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["amount"] == 25.00
        assert data["category"] == "transport"

    def test_create_expense_negative_amount_fails(self, client):
        """Negative amounts should be rejected."""
        response = client.post("/expenses", json={
            "amount": -10.00,
            "category": "food",
            "description": "Invalid",
            "date": "2024-01-15"
        })
        assert response.status_code == 422

    def test_create_expense_zero_amount_fails(self, client):
        """Zero amount should be rejected."""
        response = client.post("/expenses", json={
            "amount": 0,
            "category": "food",
            "date": "2024-01-15"
        })
        assert response.status_code == 422

    def test_create_expense_missing_category_fails(self, client):
        """Category is required."""
        response = client.post("/expenses", json={
            "amount": 50.00,
            "description": "No category",
            "date": "2024-01-15"
        })
        assert response.status_code == 422

    def test_create_expense_invalid_category_fails(self, client):
        """Category must be from allowed list."""
        response = client.post("/expenses", json={
            "amount": 50.00,
            "category": "invalid_category",
            "date": "2024-01-15"
        })
        assert response.status_code == 422

    def test_create_expense_missing_date_fails(self, client):
        """Date is required."""
        response = client.post("/expenses", json={
            "amount": 50.00,
            "category": "food"
        })
        assert response.status_code == 422

    def test_create_expense_invalid_date_format_fails(self, client):
        """Date must be in YYYY-MM-DD format."""
        response = client.post("/expenses", json={
            "amount": 50.00,
            "category": "food",
            "date": "15-01-2024"  # Wrong format
        })
        assert response.status_code == 422


# =============================================================================
# REQ-2: List Expenses
# =============================================================================

class TestListExpenses:
    """Tests for GET /expenses"""

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

    def test_list_expenses_multiple(self, client):
        """Multiple expenses are returned."""
        # Create two expenses
        client.post("/expenses", json={
            "amount": 10.00, "category": "food",
            "description": "Coffee", "date": "2024-01-15"
        })
        client.post("/expenses", json={
            "amount": 20.00, "category": "transport",
            "description": "Taxi", "date": "2024-01-15"
        })

        response = client.get("/expenses")
        assert response.status_code == 200
        expenses = response.json()
        assert len(expenses) >= 2


# =============================================================================
# REQ-3: Get Single Expense
# =============================================================================

class TestGetExpense:
    """Tests for GET /expenses/{id}"""

    def test_get_expense_success(self, client):
        """Can retrieve a specific expense by ID."""
        # Create an expense
        create_response = client.post("/expenses", json={
            "amount": 75.00,
            "category": "entertainment",
            "description": "Movie tickets",
            "date": "2024-01-20"
        })
        expense_id = create_response.json()["id"]

        # Get it back
        response = client.get(f"/expenses/{expense_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == expense_id
        assert data["amount"] == 75.00
        assert data["description"] == "Movie tickets"

    def test_get_expense_not_found(self, client):
        """Non-existent ID returns 404."""
        response = client.get("/expenses/99999")
        assert response.status_code == 404


# =============================================================================
# REQ-4: Update Expense
# =============================================================================

class TestUpdateExpense:
    """Tests for PUT /expenses/{id}"""

    def test_update_expense_success(self, client):
        """Can update an existing expense."""
        # Create an expense
        create_response = client.post("/expenses", json={
            "amount": 50.00,
            "category": "food",
            "description": "Lunch",
            "date": "2024-01-15"
        })
        expense_id = create_response.json()["id"]

        # Update it
        response = client.put(f"/expenses/{expense_id}", json={
            "amount": 60.00,
            "category": "food",
            "description": "Fancy lunch",
            "date": "2024-01-15"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["amount"] == 60.00
        assert data["description"] == "Fancy lunch"

    def test_update_expense_not_found(self, client):
        """Updating non-existent ID returns 404."""
        response = client.put("/expenses/99999", json={
            "amount": 50.00,
            "category": "food",
            "date": "2024-01-15"
        })
        assert response.status_code == 404

    def test_update_expense_invalid_data_fails(self, client):
        """Update with invalid data returns 422."""
        # Create an expense
        create_response = client.post("/expenses", json={
            "amount": 50.00,
            "category": "food",
            "date": "2024-01-15"
        })
        expense_id = create_response.json()["id"]

        # Try to update with negative amount
        response = client.put(f"/expenses/{expense_id}", json={
            "amount": -10.00,
            "category": "food",
            "date": "2024-01-15"
        })
        assert response.status_code == 422


# =============================================================================
# REQ-5: Delete Expense
# =============================================================================

class TestDeleteExpense:
    """Tests for DELETE /expenses/{id}"""

    def test_delete_expense_success(self, client):
        """Can delete an expense."""
        # Create an expense
        create_response = client.post("/expenses", json={
            "amount": 30.00,
            "category": "utilities",
            "description": "Phone bill",
            "date": "2024-01-15"
        })
        expense_id = create_response.json()["id"]

        # Delete it
        response = client.delete(f"/expenses/{expense_id}")
        assert response.status_code == 204

        # Verify it's gone
        get_response = client.get(f"/expenses/{expense_id}")
        assert get_response.status_code == 404

    def test_delete_expense_not_found(self, client):
        """Deleting non-existent ID returns 404."""
        response = client.delete("/expenses/99999")
        assert response.status_code == 404


# =============================================================================
# REQ-6: Monthly Summary
# =============================================================================

class TestMonthlySummary:
    """Tests for GET /expenses/summary/{year}/{month}"""

    def test_monthly_summary_calculates_total(self, client):
        """Summary calculates correct total for the month."""
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
        assert data["month"] == "2024-01"
        assert data["total"] == 150.00
        assert data["count"] == 2

    def test_monthly_summary_by_category(self, client):
        """Summary includes breakdown by category."""
        # Create expenses
        client.post("/expenses", json={
            "amount": 80.00, "category": "food",
            "description": "Dinner", "date": "2024-02-10"
        })
        client.post("/expenses", json={
            "amount": 20.00, "category": "food",
            "description": "Snacks", "date": "2024-02-15"
        })
        client.post("/expenses", json={
            "amount": 40.00, "category": "transport",
            "description": "Gas", "date": "2024-02-20"
        })

        response = client.get("/expenses/summary/2024/02")
        assert response.status_code == 200
        data = response.json()
        assert data["by_category"]["food"] == 100.00
        assert data["by_category"]["transport"] == 40.00

    def test_monthly_summary_empty_month(self, client):
        """Summary for month with no expenses returns zeros."""
        response = client.get("/expenses/summary/2099/12")
        assert response.status_code == 200
        data = response.json()
        assert data["month"] == "2099-12"
        assert data["total"] == 0
        assert data["count"] == 0
        assert data["by_category"] == {}

    def test_monthly_summary_average(self, client):
        """Summary includes average expense amount."""
        # Create 4 expenses totaling 200
        for i in range(4):
            client.post("/expenses", json={
                "amount": 50.00, "category": "other",
                "description": f"Expense {i}", "date": "2024-03-15"
            })

        response = client.get("/expenses/summary/2024/03")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 200.00
        assert data["count"] == 4
        assert data["average"] == 50.00
