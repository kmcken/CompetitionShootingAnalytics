from config import *
from Utilities import filehandler
import requests
from lxml import etree
from io import StringIO


def download_all(start_id=156251, end_id=181678, level=2):
    """
    Downloads match results from practiscore for given match id range
    :param start_id:
    :param end_id:
    :param level: match level (2=2+; 3=3only)
    """
    for match in range(start_id, end_id + 1):
        download_match(match, level=level)


def download_match(match_id, level=2):
    """
    Downloads Match Results .txt file for given match id. Labeled match_id.txt
    :param match_id: Practiscore match ID
    :type match_id: str
    :param level2: If level2 is True, then it only saves Level2+ matches
    :type level2: bool
    """
    file = root + '/MatchResults/' + str(match_id) + '.txt'

    if os.path.isfile(file) is True:
        print(match_id, 'is already downloaded.')
        return

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    url = 'https://practiscore.com/results/new/' + str(match_id)
    page = requests.get(url, headers=headers)

    try:
        url = webreport(page)
    except:
        print(match_id, 'is not a USPSA match.')
        return
    page = requests.get(url, headers=headers)
    with open(file, 'wb') as f:
        for chunk in page.iter_content(chunk_size=8192):
            f.write(chunk)
    if level is not None:
        if filehandler.islevel2(file, level=level) is False:
            os.remove(file)
            print(match_id, 'is not a Level II+ match.')
        else:
            print(match_id, 'is a Level II+ match.')


def webreport(page):
    """
    Returns the URL for the Web Report
    :param page: requests.get page
    :return: url
    :rtype: str
    """
    parser = etree.HTMLParser()
    html = page.content.decode('utf-8')
    tree = etree.parse(StringIO(html), parser=parser)
    refs = tree.xpath("//a")
    links = [link.get('href', 'Web Report') for link in refs]
    return [l for l in links if l.startswith('https://practiscore.com/reports/web')][0]
