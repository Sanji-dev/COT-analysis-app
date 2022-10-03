from bs4 import BeautifulSoup
import requests
from datetime import date, timedelta
import pandas as pd




# --- GLOBAL --- #
'''
URL USD   --> https://www.cftc.gov/sites/default/files/files/dea/cotarchives/2022/futures/deanybtsf010521.htm
URL OTHER --> https://www.cftc.gov/sites/default/files/files/dea/cotarchives/2022/futures/deacmesf091322.htm
Attention, deux éléments changent dans l'URL en fonction du fichier : L'année (2022) et la date (091322).
'''


OTHER_ID = [('EUR','Code-099741'),
            ('JPY','Code-097741'),
            ('AUD','Code-232741'),
            ('NZD','Code-112741'),
            ('CAD','Code-090741'),
            ('GBP','Code-096742'),
            ('CHF','Code-092741'),
            ]
USD_ID = ('USD','Code-098662')

# ------ #

def init_get_html_page(start_date, weeks_numbers):
    '''     Populate csv files with commitment of traders datas after requesting cftc.gov website

    Args:   start_date (date):  first date to request
            weeks_numbers(int): weeks numbers to incremente from start_date

    Return: (int):    status code
    '''
    
    url_set = create_every_url(start_date, weeks_numbers)
    for url in url_set:
        #parser(url,)
        print(url[0], url[1])

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

        date = date + timedelta(days=7)
        

    return url_list

def parser(file,date):
    ''' Parse html file

    '''
    new_date  = date.strftime("%d/%m/%y")
    print(new_date)
    with open(file) as f:
        soup = BeautifulSoup(f,"html.parser")
        body = soup.body.get_text()

        lines = body.splitlines()
        for idx, item in enumerate(lines):
            words = item.split()
            for money in OTHER_ID:
                if money[1] in words:
                    long = lines[idx+9].split()[0]
                    short = lines[idx+9].split()[1]

                    cloture_long = lines[idx+12].split()[0]
                    cloture_short = lines[idx+12].split()[1]

                    long_formatted = int(long.replace(",",""))
                    short_formatted = int(short.replace(",",""))
                    net_position = "{:,}".format(long_formatted - short_formatted)

                    dico = {
                        'Date':new_date,
                        'Long': long,
                        'Short': short,
                        'Cloture long':cloture_long,
                        'Cloture short':cloture_short,
                        'Net position': net_position,
                    }
                    
                    write_csv(money[0]+".csv", dico)

def write_csv(name, data):
    print(name.lower(), data)

def main():
    init_get_html_page(date(2021,1,5), 90)
    #parser('cot.html', date(2021,9,6))



if __name__ == "__main__":
    main()