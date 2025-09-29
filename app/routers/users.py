import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.user import User, UserCreate, UserUpdate
from app.services import user_service

from app.auth import require_admin

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user with pending validation.
    """
    db_user = user_service.get_user_by_name(db, name=user.name)
    if db_user:
        logger.warning(f"User creation failed: name '{user.name}' already registered.")
        raise HTTPException(status_code=400, detail="Username already registered")
    return user_service.create_user(db=db, user_create=user)


@router.get("/users", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all active users.
    """
    users = user_service.get_all_users(db, skip=skip, limit=limit)
    return users

@router.patch("/users/{user_id}", response_model=User, dependencies=[Depends(require_admin)])
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """
    Update a user's permission level or active status. (Admin only)
    """
    db_user = user_service.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_service.update_user(db=db, user=db_user, user_update=user_update)

@router.delete("/users/{user_id}", response_model=User, dependencies=[Depends(require_admin)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Soft delete a user. (Admin only)
    """
    db_user = user_service.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_service.delete_user(db=db, user=db_user)

@router.patch("/users/{user_id}/approve", response_model=User, dependencies=[Depends(require_admin)])
def approve_user(user_id: int, db: Session = Depends(get_db)):
    """
    Approve a user. (Admin only)
    """
    db_user = user_service.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_update = UserUpdate(permission_level=1)
    return user_service.update_user(db=db, user=db_user, user_update=user_update)
