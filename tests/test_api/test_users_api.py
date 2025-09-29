from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.user import create_random_user, user_authentication_headers


def test_create_user_api(client: TestClient):
    """
    Integration test for the POST /users endpoint.
    """
    # First user should be an admin
    response = client.post("/users", json={"name": "api_user1", "password": "pass"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "api_user1"
    assert data["permission_level"] == 2 # ADMIN

    # Second user should be pending validation
    response = client.post("/users", json={"name": "api_user2", "password": "pass"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "api_user2"
    assert data["permission_level"] == 0 # PENDING_VALIDATION



def test_get_users_superuser(client: TestClient, db_session: Session) -> None:
    create_random_user(db_session)
    create_random_user(db_session)
    admin_headers = user_authentication_headers(client=client, db=db_session, is_admin=True)
    r = client.get(f"/users", headers=admin_headers)
    all_users = r.json()
    assert len(all_users) > 1



def test_update_user(client: TestClient, db_session: Session) -> None:
    user = create_random_user(db_session)
    admin_headers = user_authentication_headers(client=client, db=db_session, is_admin=True)
    data = {"permission_level": 1}
    r = client.patch(
        f"/users/{user.id}",
        headers=admin_headers,
        json=data,
    )
    assert r.status_code == 200
    updated_user = r.json()
    assert updated_user["permission_level"] == data["permission_level"]



def test_delete_user(client: TestClient, db_session: Session) -> None:
    user = create_random_user(db_session)
    admin_headers = user_authentication_headers(client=client, db=db_session, is_admin=True)
    r = client.delete(f"/users/{user.id}", headers=admin_headers)
    assert r.status_code == 200
    deleted_user = r.json()
    assert deleted_user["is_active"] is False



def test_approve_user(client: TestClient, db_session: Session) -> None:
    user = create_random_user(db_session)
    admin_headers = user_authentication_headers(client=client, db=db_session, is_admin=True)
    r = client.patch(
        f"/users/{user.id}/approve",
        headers=admin_headers,
    )
    assert r.status_code == 200
    approved_user = r.json()
    assert approved_user["permission_level"] == 1