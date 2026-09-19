from fastapi import APIRouter, Depends, HTTPException
from app.models import Vente, Vendeur, Region, Produit
from app.database import get_db
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from datetime import date



router = APIRouter(prefix="/kpi", tags=["KPI"])

@router.get("/ca_total")
async def ca_total(
    region: str | None = None,
    categorie: str | None = None,
    date_debut: str | None = None,
    date_fin: str | None = None,
    db: Session = Depends(get_db)
):
    req = (
        select(func.coalesce(func.sum(Vente.montant_total), 0))
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
    
    ca = db.scalar(req)
    return {"chiffre_affaires" : ca}


@router.get("/ca_par_region")
async def ca_par_region(region: str | None = None, db: Session = Depends(get_db)):
    req = (
        select(Region.nom, func.sum(Vente.montant_total).label("ca"))
        .join(Vendeur, Vendeur.region_id == Region.id)
        .join(Vente, Vente.vendeur_id == Vendeur.id)
        .group_by(Region.nom)
        .order_by(func.sum(Vente.montant_total).desc())
    )
    if region is not None:
            req = req.where(Region.nom == region)
    resultats = db.execute(req).all()
    test = [{"region": r.nom, "ca": r.ca} for r in resultats]
    return {"Chiffre d'affaire par region":test}

@router.get("/ca_par_produit")
async def ca_par_produit(categorie : str | None = None, db: Session = Depends(get_db)):
    req = (
        select(Produit.categorie, func.sum(Vente.montant_total).label("ca"))
        .join(Vente, Vente.produit_id == Produit.id)
        .join(Vendeur, Vendeur.id == Vendeur.id)
        .group_by(Produit.categorie)
        .order_by(func.sum(Vente.montant_total).desc())
    )
    if categorie is not None:
        req = req.where(Produit.categorie == categorie)
    resultats = db.execute(req).all()
    return [{"categorie": r.categorie, "ca": r.ca} for r in resultats]

@router.get("/evolution_mensuelle")
async def ca_par_mois(date_debut : date | None = None, date_fin : date | None = None, db: Session = Depends(get_db)):
    mois = func.to_char(Vente.date_vente, 'YYYY-MM').label("mois")
    req = (
        select(mois, func.sum(Vente.montant_total).label("ca"))
        .group_by(mois)
        .order_by(mois)
    )
    if date_debut is not None:
        req = req.where(Vente.date_vente >= date_debut)
    if date_fin is not None:
        req = req.where(Vente.date_vente <= date_fin)
    result = db.execute(req).all()
    return [{"mois": row.mois, "ca": row.ca} for row in result]


@router.get("/top_vendeurs")
async def ca_par_vendeur(
    region: str | None = None,
    categorie: str | None = None,
    date_debut: str | None = None,
    date_fin: str | None = None,
    db: Session = Depends(get_db)
):
    req = (
        select(Vendeur.nom, func.sum(Vente.montant_total).label("ca"))
        .join(Vente, Vente.vendeur_id == Vendeur.id)
        .group_by(Vendeur.nom)
        .order_by(func.sum(Vente.montant_total).desc())
    )
    if region is not None:
        req = req.where(Region.nom == region)
    if categorie is not None:
        req = req.where(Produit.categorie == categorie)
    if date_debut is not None:
        req = req.where(Vente.date_vente >= date_debut)
    if date_fin is not None:
        req = req.where(Vente.date_vente <= date_fin)
    result = db.execute(req).all()
    return [{"vendeur": row.nom, "ca": row.ca} for row in result]


@router.get("/top1_vendeurs")
async def top1_vendeurs(
    region: str | None = None,
    categorie: str | None = None,
    date_debut: str | None = None,
    date_fin: str | None = None,
    db: Session = Depends(get_db)
):
    req = (
        select(Vendeur.nom.label("nom_vendeur"), Region.nom.label("nom_region"), func.sum(Vente.montant_total).label("ca"), func.count(Vente.id).label("nb_ventes"))
        .join(Vente, Vente.vendeur_id == Vendeur.id)
        .join(Region, Region.id == Vendeur.region_id)
        .group_by(Vendeur.nom, Region.nom)
        .order_by(func.sum(Vente.montant_total).desc())
        .limit(1)
    )
    if region is not None:
        req = req.where(Region.nom == region)
    if categorie is not None:
        req = req.where(Produit.categorie == categorie)
    if date_debut is not None:
        req = req.where(Vente.date_vente >= date_debut)
    if date_fin is not None:
        req = req.where(Vente.date_vente <= date_fin)
    result = db.execute(req).all()
    return [{"vendeur": row.nom_vendeur, "region": row.nom_region, "ca": row.ca, "nb_ventes": row.nb_ventes} for row in result]

