from bs4 import BeautifulSoup
import requests
from datetime import date, timedelta
import pandas as pd
from time import sleep
from random import randint
from tqdm import tqdm

# --- GLOBAL --- #
'''
ICE Futures US (USD)         --> https://www.cftc.gov/sites/default/files/files/dea/cotarchives/2021/futures/deanybtsf010521.htm
Chicago Board (DowJones)     --> https://www.cftc.gov/sites/default/files/files/dea/cotarchives/2022/futures/deacbtsf010422.htm
Chicago Mercantile Exchange  --> https://www.cftc.gov/sites/default/files/files/dea/cotarchives/2022/futures/deacmesf091322.htm
New York Mercantile Exchange --> https://www.cftc.gov/sites/default/files/files/dea/cotarchives/2021/futures/deanymesf010521.htm
Commodity Exchange           --> https://www.cftc.gov/sites/default/files/files/dea/cotarchives/2021/futures/deacmxsf010521.htm
Attention, deux éléments changent dans l'URL en fonction du fichier : L'année (2022) et la date (091322).
'''

#Currencies by report

RUN = True
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

print(ALL_ASSET)
# --- FUNCTIONS --- #

def init_csv_files_from_html(start_date, weeks_numbers):
    '''     Populate csv files with commitment of traders datas after requesting cftc.gov website

    Args:   start_date (date):  first date to request
            weeks_numbers(int): weeks numbers to incremente from start_date

    Return: (int):    status code
    '''
    
    #Generate and get every url to request
    url_set = create_every_url(start_date, weeks_numbers)

    #Request every url (every tuesday)
    for url in tqdm(url_set):
        parser(url[1],url[0]) #parser(https://.... , 2022-xx-xx)
        
        sleep(randint(1,3))


    for asset in ALL_ASSET:
        dataframe_to_csv(asset[0].lower(), asset[4], asset[3])

def dataframe_to_csv(asset, data, outdir):
    #Reverse to get newest to oldest
    data.reverse()
    df = pd.DataFrame(data)
    import os
    #Write Symbols DataFrames in csv
    
    if not os.path.exists(os.path.join(os.getcwd(),'csv_folder',outdir)):
        os.mkdir(os.path.join(os.getcwd(),'csv_folder',outdir))
    df.to_csv(f"csv_folder\\{outdir}\\{asset}.csv", index=False)
    print(f"##-- {asset.upper()} --##")
    print(df,"\n")
    

def create_every_url(start_date, weeks_numbers):
    ''' Generate every url for each date (tuesday) based on url param

    Args:   start_date (date):  first date to request
            weeks_numbers(int): weeks numbers to incremente from start_date

    Return: (list): List of url for each date
    '''

    date = start_date
    url_list = list()
    for i in range(weeks_numbers):
        url_chicago = "https://www.cftc.gov/sites/default/files/files/dea/cotarchives/20{}/futures/deacmesf{}.htm".format(str(date.strftime("%y")),str(date.strftime("%m%d%y")))
        url_list.append((date,url_chicago))
        
        url_dj = "https://www.cftc.gov/sites/default/files/files/dea/cotarchives/20{}/futures/deacbtsf{}.htm".format(str(date.strftime("%y")),str(date.strftime("%m%d%y")))
        url_list.append((date,url_dj))

        url_ny = "https://www.cftc.gov/sites/default/files/files/dea/cotarchives/20{}/futures/deanymesf{}.htm".format(str(date.strftime("%y")),str(date.strftime("%m%d%y")))
        url_list.append((date,url_ny))

        url_usd = "https://www.cftc.gov/sites/default/files/files/dea/cotarchives/20{}/futures/deanybtsf{}.htm".format(str(date.strftime("%y")),str(date.strftime("%m%d%y")))
        url_list.append((date,url_usd))

        url_commodity = "https://www.cftc.gov/sites/default/files/files/dea/cotarchives/20{}/futures/deacmxsf{}.htm".format(str(date.strftime("%y")),str(date.strftime("%m%d%y"))) 
        url_list.append((date,url_commodity))

        #Date incrementation by 7 days (each tuesday)
        date = date + timedelta(days=7)
    
    return(url_list)

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



def main():
    if RUN:
        init_csv_files_from_html(date(2022,1,4), 62)
        #create_every_url(date(2021,1,5), 92)
        #parser('cot.html', date(2021,9,6))
        #for m in major_fx:
        #    print(m)
        

    #Update local, change 2nd is week number after 01-04-2022
    #Help with https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalViewable/index.htm
    #for url in create_every_url(date(2022,1,4), 62):
    #  print(url)
    
if __name__ == "__main__":
    main()