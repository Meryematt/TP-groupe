from pydantic import BaseModel

class Produit(BaseModel):
    nom: str
    categorie: str
    prix_unitaire: float


class ProduitOut(Produit):
    id : int