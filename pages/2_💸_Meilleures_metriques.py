import streamlit as st
import pandas as pd

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
    list_rank_short.sort(reverse=True)
    
    if last_change >= 0:
        for idx, item in enumerate(list_rank_long):
            if item[1] == 0:   #On récupère dans la liste triée le dernier rapport (indice 0)
                rank = idx+1
                return rank, last_change, list_rank_long

    elif last_change < 0:
        for idx, item in enumerate(list_rank_short):
            if item[1] == 0:   #On récupère dans la liste triée le dernier rapport (indice 0)
                rank = idx+1
                return rank, last_change, list_rank_short
    


#def get_evolution_net_total(asset, since=1):
#    new_net_position = asset.loc[0]['Net position']
#    old_net_position = asset.loc[since]['Net position']
#    evolution = (new_net_position - old_net_position)/old_net_position * 100
#
#    return evolution

def main():
    st.title("En cours de développement")

    list_evolution = list()
    for asset in ALL_ASSET[0:1]:
        outdir = asset[3]
        file_name = asset[0].lower()
        df = csv_to_dataframe(f"csv_folder/{outdir}/{file_name}.csv",index=None)
        rank, value, list_rank = ranking(df)

        st.header(asset[0])
        st.markdown(f'Rank: **{rank}** Value: {value}')
        new_df = pd.DataFrame(list_rank, columns=['Diff','Index','Date'])
        new_df
    
    
    #df_total = pd.DataFrame(list_evolution, columns=['Asset','Evolution']).sort_values('Evolution')
    #st.dataframe(rank_long)
    #st.dataframe(rank_short)


    #url ='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0101EN-SkillsNetwork/labs/Module%205/data/addresses.csv'
    #df = pd.read_csv(url)
    #df.columns =['First Name', 'Last Name', 'Location ', 'City','State','Area Code']
    #st.dataframe(df)
#
    #st.markdown(type(df))
    

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