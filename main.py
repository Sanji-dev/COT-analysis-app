from bs4 import BeautifulSoup
import requests
from datetime import date, timedelta
import pandas as pd




# --- GLOBAL --- #
"""
URL USD   --> https://www.cftc.gov/sites/default/files/files/dea/cotarchives/2022/futures/deanybtsf010521.htm
URL OTHER --> https://www.cftc.gov/sites/default/files/files/dea/cotarchives/2022/futures/deacmesf091322.htm
Attention, deux éléments changent dans l'URL en fonction du fichier : L'année (2022) et la date (091322).
Par conséquent, l'URL est traitée en 4 parties.
"""

# url for all forex money except USD
START_URL_OTHER, END_URL_OTHER = "https://www.cftc.gov/sites/default/files/files/dea/cotarchives/20", "/futures/deacmesf"

# url for USD
START_URL_USD, END_URL_USD = "https://www.cftc.gov/sites/default/files/files/dea/cotarchives/20", "/futures/deanybtsf"

# ID by money
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

def init_get_html_page(url, start_date, weeks_numbers):
    create_every_url(url, start_date, weeks_numbers)


def create_every_url(url, start_date, weeks_numbers):
    date = start_date
    for i in range(weeks_numbers):

        specific_url = url + str(date.strftime("%m%d%y")) + ".htm"
        print(specific_url)
        date = date + timedelta(days=7)

def parser(file,date):
    new_date  = date.strftime("%d/%m/%y")
    print(d)
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

                    net_position = long - short
                    
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
    #init_get_html_page(URL, date(2021,1,5), 90)
    parser('cot.html', date(2021,9,6))



if __name__ == "__main__":
    main()