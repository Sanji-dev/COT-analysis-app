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

DJ = [['DOW JONES','Code-124603','deacbtsf','index',[]]]

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

ALL_ASSET = CHICAGO + DJ + USD + NEW_YORK + COMMODITY



@st.cache
def csv_to_dataframe(file, index="Date"):
    return pd.read_csv(file, index_col=index)

@st.cache(allow_output_mutation=True)
def customize_dataframe(df,start):
    cm = sns.blend_palette(['red','white','green'], as_cmap=True, n_colors=4)

    df_customized = (
        df.drop(['Long','Short','url_report', 'type'], axis=1)
        .head(start)
        .style.background_gradient(subset=['Net position'],axis=0, cmap=cm)
        .bar(height=70,color=['red','green'],align='zero',subset=['Change long', 'Change short'])
    )
    return df_customized

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

@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

def main():
    st.header("Tableaux de données par actifs")
    
    df = csv_to_dataframe("csv_folder/forex/usd.csv")
    dates = list(df.index)

    #Input slider pour filter la date range
    start = st.select_slider("Sélectionner la date de début", options = dates, value=("19/07/22"))

    #Récupère l'index de l'USD dans la liste pour l'afficher par défaut dans la selectbox
    choices_asset = [item[0] for item in ALL_ASSET]
    st.caption("Etude sur **{}** semaines".format(dates.index(start)+1))
    col1, col2 = st.columns(2)
    cm = sns.blend_palette(['red','white','green'], as_cmap=True, n_colors=4)

    with col1:
        option = st.selectbox(
            'Premier actif ?', choices_asset, index=0 #EUR default
        )
        #Lis le fichier CSV en fonction de l'actif sélectionné
        index = choices_asset.index(option)
        df = csv_to_dataframe(f"csv_folder/{ALL_ASSET[index][3]}/{option.lower()}.csv",'Date')
        #Convert to df to csv for download button
        csv = convert_df(df)

        df = customize_dataframe(df,dates.index(start)+1)
        st.markdown(f"<h1 style='text-align: center'>{option}</h1>", unsafe_allow_html=True)
        st.table(df)
        
        #Download button
        date = df.index[0].replace("/","-")
        st.download_button(
            label="Exporter le CSV",
            data=csv,
            file_name=f'{option}_{date}.csv',
            mime='text/csv',
        )
    with col2:
        option = st.selectbox(
        'Second actif ?', choices_asset, index = 15 #USD default
        )
        #Lis le fichier CSV en fonction de l'actif sélectionné
        index = choices_asset.index(option)
        df = csv_to_dataframe(f"csv_folder/{ALL_ASSET[index][3]}/{option.lower()}.csv",'Date')
        #Convert to df to csv for download button
        csv = convert_df(df)

        df = customize_dataframe(df,dates.index(start)+1)
        st.markdown(f"<h1 style='text-align: center'>{option}</h1>", unsafe_allow_html=True)
        st.table(df)
       
        #Download button
        date = df.index[0].replace("/","-")
        st.download_button(
            label="Exporter le CSV",
            data=csv,
            file_name=f'{option}_{date}.csv',
            mime='text/csv',
        )
if __name__ == "__main__":
    st.set_page_config(
        page_title="Comparateur d'actifs",
        page_icon="⚖️",
        layout="wide",
    )
    main()