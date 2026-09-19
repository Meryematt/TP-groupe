from fastapi import APIRouter, Depends, HTTPException
from app.schemas.vendeurs import VendeurOut
from app.models import Vendeur
from app.database import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session


router = APIRouter(prefix="/vendeurs", tags=["Vendeurs"])

@router.get("/")
async def read_vendeurs(db: Session = Depends(get_db)):
    req = select(Vendeur).order_by(Vendeur.id)
    vendeurs = db.scalars(req).all()
    return vendeurs