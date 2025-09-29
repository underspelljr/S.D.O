import logging
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

logger = logging.getLogger(__name__)

def create_user(db: Session, user_create: UserCreate) -> User:
    """Creates a new user in the database with pending validation."""
    logger.info(f"Creating user with name: {user_create.name}")
    db_user = User(name=user_create.name, permission_level=0) # PENDING_VALIDATION
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User '{db_user.name}' created with ID {db_user.id} and is pending validation.")
    return db_user

def get_user_by_name(db: Session, name: str) -> User | None:
    """Retrieves a user by their name."""
    return db.query(User).filter(User.name == name).first()

def get_user_by_id(db: Session, user_id: int) -> User | None:
    """Retrieves a user by their id."""
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """Retrieves all active users."""
    logger.debug(f"Fetching all active users with skip={skip}, limit={limit}")
    return db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()

def update_user(db: Session, user: User, user_update: UserUpdate) -> User:
    """Updates a user's information."""
    logger.info(f"Updating user with ID: {user.id}")
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    logger.info(f"User with ID {user.id} has been updated.")
    return user

def delete_user(db: Session, user: User) -> User:
    """Soft deletes a user by setting is_active to False."""
    logger.info(f"Soft deleting user with ID: {user.id}")
    user.is_active = False
    db.commit()
    db.refresh(user)
    logger.info(f"User with ID {user.id} has been soft deleted.")
    return user