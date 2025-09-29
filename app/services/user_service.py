import logging
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate

logger = logging.getLogger(__name__)

def create_user(db: Session, user_create: UserCreate) -> User:
    """Creates a new user in the database."""
    logger.info(f"Creating user with name: {user_create.name}")
    db_user = User(name=user_create.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User '{db_user.name}' created with ID {db_user.id}")
    return db_user

def get_user_by_name(db: Session, name: str) -> User | None:
    """Retrieves a user by their name."""
    return db.query(User).filter(User.name == name).first()

def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """Retrieves all users."""
    logger.debug(f"Fetching all users with skip={skip}, limit={limit}")
    return db.query(User).offset(skip).limit(limit).all()