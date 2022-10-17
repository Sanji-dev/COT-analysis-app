from bs4 import BeautifulSoup
import requests
from datetime import date, timedelta
import pandas as pd
from time import sleep
from random import randint
from tqdm import tqdm

# --- GLOBAL --- #
'''
ICE Futures US (USD)         --> https://www.cftc.gov/sites/default/files/files/dea/cotarchives/2022/futures/deanybtsf010521.htm
Chicago Mercantile Exchange  --> https://www.cftc.gov/sites/default/files/files/dea/cotarchives/2022/futures/deacmesf091322.htm
New York Mercantile Exchange --> https://www.cftc.gov/sites/default/files/files/dea/cotarchives/2021/futures/deanymesf010521.htm
Commodity Exchange           --> https://www.cftc.gov/sites/default/files/files/dea/cotarchives/2021/futures/deacmxsf010521.htm
Attention, deux éléments changent dans l'URL en fonction du fichier : L'année (2022) et la date (091322).
'''

#Currencies by report

RUN = False
CHICAGO = [
            ['EUR','Code-099741',[]], #Money , Code, List of COT values
            ['JPY','Code-097741',[]],
            ['AUD','Code-232741',[]],
            ['NZD','Code-112741',[]],
            ['CAD','Code-090741',[]],
            ['GBP','Code-096742',[]],
            ['CHF','Code-092741',[]],
            ['MXN','Code-095741',[]],
            ['BRL','Code-102741',[]],
            ['ZAR','Code-122741',[]],
            ['BTC','Code-133741',[]],
            ['ETH','Code-146021',[]],
            ['NASDAQ-100','Code-209742',[]],
            ['S&P 500','Code-209742',[]],
]

USD = ['USD','Code-098662',[]]

NEW_YORK = [
            ['OIL','Code-067651',[]],
            ['GAS','Code-023651',[]],
]

COMMODITY = [
            ['SILVER','Code-084691',[]],
            ['COPPER','Code-085692',[]],
            ['GOLD','Code-088691',[]],
    
]

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
        #print("{} added".format(url[0].strftime("%d/%m/%y")))
        sleep(randint(1,3))


    for money in major_fx:
        dataframe_to_csv(money[0].lower(), money[2])

def dataframe_to_csv(money, data):
    #Reverse to get latest at the top
    data.reverse()
    df = pd.DataFrame(data)

    #Write Symbols DataFrames in csv 
    df.to_csv(f"csv_folder/{money}.csv", index=False)
    print(f"##-- {money.upper()} --##")
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
        url = "https://www.cftc.gov/sites/default/files/files/dea/cotarchives/20{}/futures/deacmesf{}.htm".format(str(date.strftime("%y")),str(date.strftime("%m%d%y")))
        url_list.append((date,url))

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
            for money in major_fx:
                if money[1] in words:
                    long = int(lines[idx+9].split()[0].replace(",",""))
                    short = int(lines[idx+9].split()[1].replace(",",""))

                    cloture_long = int(lines[idx+12].split()[0].replace(",",""))
                    cloture_short = int(lines[idx+12].split()[1].replace(",",""))

                    
                    net_position = long - short
                    print(net_position)

                    dico = {
                        'Date':new_date,
                        'Long': long,
                        'Short': short,
                        'Change long':cloture_long,
                        'Change short':cloture_short,
                        'Net position': net_position,
                    }
                    
                    money[2].append(dico)

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
        init_csv_files_from_html(date(2021,1,5), 93)
        #create_every_url(date(2021,1,5), 92)
        #parser('cot.html', date(2021,9,6))
        #for m in major_fx:
        #    print(m)

if __name__ == "__main__":
    main()