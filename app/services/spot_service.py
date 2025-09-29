import logging
from sqlalchemy.orm import Session, joinedload
from app.models.spot import Spot
from app.schemas.spot import SpotCreate

logger = logging.getLogger(__name__)

def create_spot(db: Session, spot_create: SpotCreate) -> Spot:
    """Creates a new spot."""
    logger.info(f"Creating spot '{spot_create.name}' at ({spot_create.latitude}, {spot_create.longitude})")
    db_spot = Spot(**spot_create.model_dump())
    db.add(db_spot)
    db.commit()
    db.refresh(db_spot)
    logger.info(f"Spot '{db_spot.name}' created with ID {db_spot.id}")
    return db_spot

def get_spot_by_id(db: Session, spot_id: int) -> Spot | None:
    """Retrieves a single spot by its ID."""
    logger.debug(f"Fetching spot with id={spot_id}")
    return db.query(Spot).options(joinedload(Spot.created_by)).filter(Spot.id == spot_id).first()

def get_all_spots(db: Session, skip: int = 0, limit: int = 100) -> list[Spot]:
    """Retrieves all spots."""
    logger.debug(f"Fetching all spots with skip={skip}, limit={limit}")
    return db.query(Spot).options(joinedload(Spot.created_by)).offset(skip).limit(limit).all()