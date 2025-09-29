from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate
from app.services import user_service


import uuid

def user_authentication_headers(client: TestClient, db: Session, is_admin: bool = False) -> dict[str, str]:
    username = str(uuid.uuid4())
    user_in = UserCreate(name=username, password="pass")
    user = user_service.create_user(db, user_in)
    if is_admin:
        user.permission_level = 2
        db.commit()

    response = client.post(
        f"/login/access-token",
        data={"username": user_in.name, "password": user_in.password},
    )
    tokens = response.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


def create_random_user(db: Session) -> User:
    username = str(uuid.uuid4())
    user_in = UserCreate(name=username, password="pass")
    user = user_service.create_user(db, user_in)
    return user