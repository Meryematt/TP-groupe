from pydantic import BaseModel
from datetime import date

class Vente(BaseModel):
    produit_id: int
    date_vente: date
    vendeur_id: int
    produit_id: int
    quantite: int
    montant_total: float


class VenteOut(Vente):
    id : int