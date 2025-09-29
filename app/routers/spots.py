import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.spot import Spot, SpotCreate
from app.services import spot_service

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/spots", response_model=Spot, status_code=status.HTTP_201_CREATED)
def create_spot(spot: SpotCreate, db: Session = Depends(get_db)):
    """
    Create a new spot on the map.
    """
    return spot_service.create_spot(db=db, spot_create=spot)

@router.get("/spots", response_model=List[Spot])
def read_spots(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all spots.
    """
    spots = spot_service.get_all_spots(db, skip=skip, limit=limit)
    return spots

@router.get("/spots/{spot_id}", response_model=Spot)
def read_spot(spot_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single spot by its ID.
    """
    db_spot = spot_service.get_spot_by_id(db, spot_id=spot_id)
    if db_spot is None:
        logger.error(f"Spot with id {spot_id} not found.")
        raise HTTPException(status_code=404, detail="Spot not found")
    return db_spot