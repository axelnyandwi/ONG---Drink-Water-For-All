import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Accueil",
)

st.title("Analyse de l'accès à l'eau potable dans le monde pour l'ONG DWFA")

st.markdown(
    """
    Ce tableau de bord présente une vue globale de l’accès à l’eau potable dans le monde.
    Vous pouvez naviguer dans celui-ci grâce au volet à gauche, vous permettant de sélectionner
    la granularité géographique sur laquelle vous souhaitez visualiser vos données. La réalisation
    de ce dashboard se situe dans le cadre d'une mission confiée par l'ONG DWFA (Drink Water For All)
    ### Les domaines d'expertise de DWFA
    - Création de services d’accès à l’eau potable.
    - Modernisation de services d’accès à l’eau déjà existants.
    - Consulting auprès d’administrations/gouvernements à propos des politiques d’accès à l’eau.
    ### Les objectifs du tableau de bord
    - Une vue d'ensemble sur l'accès à l'eau potable dans le monde
    - Identifier un pays dans lequelle financer un projet dans un domaine d'expertise
    ### Les sources
    - [Food and Agriculture Organization of the United Nations](http://www.fao.org/)
    - [World Health Organization](https://apps.who.int/gho/)
"""
)
image_url = "https://github.com/axelnyandwi/dashboard_ong/blob/main/picture.png?raw=true"
st.image(image_url, use_column_width=True)

def vue_mondiale():
    st.title("Vue Mondiale")
    # ... code spécifique à la vue mondiale ...

def vue_continentale():
    st.title("Vue Continentale")
    # ... code spécifique à la vue continentale ...

def vue_nationale():
    st.title("Vue Nationale")
    # ... code spécifique à la vue nationale ...

# Liste des options pour la boîte de sélection
options = ["Vue Mondiale", "Vue Continentale", "Vue Nationale"]
selected_page = st.selectbox("Sélectionnez une vue", options)

# Afficher la page sélectionnée
if selected_page == "Vue Mondiale":
    vue_mondiale()
elif selected_page == "Vue Continentale":
    vue_continentale()
elif selected_page == "Vue Nationale":
    vue_nationale()



