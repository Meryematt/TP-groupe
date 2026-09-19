from fastapi import FastAPI
from app.routers import produits, ventes, vendeurs, regions, kpi


app = FastAPI(title="NordCommerce", description="Gestion des produits, ventes, vendeurs et régions", version="1.0.0")

app.include_router(produits.router)
app.include_router(ventes.router)    
app.include_router(vendeurs.router)
app.include_router(regions.router)
app.include_router(kpi.router)