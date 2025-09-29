from fastapi.testclient import TestClient

def test_create_spot_api(client: TestClient):
    """
    Integration test for creating a spot.
    """
    # First, create a user
    user_res = client.post("/users", json={"name": "spot_creator", "password": "pass"})
    assert user_res.status_code == 201
    user_id = user_res.json()["id"]

    # Then, create a spot
    spot_data = {
        "name": "Praia de Carcavelos",
        "description": "Popular surf spot.",
        "latitude": 38.679,
        "longitude": -9.336,
        "user_id": user_id
    }
    response = client.post("/spots", json=spot_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Praia de Carcavelos"
    assert data["created_by"]["id"] == user_id
    assert data["created_by"]["name"] == "spot_creator"

def test_read_all_spots_api(client: TestClient):
    """
    Integration test for retrieving all spots.
    """
    response = client.get("/spots")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_one_spot_api(client: TestClient):
    """
    Integration test for retrieving a single spot by ID.
    """
    # Create user and spot first
    user_id = client.post("/users", json={"name": "spot_reader", "password": "pass"}).json()["id"]
    spot_data = {
        "name": "Boca do Inferno", "latitude": 38.69, "longitude": -9.49, "user_id": user_id
    }
    created_spot_id = client.post("/spots", json=spot_data).json()["id"]

    # Retrieve it
    response = client.get(f"/spots/{created_spot_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_spot_id
    assert data["name"] == "Boca do Inferno"

def test_read_nonexistent_spot_api(client: TestClient):
    """
    Test retrieving a spot that doesn't exist.
    """
    response = client.get("/spots/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Spot not found"