from fastapi import APIRouter, Depends, HTTPException
from app.schemas.regions import RegionOut
from app.models import Region
from app.database import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session


router = APIRouter(prefix="/regions", tags=["Regions"])

@router.get("/")
async def get_regions(db: Session = Depends(get_db)):
    req = select(Region.nom).order_by(Region.nom)
    regions = db.scalars(req).all()
    return regions