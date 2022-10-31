import streamlit as st
import pandas as pd
from datetime import date
import seaborn as sns
from datetime import date, timedelta, datetime
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import requests
import os

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

def main():
    st.header("Tableaux de données par actifs")
    
    df = csv_to_dataframe("csv_folder/forex/usd.csv")
    dates = list(df.index)

    #Check for new COT report
    check_last_row(dates[0])
    
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

        #Convert dataframe to csv for download button
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
            key='button1',
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
            key='button2',
        )

def update_csv(tuesday_date):
    year = str(tuesday_date.strftime("%y"))
    day = str(tuesday_date.strftime("%m%d%y"))
    url_list = list()

    url_chicago =   f"https://www.cftc.gov/sites/default/files/files/dea/cotarchives/20{year}/futures/deacmesf{day}.htm"
    url_list.append(url_chicago)

    url_dj =        f"https://www.cftc.gov/sites/default/files/files/dea/cotarchives/20{year}/futures/deacbtsf{day}.htm"
    url_list.append(url_dj)

    url_ny =        f"https://www.cftc.gov/sites/default/files/files/dea/cotarchives/20{year}/futures/deanymesf{day}.htm"
    url_list.append(url_ny)

    url_usd =       f"https://www.cftc.gov/sites/default/files/files/dea/cotarchives/20{year}/futures/deanybtsf{day}.htm"
    url_list.append(url_usd)

    url_commodity = f"https://www.cftc.gov/sites/default/files/files/dea/cotarchives/20{year}/futures/deacmxsf{day}.htm"
    url_list.append(url_commodity)
    print(url_list)
    for url in url_list:
        sleep(randint(1, 3))
        parser(url, tuesday_date)

    for asset in ALL_ASSET:
        dataframe_to_csv(asset[0].lower(), asset[4], asset[3])
    st.experimental_memo.clear()

def dataframe_to_csv(asset, data, outdir):
    old_df = csv_to_dataframe(f"csv_folder/{outdir}/{asset}.csv", index=False)
    new_df = pd.concat([pd.DataFrame(data),old_df],ignore_index=True)
        
    #Update with new report in CSV files
    
    new_df.to_csv(f"csv_folder/{outdir}/{asset}.csv", index=False)
    print(f"##-- {asset.upper()} --##")
    print(new_df.head(),"\n")

def parser(url,date):
    ''' Parse html file from specific URL after requesting it.

    Args:   url(string): Url to request to
            date(date): the date we want to get COT datas from
    
    Return: (int): Status code
    '''

    new_date  = date.strftime("%d/%m/%y")
    html_response = get_request_url(url)

    #If html response is not None
    if html_response:
        soup = BeautifulSoup(html_response,"html.parser")
        body = soup.body.get_text()

        lines = body.splitlines()
        for idx, item in enumerate(lines):
            words = item.split()
            for asset in ALL_ASSET:
                if asset[1] in words:
                    long = int(lines[idx+9].split()[0].replace(",",""))
                    short = int(lines[idx+9].split()[1].replace(",",""))

                    cloture_long = int(lines[idx+12].split()[0].replace(",",""))
                    cloture_short = int(lines[idx+12].split()[1].replace(",",""))

                    
                    net_position = long - short

                    dico = {
                        'Date':new_date,
                        'Long': long,
                        'Short': short,
                        'Change long':cloture_long,
                        'Change short':cloture_short,
                        'Net position': net_position,
                        'url_report':asset[2],
                        'type': asset[3],
                    }
                    
                    asset[4].append(dico)

def get_request_url(url):
    try:
        html_response = requests.get(url)
        if html_response.status_code == 200:
            return html_response.content
        return None
    except requests.exceptions.RequestException as e: 
        print(f'save failed: unable to get page content: {e}')
        return None

def check_last_row(last_date):
    str_to_date = datetime.strptime(last_date,'%d/%m/%y').date()
    today = date.today()
    delta = today - str_to_date
    if delta > timedelta(days=10):
        update_csv(str_to_date+ timedelta(days=7))

@st.experimental_memo
def csv_to_dataframe(file, index="Date"):
    return pd.read_csv(file, index_col=index)


def customize_dataframe(df,start):
    cm = sns.blend_palette(['red','white','green'], as_cmap=True, n_colors=4)

    df_customized = (
        df.drop(['Long','Short','url_report', 'type'], axis=1)
        .head(start)
        .style.background_gradient(subset=['Net position'],axis=0, cmap=cm)
        .bar(height=70,color=['red','green'],align='zero',subset=['Change long', 'Change short'])
    )
    return df_customized

def convert_df(df):
    return df.to_csv().encode('utf-8')

if __name__ == "__main__":
    st.set_page_config(
        page_title="Comparateur d'actifs",
        page_icon="⚖️",
        layout="wide",
    )
    main()