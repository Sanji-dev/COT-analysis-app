import streamlit as st
import pandas as pd
from millify import millify

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



def ranking(asset):
    list_change = list()
    list_rank_long = list()
    list_rank_short = list()
    last_change = 0

    for row in asset.index:
        change_long = asset['Change long'][row]
        change_short = asset['Change short'][row]
        total_long, total_short = 0,0

        if change_long >= 0:
            total_long += change_long
        else:
            total_short += change_long
        
        if change_short >= 0:
            total_short -= change_short
        else:
            total_long += abs(change_short)

        diff = total_long + total_short

        if row == 0:
            last_change = diff

        if diff >= 0:
            list_rank_long.append((diff,row,asset['Date'][row]))
        else:
            list_rank_short.append((diff,row,asset['Date'][row]))
    
    list_rank_long.sort(reverse=True)
    list_rank_short.sort()
    
    if last_change >= 0:
        for idx, item in enumerate(list_rank_long):
            if item[1] == 0:   #On récupère dans la liste triée le dernier rapport (indice 0)
                rank = idx+1
                return rank, last_change

    elif last_change < 0:
        for idx, item in enumerate(list_rank_short):
            if item[1] == 0:   #On récupère dans la liste triée le dernier rapport (indice 0)
                rank = idx+1
                return rank, last_change
    
def get_longest_length(list1, list2):
    if len(list1) - len(list2) >= 0:
        return len(list1)
    else:
        return len(list2)

def try_display_metric_long(i, df_long):
    ''' Display metric for a long value if it does exists

    Args:   i(int): index in dataframe
            df_long(dataframe): dataframe of assets in long direction
    
    '''
    try:
        st.metric(label=f'Rang {i+1}', value=df_long['Asset'][i], delta = millify(int(df_long['Value'][i])))
    except KeyError as e:
        pass

def try_display_metric_short(i, df_short):
    ''' Display metric for a short value if it does exists

    Args:   i(int): index in dataframe
            df_long(dataframe): dataframe of assets in short direction
    
    '''
    try:
        st.metric(label=f'Rang {i+1}', value=df_short['Asset'][i], delta = millify(int(df_short['Value'][i])))
    except KeyError as e:
        pass

def main():
    st.header("Plus grosses injections d'ordres des derniers rapports COT")
    st.markdown(
            """
            Un algorithme permet d'identifier puis de classer les actifs qui ont reçu les plus grosses injections de positions, selon les derniers rapports "Commitments of traders" publiés le vendredi le plus récent.
        """ 
        )
    with st.expander("Voir explications"):
        st.markdown(
            """
            ##### Etape 1 : Premier tri effectué sur chaque actif.
            Pour un actif donné:
            1. Récupère le **volume de position long** du dernier rapport en date. (Injection de long + clotûre de short).
            2. Récupère le **volume de position short** du dernier rapport en date. (Injection de short + clotûre de long).
            3. On fait la différence entre le volume de long et de short pour identifier l'orderflow.
            4. On refait les mêmes opérations avec tous les autres rapports précédents. ( échantillon de données sur quasi 1 an, depuis le 4 Janvier 2022)
            5. On classe tous les volumes de positions long d'une part, et les volumes de positions short d'autre part. **Du plus grand au plus petit**.
            6. Avec ce classement, on peut comparer le dernier volume de position injecté dans l'actif avec tous les autres volumes précédemment injectés.
            7. De cette manière, plus la position du dernier volume de position injecté est importante dans le classement, plus l'actif est susceptible de nous intéresser car fort orderflow.
            8. (Exemple: Si le dernier volume de position injecté est classé 1er du classement, alors on en conclu que c'est la plus grosse injection d'ordre de l'année sur cet actif )

            ##### Etape 2 : Nouveau tri
            Enfin, on effectue un nouveau classement composé du rang des derniers volumes injectés de chaque actif (grâce à l'étape 1)
            Ce classement est observable ci-dessous sous forme de métrique.
        """ 
        )

    final_ranking_long = list()
    final_ranking_short = list()

    for asset in ALL_ASSET:
        outdir = asset[3]
        file_name = asset[0].lower()
        df = csv_to_dataframe(f"csv_folder/{outdir}/{file_name}.csv",index=None)
        
        rank, value = ranking(df)
        if value >= 0:
            final_ranking_long.append((asset[0], rank, value))
        else:
            final_ranking_short.append((asset[0], rank, value))


    final_ranking_long.sort(key=lambda x: x[1])
    df_long = pd.DataFrame(final_ranking_long, columns=['Asset','Rank','Value'])

    final_ranking_short.sort(key=lambda x: x[1])
    df_short = pd.DataFrame(final_ranking_short, columns=['Asset','Rank','Value'])

    col1, col2= st.columns(2)
    with col1:
        st.subheader("Classement positions long ↗️")
    with col2:
        st.subheader('Classement positions short ↘️')

    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    length = get_longest_length(df_long, df_short)
    for i in range(length):
        if i%3 == 0:
            with col1:
                try_display_metric_long(i,df_long)
            with col5:
                try_display_metric_short(i,df_short)
        if i%3 == 1:
            with col2:
                try_display_metric_long(i,df_long)
            with col6:
                try_display_metric_short(i,df_short)
        if i%3 == 2:
            with col3:
                try_display_metric_long(i,df_long)
            with col7:
                try_display_metric_short(i,df_short)
        
        
    #col1, col2 = st.columns(2)
    #with col1:
    #    final_ranking_long.sort(key=lambda x: x[1])
    #    df = pd.DataFrame(final_ranking_long, columns=['Asset','Rank','Value'])
    #    df
    #with col2:
    #    final_ranking_short.sort(key=lambda x: x[1])
    #    df = pd.DataFrame(final_ranking_short, columns=['Asset','Rank','Value'])
    #    df

@st.experimental_memo
def csv_to_dataframe(file, index="Date"):
    return pd.read_csv(file, index_col=index)

if __name__ == "__main__":
    st.set_page_config(
        page_title="Meilleures_metriques",
        page_icon="💸",
        layout="wide",
    )
    main()