import streamlit as st
import pandas as pd
from datetime import date
import seaborn as sns

major_fx = ['EUR','JPY','AUD','NZD','CAD','GBP','CHF']
CHICAGO = [
            ['EUR','Code-099741','deacmesf','forex',[]], #Asset , Code, End_url, Type(folder), List of value
            ['JPY','Code-097741','deacmesf','forex',[]],
            ['AUD','Code-232741','deacmesf','forex',[]],
            ['NZD','Code-112741','deacmesf','forex',[]],
            ['CAD','Code-090741','deacmesf','forex',[]],
            ['GBP','Code-096742','deacmesf','forex',[]],
            ['CHF','Code-092741','deacmesf','forex',[]],
            ['MXN','Code-095741','deacmesf','forex',[]],
            ['BRL','Code-102741','deacmesf','forex',[]],
            ['ZAR','Code-122741','deacmesf','forex',[]],
            ['BTC','Code-133741','deacmesf','crypto',[]],
            ['ETH','Code-146021','deacmesf','crypto',[]],
            ['NASDAQ-100','Code-209742','deacmesf','index',[]],
            ['S&P 500','Code-13874A','deacmesf','index',[]],

]

USD = [['USD','Code-098662','deanybtsf','forex',[]]]

NEW_YORK = [
            ['OIL','Code-067651','deanymesf','other',[]],
            ['GAS','Code-023651','deanymesf','other',[]],
]

COMMODITY = [
            ['SILVER','Code-084691','deacmxsf','metals',[]],
            ['COPPER','Code-085692','deacmxsf','metals',[]],
            ['GOLD','Code-088691','deacmxsf','metals',[]],
]

ALL_ASSET = CHICAGO + USD + NEW_YORK + COMMODITY


st.set_page_config(
    page_title="Rapports COT",
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

@st.cache
def csv_to_dataframe(file, index="Date"):
    return pd.read_csv(file, index_col=index)

@st.cache
def compare_row(dataframe):
    new_net = dataframe.iloc[0,4]
    old_net = dataframe.iloc[1,4]
    if new_net > old_net:
        return "↗️"
    if new_net < old_net:
        return "↘️"
    if new_net == old_net:
        return "➡️"

#@st.cache
#def convert_df(df):
#    return df.to_csv().encode('utf-8')

st.header("Tableaux de données par actifs")

#Liste de tous les actifs par leur nom
choices_asset = [item[0] for item in ALL_ASSET]

#Récupère l'index de l'USD dans la liste pour l'afficher par défaut dans la selectbox
for i,choice in enumerate(choices_asset):
    if choice == 'USD':
        usd_index = i

#Change color gradient
cm = sns.blend_palette(['red','white','green'], as_cmap=True, n_colors=4)

df = csv_to_dataframe("csv_folder/forex/usd.csv")
#Liste de toutes les dates
dates = list(df.index)

#Input slider pour filter la date range
start = st.select_slider("Sélectionner la date de début", options = dates, value=("19/07/22"))

st.caption("Etude sur **{}** semaines".format(dates.index(start)+1))

col1, col2 = st.columns(2)

with col1:
    option = st.selectbox(
    'Premier actif ?', choices_asset, index=usd_index
     )
    index = choices_asset.index(option)
    #Lis le fichier CSV en fonction de l'actif sélectionné
    df = csv_to_dataframe(f"csv_folder/{ALL_ASSET[index][3]}/{option.lower()}.csv",'Date')
    df = df.drop(['Long','Short','url_report', 'type'], axis=1).head(dates.index(start)+1).style.background_gradient(axis=0, cmap=cm)
    st.markdown(f"<h1 style='text-align: center'>{option}</h1>", unsafe_allow_html=True)
    st.table(df)

with col2:
    option = st.selectbox(
    'Second actif ?', choices_asset
     )
    index = choices_asset.index(option)
    #Lis le fichier CSV en fonction de l'actif sélectionné
    df = csv_to_dataframe(f"csv_folder/{ALL_ASSET[index][3]}/{option.lower()}.csv",'Date')
    df = df.drop(['Long','Short','url_report', 'type'], axis=1).head(dates.index(start)+1).style.background_gradient(axis=0, cmap=cm)
    st.markdown(f"<h1 style='text-align: center'>{option}</h1>", unsafe_allow_html=True)
    st.table(df)

    

    #csv = convert_df(df)
    #date = df.index[0].replace("/","-")
    #st.download_button(
    #    label="Exporter le CSV",
    #    data=csv,
    #    file_name=f'{option}_{date}.csv',
    #    mime='text/csv',
    #)