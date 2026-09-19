from fastapi import APIRouter, Depends, HTTPException
from app.models import Produit
from app.schemas.produits import ProduitOut
from app.database import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session


router = APIRouter(prefix="/categories", tags=["Produits"])

@router.get("")
async def get_categories(db: Session = Depends(get_db)):
    req = select(Produit.categorie).distinct().order_by(Produit.categorie)
    categories = db.scalars(req).all()
    return categories