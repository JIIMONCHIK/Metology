from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/api/pickup-points", tags=["pickup-points"])

@router.get("/", response_model=List[schemas.PickupPoint])
def get_pickup_points(db: Session = Depends(get_db)):
    """Возвращает список всех пунктов выдачи."""
    return crud.get_pickup_points(db)

@router.get("/{point_id}", response_model=schemas.PickupPoint)
def get_pickup_point(point_id: int, db: Session = Depends(get_db)):
    """Возвращает пункт выдачи по ID."""
    return crud.get_pickup_point(db, point_id)