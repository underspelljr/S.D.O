from fastapi.testclient import TestClient

def test_create_user_api(client: TestClient):
    """
    Integration test for the POST /users endpoint.
    """
    response = client.post("/users", json={"name": "api_user"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "api_user"
    assert "id" in data
    assert "uuid" in data
    assert data["permission_level"] == 0
    assert data["is_active"] == True

def test_create_existing_user_api(client: TestClient):
    """
    Test creating a user that already exists.
    """
    client.post("/users", json={"name": "duplicate_user"}) # First time should succeed
    response = client.post("/users", json={"name": "duplicate_user"}) # Second time should fail
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"

def test_read_users_api(client: TestClient):
    """
    Integration test for the GET /users endpoint.
    """
    client.post("/users", json={"name": "user_a"})
    client.post("/users", json={"name": "user_b"})

    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2 # Use >= in case other tests added users
    names = [user['name'] for user in data]
    assert "user_a" in names
    assert "user_b" in names

def test_update_user_api(client: TestClient):
    """
    Integration test for the PATCH /users/{user_id} endpoint.
    """
    response = client.post("/users", json={"name": "user_to_update"})
    user_id = response.json()["id"]

    response = client.patch(f"/users/{user_id}", json={"permission_level": 2})
    assert response.status_code == 200
    data = response.json()
    assert data["permission_level"] == 2

def test_delete_user_api(client: TestClient):
    """
    Integration test for the DELETE /users/{user_id} endpoint.
    """
    response = client.post("/users", json={"name": "user_to_delete"})
    user_id = response.json()["id"]

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["is_active"] == False

    # Check that the user is not returned by the GET /users endpoint
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    for user in data:
        assert user["name"] != "user_to_delete"

def test_approve_user_api(client: TestClient):
    """
    Integration test for the PATCH /users/{user_id}/approve endpoint.
    """
    response = client.post("/users", json={"name": "user_to_approve"})
    user_id = response.json()["id"]

    response = client.patch(f"/users/{user_id}/approve")
    assert response.status_code == 200
    data = response.json()
    assert data["permission_level"] == 1
