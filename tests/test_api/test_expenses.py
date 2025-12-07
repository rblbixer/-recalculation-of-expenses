import pytest


@pytest.mark.asyncio
async def test_create_and_list_expense(client):
    payload = {
        "user_id": 123,
        "amount": 150.5,
        "category": "taxi",
        "description": "до дома",
    }
    response = await client.post("/api/expenses/", json=payload)
    assert response.status_code == 200
    created = response.json()
    assert created["amount"] == payload["amount"]
    assert created["category"] == payload["category"]
    assert created["user_id"] == payload["user_id"]

    list_today = await client.get(f"/api/expenses/today?user_id={payload['user_id']}")
    assert list_today.status_code == 200
    data = list_today.json()
    assert len(data) >= 1
    assert any(item["id"] == created["id"] for item in data)

