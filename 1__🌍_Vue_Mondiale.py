import streamlit as st
import pandas as pd
import plotly.express as px

# Chargement des données
water_data = pd.read_csv("https://raw.githubusercontent.com/axelnyandwi/dashboard_ong/main/BasicAndSafelyManagedDrinkingWaterServices.csv")
mortality_data = pd.read_csv("https://raw.githubusercontent.com/axelnyandwi/dashboard_ong/main/MortalityRateAttributedToWater.csv")
stability_data = pd.read_csv("https://raw.githubusercontent.com/axelnyandwi/dashboard_ong/main/PoliticalStability.csv")
population_data = pd.read_csv("https://raw.githubusercontent.com/axelnyandwi/dashboard_ong/main/Population.csv")
region_data = pd.read_csv("https://raw.githubusercontent.com/axelnyandwi/dashboard_ong/main/RegionCountry.csv")

# Filtrer les lignes pour garder les lignes présentant la granularité total
water_data = water_data[water_data["Granularity"] == "Total"]
mortality_data = mortality_data[mortality_data["Granularity"] == "Total"]
population_data = population_data[population_data["Granularity"] == "Total"]

# Reformatage des nombres de population et de mort
population_data['Population'] = population_data['Population'].astype(str).str.replace('.', '', regex=False)
population_data['Population'] = pd.to_numeric(population_data['Population'], errors='coerce')

mortality_data['WASH deaths'] = mortality_data['WASH deaths'].astype(str).str.split('.').str[0]
mortality_data['WASH deaths'] = pd.to_numeric(mortality_data['WASH deaths'], errors='coerce')

# Jointure entre mortality_data et stability_data grâce au pays et à l'année
join_mort_stab = pd.merge(mortality_data, stability_data, on=["Country", "Year"], how="inner")

# Vue mondiale
st.title("Vue Mondiale")

st.markdown(
    """
    Agrégation des indicateurs au niveau mondial.
"""
)

# Graphique d'évolution de la population mondiale par année
st.subheader("Évolution de la population mondiale par année")

group_population_an = population_data.groupby("Year")["Population"].sum().reset_index()

fig_population = px.bar(
    group_population_an,
    x="Year",
    y="Population",
    labels={"Population": "Population mondiale"},
)

st.plotly_chart(fig_population)

# Taux de mortalité dû à de l'eau insalubre
st.subheader("Nombre de mort et taux de mortalité dû à de l'eau insalubre en 2016")

# bouton switch pour filtrer les pays stables
filtre_stable = st.checkbox("Afficher seulement les données pour les pays stables (où l'indice de stabilité politique est supérieur à 0)")

# Calcul du nombre de mort dû à l'eau insalubre
nb_mort = mortality_data["WASH deaths"].sum()
round_nb_mort = round(nb_mort, 0)

# Afficher la valeur brute par défaut
nb_mort_tot = round_nb_mort

# Vérifie l'état du bouton switch
if filtre_stable:
    # Filtre pour un indice de stabilité politique supérieur à 0
    filtre_pays_stable = join_mort_stab[join_mort_stab["Political_Stability"] > 0]
    # Calcul du nombre de mort pour les pays stables
    nb_mort_filtre = filtre_pays_stable["WASH deaths"].sum()
    round_nb_mort_filtre = round(nb_mort_filtre,0)

    # Met à jour la valeur affichée si le bouton est activé
    nb_mort_tot = round_nb_mort_filtre

# Afficher la valeur (qu'elle soit filtrée ou non)
st.write(f"Il y'a eu {nb_mort_tot} morts dû à une exposition à une eau insalubre en 2016.")

# Calcul du taux de mortalité
mortality_value = mortality_data["Mortality rate attributed to exposure to unsafe WASH services"].mean()
round_mortality_value = round(mortality_value, 2)

mortality_value_tot = round_mortality_value

if filtre_stable:
    # Calcul de la moyenne du taux de mortalité
    mortality_value_filtre = filtre_pays_stable["Mortality rate attributed to exposure to unsafe WASH services"].mean()
    round_mortality_value_filtre = round(mortality_value_filtre, 2)

    # Met à jour la valeur affichée si le bouton est activé
    mortality_value_tot = round_mortality_value_filtre

# Afficher la valeur (qu'elle soit filtrée ou non)
st.write(f"Le taux de mortalité moyen dû à une exposition à une eau insalubre en 2016 est de {mortality_value_tot}%.")

# Création et affichage d'une carte
st.subheader("Taux de mortalité en 2016 dû à de l'eau insalubre sur une carte")
fig_map = px.choropleth(
    mortality_data,
    locations="Country",
    locationmode="country names",
    color="Mortality rate attributed to exposure to unsafe WASH services",
    hover_name="Country",
    color_continuous_scale=px.colors.sequential.Viridis,
    projection="natural earth",
    width=800,  # Ajuster la largeur en pixels
    height=500,
    labels={'Mortality rate attributed to exposure to unsafe WASH services': 'Taux en %'}   # Ajuster la hauteur en pixels
)

st.plotly_chart(fig_map)

st.subheader("La stabilité politique mondiale par an")

# Filtre par année
filtre_année = st.slider("Sélectionnez une année", 
    min_value=stability_data['Year'].min(), 
    max_value=stability_data['Year'].max(), 
    value=stability_data['Year'].min()
)

filtre_indice_stabilite = stability_data[stability_data['Year'] == filtre_année]

fig = px.choropleth(
    filtre_indice_stabilite,
    locations="Country",
    locationmode="country names",
    color="Political_Stability",
    hover_name="Country",
    title=f"en {filtre_année}",
    color_continuous_scale=px.colors.sequential.Blues,
    projection="natural earth",
    width=800,
    height=500,
    labels={'Political_Stability': 'Indice de stabilité politique'}
)

st.plotly_chart(fig)

