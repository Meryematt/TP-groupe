from sqlalchemy.ext.automap import automap_base
from app.database import engine

Base = automap_base()
Base.prepare(autoload_with=engine)

Produit = Base.classes.produits
Vendeur = Base.classes.vendeurs
Region = Base.classes.regions
Vente = Base.classes.ventes