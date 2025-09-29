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