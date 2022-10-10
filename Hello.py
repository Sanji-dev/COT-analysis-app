import streamlit as st
import pandas as pd
from datetime import date

major_fx = ['EUR','JPY','AUD','NZD','CAD','GBP','CHF']

st.set_page_config(
    page_title="COT Datas",
    page_icon="📊",
)

st.title("Commitments of traders - Datas 📊")
st.markdown(
    """
    Cette application a pour objectif de faciliter l'analyse des rapports "Commitments of traders", issues du site [cftc.gov](https://www.cftc.gov/).
    Les données récupérées sont des contrats à terme non commerciaux, tels que les devises forex majeures essentiellement.
    💵 💴 💶 💷  

    La finalité est de déduire **l'Orderflow de la Smart Money** de manière la plus probable en fonction de nos analyses.
"""
)

st.header("Tableaux de données par devise")
option = st.selectbox(
    'Quelle devise voulez-vous ?',
     major_fx)

st.subheader(f"Rapports pour **{option}**")

#Lis le fichier CSV en fonction de la devise sélectionnée
df = pd.read_csv(f"csv_folder/{option.lower()}.csv", index_col='Date')
dates = list(df.index)
start = st.select_slider("Date de début", options = dates, value=(dates[-1]))
st.write("Début:", dates.index(start))

st.table(df.head(dates.index(start)+1).style.background_gradient(axis=0))
@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(df)

date = df.index[0].replace("/","-")
st.download_button(
    label="Exporter le CSV",
    data=csv,
    file_name=f'{option}_{date}.csv',
    mime='text/csv',
)

