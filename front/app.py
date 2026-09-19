import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide")

API_URL = "http://127.0.0.1:8001"

st.title("**Dashboard KPI Ventes - NordCommerce**")

st.sidebar.header("Filtres")

periode = st.sidebar.date_input("Période", value=())

@st.cache_data(ttl="30s")
def get_regions(url: str):
    response = requests.get(f"{url}/regions")
    response.raise_for_status()
    return response.json()

@st.cache_data(ttl="30s")
def get_categories(url: str):
    response = requests.get(f"{url}/categories")
    response.raise_for_status()
    return response.json()

regions = get_regions(API_URL)
region_choisie = st.sidebar.selectbox("Région", ["Toutes"] + regions)

categories = get_categories(API_URL)
categorie_choisie = st.sidebar.selectbox("Catégorie", ["Toutes"] + categories)

params = {}

if len(periode) == 2:
    params["date_debut"] = periode[0]
    params["date_fin"] = periode[1]

if region_choisie != "Toutes":
    params["region"] = region_choisie

if categorie_choisie != "Toutes":
    params["categorie"] = categorie_choisie


@st.cache_data(ttl="30s")
def get_ventes(url : str, params : dict):
    response = requests.get(f"{url}/ventes", params=params)
    response.raise_for_status()
    return response.json()


@st.cache_data(ttl="30s")
def ca_total(url : str, params : dict):
    response = requests.get(f"{url}/kpi/ca_total", params=params)
    response.raise_for_status()
    return response.json()

@st.cache_data(ttl="30s")
def ca_par_region(url : str, params : dict):
    response = requests.get(f"{url}/kpi/ca_par_region", params=params)
    response.raise_for_status()
    return response.json()

@st.cache_data(ttl="30s")
def evolution_ca(url : str, params : dict):
    response = requests.get(f"{url}/kpi/evolution_mensuelle", params=params)
    response.raise_for_status()
    return response.json()

@st.cache_data(ttl="30s")
def nb_ventes(url : str, params : dict):
    response = requests.get(f"{url}/ventes/nb_ventes", params=params)
    response.raise_for_status()
    return response.json()

@st.cache_data(ttl="30s")
def panier_moyen(url : str, params : dict):
    response = requests.get(f"{url}/ventes/panier_moyen", params=params)
    response.raise_for_status()
    return response.json()


@st.cache_data(ttl="30s")
def top1_vendeurs(url : str, params : dict):
    response = requests.get(f"{url}/kpi/top1_vendeurs", params=params)
    response.raise_for_status()
    return response.json()


caTotal = ca_total(API_URL, params=params)
nbVentes = nb_ventes(API_URL, params=params)
panierMoyen = panier_moyen(API_URL, params=params)

col1, col2, col3 = st.columns(3)
col1.metric("CA total", f"{caTotal['chiffre_affaires']:,.2f} €".replace(","," "))
col2.metric("Nombre de ventes", nbVentes)
col3.metric("Panier Moyen", f"{panierMoyen:.2f} €")

st.divider()

caRegion = ca_par_region(API_URL, params=params)
evolutionCA = evolution_ca(API_URL, params=params)

col4, col5 = st.columns(2)

with col4:
    st.subheader("CA par région")    
    df_region = pd.DataFrame(caRegion["Chiffre d'affaire par region"])
    st.bar_chart(df_region.set_index("region"))

with col5:
    st.subheader("Évolution du CA")
    if evolutionCA:
        df_produit = pd.DataFrame(evolutionCA)
        st.line_chart(df_produit.set_index("mois"))
    else :
        st.info("Aucune donnée pour ces filtres.")

st.divider()

st.subheader("Top vendeurs")
df = pd.DataFrame(top1_vendeurs(API_URL, params))
st.dataframe(df, hide_index=True)




