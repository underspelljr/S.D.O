import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.user import User, UserCreate
from app.services import user_service

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    db_user = user_service.get_user_by_name(db, name=user.name)
    if db_user:
        logger.warning(f"User creation failed: name '{user.name}' already registered.")
        raise HTTPException(status_code=400, detail="Username already registered")
    return user_service.create_user(db=db, user_create=user)


@router.get("/users", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all users.
    """
    users = user_service.get_all_users(db, skip=skip, limit=limit)
    return users