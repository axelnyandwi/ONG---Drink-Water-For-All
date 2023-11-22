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

# Reformatage des nombres de population et de mort
population_data['Population'] = population_data['Population'].astype(str).str.replace('.', '', regex=False)
population_data['Population'] = pd.to_numeric(population_data['Population'], errors='coerce')

mortality_data['WASH deaths'] = mortality_data['WASH deaths'].astype(str).str.split('.').str[0]
mortality_data['WASH deaths'] = pd.to_numeric(mortality_data['WASH deaths'], errors='coerce')

# Jointure entre les datasets population_data et region_data par le champ "Country"
join_population_continent = pd.merge(population_data, region_data, left_on="Country", right_on="COUNTRY (DISPLAY)", how="left")

# Jointure entre les datasets mortality_data, stability_data et region_data
join_mortality_stability = pd.merge(mortality_data, stability_data, on=["Country", "Year"])
join_mortality_stability_continent = pd.merge(join_mortality_stability, region_data, left_on="Country", right_on="COUNTRY (DISPLAY)", how="left")

# Vue continentale
st.title("Vue Continentale")

st.markdown(
    """
    Agrégation des indicateurs en fonction du continent sélectionné.
"""
)

# Création d'un graphique d'évolution de la population par continent par année
st.subheader("Évolution de la population par continent entre 2000 et 2018")

# Sélection de la granularité par l'utilisateur
selected_granularity_pop = st.selectbox("Sélectionnez une granularité pour la population", population_data["Granularity"].unique())

# Filtrer les données en fonction de la granularité sélectionnée
filtre_pop_data = join_population_continent[join_population_continent["Granularity"] == selected_granularity_pop]

# Grouper les données par année et par continent
group_population_data = filtre_pop_data.groupby(["Year", "REGION (DISPLAY)"]).agg({"Population": "sum"}).reset_index()

fig_all_continents_population = px.line(
    group_population_data,
    x="Year",
    y="Population",
    color="REGION (DISPLAY)",
    labels={"REGION (DISPLAY)": "Continent"},
)

st.plotly_chart(fig_all_continents_population)

# Sélection du continent par l'utilisateur
filtre_continent = st.selectbox("Sélectionnez un continent", region_data["REGION (DISPLAY)"].unique())

# Filtrer les données du continent sélectionné
selection_continent = region_data[region_data["REGION (DISPLAY)"] == filtre_continent]
# Obtenir la liste des pays du continent sélectionné
selection_pays = selection_continent["COUNTRY (DISPLAY)"]
# Créer un masque booléen pour les pays du continent dans water_data
mask_selection_pays = water_data["Country"].isin(selection_pays)
# Filtrer les données d'eau pour inclure uniquement les pays du continent sélectionné
continent_water_data = water_data[mask_selection_pays]

# Filtrer les données du continent sélectionné pour la mortalité
selection_continent_mortality = region_data[region_data["REGION (DISPLAY)"] == filtre_continent]
# Obtenir la liste des pays du continent sélectionné pour la mortalité
selection_pays_mortality = selection_continent_mortality["COUNTRY (DISPLAY)"]
# Créer un masque booléen pour les pays du continent dans mortality_data
mask_selection_pays_mortality = mortality_data["Country"].isin(selection_pays_mortality)
# Filtrer les données de mortalité pour inclure uniquement les pays du continent sélectionné
continent_mortality_data = mortality_data[mask_selection_pays_mortality]


# Affichage des graphiques

st.subheader(f"Nombre de mort et taux de mortalité dû à de l'eau insalubre en 2016 - {filtre_continent}")

mort_par_continent = round(continent_mortality_data["WASH deaths"].sum(),0)
st.write(f"Il y'a eu {mort_par_continent} morts dû à une exposition à une eau insalubre en 2016.")

taux_mort_par_continent = round(continent_mortality_data["Mortality rate attributed to exposure to unsafe WASH services"].mean(),2)
st.write(f"Le taux de mortalité moyen dû à une exposition à une eau insalubre en 2016 est de {taux_mort_par_continent}%.")

st.subheader(f"Taux de mortalité dû à de l'eau insalubre sur carte en 2016 - {filtre_continent}")
# Création d'une carte pour le taux de mortalité par continent
fig_map_continent = px.choropleth(
    continent_mortality_data,
    locations="Country",
    locationmode="country names",
    color="Mortality rate attributed to exposure to unsafe WASH services",
    hover_name="Country",
    color_continuous_scale=px.colors.sequential.Viridis,
    projection="natural earth",
    width=1000,
    height=600,
    labels={'Mortality rate attributed to exposure to unsafe WASH services': 'Taux en %'} 
)

st.plotly_chart(fig_map_continent)


st.subheader("Le nombre de mort et taux de mortalité dû à l'eau insalubre en 2016 dans le monde par continent et pays")

fig = px.scatter(
    join_mortality_stability_continent, 
    x='Political_Stability', 
    y='WASH deaths', 
    color='REGION (DISPLAY)',
    size= "Mortality rate attributed to exposure to unsafe WASH services",
    hover_name="COUNTRY (DISPLAY)",
    labels={"REGION (DISPLAY)": "Continent", "COUNTRY (DISPLAY)": "Pays"},
)
st.plotly_chart(fig)

