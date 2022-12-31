from config import *
from Utilities import filehandler
from six.moves.urllib.request import Request, urlopen
from bs4 import BeautifulSoup


def classification(division='Open', member='L3137'):
    url = "https://uspsa.org/classification/" + member
    soup = BeautifulSoup(requests.get(url, headers=HEADER, proxies=PROXY, verify=False).content, features='lxml')
    table = soup.find('table', attrs={'class': 'table table-striped table-responsive'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')

    cols = list()
    for row in rows:
        if row.find('th').text.strip() == division:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]

    cols[0] = cols[0].split(": ")[1]
    try:
        cols[1] = float(cols[1].split(": ")[1])
    except:
        cols[1] = 0
    try:
        cols[2] = float(cols[2].split(": ")[1])
    except:
        cols[2] = 0
    cols.insert(0, division)
    return cols

