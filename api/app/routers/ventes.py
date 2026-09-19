from fastapi import APIRouter, Depends, HTTPException
from app.schemas.ventes import VenteOut
from app.models import Vente, Vendeur, Produit, Region
from app.database import get_db
from sqlalchemy import select, func
from sqlalchemy.orm import Session


router = APIRouter(prefix="/ventes", tags=["Ventes"])

@router.get("")
async def read_ventes(db: Session = Depends(get_db)):
    req = select(Vente).order_by(Vente.id)
    ventes = db.scalars(req).all()
    return ventes

@router.get("/nb_ventes")
async def nb_ventes(
    region: str | None = None,
    categorie: str | None = None,
    date_debut: str | None = None,
    date_fin: str | None = None,
    db: Session = Depends(get_db)
):
    req = (
        select(func.count(Vente.id))
        .join(Vendeur, Vendeur.id == Vente.vendeur_id)
        .join(Region, Region.id == Vendeur.region_id)
        .join(Produit, Produit.id == Vente.produit_id)
    )
    if region is not None:
        req = req.where(Region.nom == region)
    if categorie is not None:
        req = req.where(Produit.categorie == categorie)
    if date_debut is not None:
        req = req.where(Vente.date_vente >= date_debut)
    if date_fin is not None:
        req = req.where(Vente.date_vente <= date_fin)

    nb_ventes = db.scalar(req)
    return nb_ventes

@router.get("/panier_moyen")
async def panier_moyen(
    region: str | None = None,
    categorie: str | None = None,
    date_debut: str | None = None,
    date_fin: str | None = None,
    db: Session = Depends(get_db)
):
    req = (
        select(func.coalesce(func.avg(Vente.montant_total), 0))
        .join(Vendeur, Vendeur.id == Vente.vendeur_id)
        .join(Region, Region.id == Vendeur.region_id)
        .join(Produit, Produit.id == Vente.produit_id)
    )
    if region is not None:
        req = req.where(Region.nom == region)
    if categorie is not None:
        req = req.where(Produit.categorie == categorie)
    if date_debut is not None:
        req = req.where(Vente.date_vente >= date_debut)
    if date_fin is not None:
        req = req.where(Vente.date_vente <= date_fin)
    panier_moyen = db.scalar(req)
    return panier_moyen