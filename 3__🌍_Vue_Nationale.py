import streamlit as st
import pandas as pd
import plotly.express as px

# Chargement des données
water_data = pd.read_csv("https://raw.githubusercontent.com/axelnyandwi/dashboard_ong/main/BasicAndSafelyManagedDrinkingWaterServices.csv")
mortality_data = pd.read_csv("https://raw.githubusercontent.com/axelnyandwi/dashboard_ong/main/MortalityRateAttributedToWater.csv")
stability_data = pd.read_csv("https://raw.githubusercontent.com/axelnyandwi/dashboard_ong/main/PoliticalStability.csv")
population_data = pd.read_csv("https://raw.githubusercontent.com/axelnyandwi/dashboard_ong/main/Population.csv")
region_data = pd.read_csv("https://raw.githubusercontent.com/axelnyandwi/dashboard_ong/main/RegionCountry.csv")

# Filtrer les lignes avec Granularity = "Total"
water_data = water_data[water_data["Granularity"] == "Total"]
mortality_data = mortality_data[mortality_data["Granularity"] == "Total"]

# Supprimez les chiffres après le point dans la colonne 'Population'
population_data['Population'] = population_data['Population'].astype(str).str.replace('.', '', regex=False)
population_data['Population'] = pd.to_numeric(population_data['Population'], errors='coerce')

# Supprimez les chiffres après le point dans la colonne 'WASH deaths'
mortality_data['WASH deaths'] = mortality_data['WASH deaths'].astype(str).str.split('.').str[0]
mortality_data['WASH deaths'] = pd.to_numeric(mortality_data['WASH deaths'], errors='coerce')

# Vue nationale
st.title("Vue Nationale")

st.markdown(
    """
    Agrégation des indicateurs en fonction du pays sélectionné.
"""
)

# Sélection du pays par l'utilisateur
filtre_pays = st.selectbox("Sélectionnez un pays", water_data["Country"].unique())

# Filtrer les données en fonction du pays sélectionné
country_water_data = water_data[water_data["Country"] == filtre_pays]
country_mortality_data = mortality_data[mortality_data["Country"] == filtre_pays]
# Filtrer les données en fonction du pays sélectionné
population_data_tot = population_data[population_data["Granularity"] == "Total"]
country_population_data = population_data_tot[population_data_tot["Country"] == filtre_pays]

# Création d'un graphique d'évolution de la population par pays par an
st.subheader(f"Évolution de la population entre 2000 et 2018 - {filtre_pays}")
fig_country_population = px.bar(
    country_population_data,
    x="Year",
    y="Population",
    labels={"Population": f"Population - {filtre_pays}"}
)

st.plotly_chart(fig_country_population)

# Création d'un graphique de répartition de la population par typologie de résidence
st.subheader(f"Répartition de la population par typologie de résidence - {filtre_pays}")

filtre_année = st.slider("Sélectionnez une année", 
    min_value=stability_data['Year'].min(), 
    max_value=stability_data['Year'].max(), 
    value=stability_data['Year'].min()
)

population_data_urb_rur = population_data[(population_data["Granularity"] == "Rural") & (population_data["Year"] == filtre_année) | (population_data["Granularity"] == "Urban") & (population_data["Year"] == filtre_année)]
country_population_data_urb_rur = population_data_urb_rur[population_data_urb_rur["Country"] == filtre_pays]

fig_pie_chart_population = px.pie(
    country_population_data_urb_rur,
    names="Granularity",
    values="Population",
    title=f"en {filtre_année}"
)
st.plotly_chart(fig_pie_chart_population)

# Agrégation au niveau du pays
agg_country_water_data = country_water_data.groupby("Year")[["Population using at least basic drinking-water services (%)","Population using safely managed drinking-water services (%)"]].mean().reset_index()
agg_country_mortality_data = country_mortality_data.groupby("Year")[["Mortality rate attributed to exposure to unsafe WASH services","WASH deaths"]].mean().reset_index()

st.subheader(f"Nombre de mort et taux de mortalité dû à de l'eau insalubre en 2016 - {filtre_pays}")

mort_par_pays = round(country_mortality_data["WASH deaths"].sum(),0)
st.write(f"Il y'a eu {mort_par_pays} morts dû à une exposition à une eau insalubre en 2016.")

taux_mort_par_pays = round(country_mortality_data["Mortality rate attributed to exposure to unsafe WASH services"].mean(),2)
st.write(f"Le taux de mortalité moyen dû à une exposition à une eau insalubre en 2016 est de {taux_mort_par_pays}%.")

st.subheader(f"Population mondiale ayant accès à une eau sûre ou basique - {filtre_pays}")
fig_country_population = px.line(agg_country_water_data, x="Year", y=["Population using at least basic drinking-water services (%)","Population using safely managed drinking-water services (%)"], labels={"value": "Percentage"})
st.plotly_chart(fig_country_population)

st.subheader(f"Stabilité politique au fil du temps entre 2000 et 2018 - {filtre_pays}")

# Filtrer les données en fonction du pays sélectionné
country_stability_data = stability_data[stability_data["Country"] == filtre_pays]

# Vérifie si l'indice de stabilité est disponible pour le pays sélectionné
if not country_stability_data.empty:
    fig_country_stability = px.line(country_stability_data, 
        x="Year",
        y="Political_Stability",
        )
    st.plotly_chart(fig_country_stability)
else:
    st.warning(f"Aucune donnée de stabilité politique disponible pour {filtre_pays}")