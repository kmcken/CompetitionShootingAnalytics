from config import *
from Utilities import filehandler
import requests
from lxml import etree
from io import StringIO
import pandas as pd


class Match:
    def __init__(self, file):
        self.file = file                # file path
        self.id = None                  # Practiscore match ID
        self.date = None                # Date MM/DD/YYYY
        self.date_unix = None           # Date unix
        self.clubcode = None            # Club Code
        self.clubname = None            # Club Name
        self.matchname = None           # Match Name
        self.stages = None              # List of stages
        self.overall = None             # Overall Scores (pd.Dataframe)


class Stage:
    def __init__(self):
        self.number = None              # Stage Number in the match
        self.name = None                # Stage Name
        self.rounds = None              # Minimum Round Count
        self.points = None              # Maximum Points Possible
        self.classifier = None          # Is a classifier (bool)
        self.classifier_number = None   # Classifier Number
        self.scores = None              # List of scores


def data_to_unix(date):
    date = date.split('/')
    date = datetime.datetime(int(date[2]), int(date[0]), int(date[1]))
    return int(time.mktime(date.timetuple()))


def unix_to_date(unix):
    return datetime.datetime.utcfromtimestamp(unix).strftime('%m/%d/%Y')


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
    :type match_id: int
    :param level: If level == 2, then returns level 2+ matches, if level == 3, then level 3 matches only, else all
    :type level: bool
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
        if islevel2(file, level=level) is False or isuspsa(file) is False:
            os.remove(file)
            print(match_id, 'is not a Level II+ match.')
            return
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


def isuspsa(file):
    with open(file, 'r', encoding='utf-8') as f:
        line = [line for line in f if 'E 1,' in line]
    line = line[0].split(",")
    if line[1].isalnum() is True:
        if line[1].isdigit() is True or line[1].isalpha() is True:
            return False
        return True
    return False


def islevel2(file, level=2):
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        if level == 2:
            if "Level II" in line or "Level III" in line:
                return True
        if level == 3:
            if "Level III" in line:
                return True
    return False


def islevel3(file):
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if "Level III" in line:
                return True
        return False


def txt_to_json(file):
    """
    Converts practiscore txt file to json
    """
    match_id = file.split('/')[-1].strip('.txt')
    jfile = root + '/MatchResults/jsonFiles/' + match_id + '.json'
    header = json_header(file=file)
    overall = json_overall(file)
    stages = json_stages(file)
    scores = json_scores(file)

    filehandler.new_json(jfile, header)
    filehandler.add_to_json(jfile, overall)
    filehandler.add_to_json(jfile, stages)
    filehandler.add_to_json(jfile, scores)


def json_header(file):
    """
    JSON: get the $INFO header from practiscore.txt file
    """
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    info_list = list()
    for line in lines:
        items = line.split(" ")
        if items[0] == '$INFO':
            line = line.strip('$INFO ')
            line = line.strip('\n')
            info = line.split(':')
            info_list.append(info)

    def get_info(key, info):
        for element in info:
            if element[0].lower() == key.lower():
                return element[1]

    level = 1
    if get_info('match level', info_list).lstrip() == 'Level II':
        level = 2
    if get_info('match level', info_list).lstrip() == 'Level III':
        level = 3

    data = {
        'version': version,
        'practiscore_id': int(file.split('/')[-1].strip('.txt')),
        'practiscore_version': get_info('PractiScore_Version', info_list),
        'match_name': get_info('match name', info_list),
        'date': get_info('match date', info_list),
        'unix': data_to_unix(get_info('match date', info_list)),
        'club': get_info('club name', info_list),
        'club_code': get_info('club code', info_list),
        'classifiers': int(get_info('classifiers', info_list)),
        'level': level
    }
    return data


def json_overall(file):
    """
    JSON: get the overall results from practiscore.txt file
    """
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    overall_list = list()
    for line in lines:
        items = line.split(" ")
        if items[0] == 'E':
            line = line.strip('E ')
            line = line.strip('\n')
            line = line.split(',')

            try:
                points = float(line[10])
            except:
                points = 0

            overall_list.append({
                'competitor': int(line[0]),
                'uspsa_num': line[1],
                'firstname': line[2],
                'lastname': line[3],
                'disqualify': True if line[4].lower() == 'yes' else False,
                'class': line[8],
                'division': line[9],
                'match_points': points,
                'place': int(line[11]),
                'percent': None,
                'power_factor': line[12],
                'female': True if line[33].lower() == 'yes' else False,
                'age': line[34],
                'law': True if line[35].lower() == 'yes' else False,
                'military': True if line[36].lower() == 'yes' else False
            })

    df = pd.DataFrame(overall_list)
    for score in overall_list:
        pct = None
        if score['division'] == 'Carry Optics':
            try:
                pct = np.round(score['match_points'] /
                               df.loc[df['division'] == 'Carry Optics']['match_points'].max() * 100, 2)
            except:
                pct = 0

        if score['division'] == 'Open':
            try:
                pct = np.round(score['match_points'] /
                               df.loc[df['division'] == 'Open']['match_points'].max() * 100, 2)
            except:
                pct = 0

        if score['division'] == 'Limited':
            try:
                pct = np.round(score['match_points'] /
                               df.loc[df['division'] == 'Limited']['match_points'].max() * 100, 2)
            except:
                pct = 0

        if score['division'] == 'Limited 10':
            try:
                pct = np.round(score['match_points'] /
                               df.loc[df['division'] == 'Limited 10']['match_points'].max() * 100, 2)
            except:
                pct = 0

        if score['division'] == 'PCC':
            try:
                pct = np.round(score['match_points'] /
                               df.loc[df['division'] == 'PCC']['match_points'].max() * 100, 2)
            except:
                pct = 0

        if score['division'] == 'Production':
            try:
                pct = np.round(score['match_points'] /
                               df.loc[df['division'] == 'Production']['match_points'].max() * 100, 2)
            except:
                pct = 0

        if score['division'] == 'Single Stack':
            try:
                pct = np.round(score['match_points'] /
                               df.loc[df['division'] == 'Single Stack']['match_points'].max() * 100, 2)
            except:
                pct = 0

        if score['division'] == 'Revolver':
            try:
                pct = np.round(score['match_points'] /
                               df.loc[df['division'] == 'Revolver']['match_points'].max() * 100, 2)
            except:
                pct = 0

        score.update({'percent': pct})

    return {'overall': overall_list}


def json_stages(file):
    """
    JSON: get the stage info from practiscore.txt file
    """
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    stage_list = list()
    for line in lines:
        items = line.split(" ")
        if items[0] == 'G':
            line = line.strip('G ')
            line = line.strip('\n')
            line = line.split(',')

            stage_list.append({
                'number': int(line[0]),
                'name': line[6],
                'min_rounds': int(line[2]),
                'max_points': int(line[3]),
                'classifer': True if line[4].lower() == 'yes' else False,
                'classifier_number': line[5],
                'scoring': line[7]
            })

    return {'stages': stage_list}


def json_scores(file):
    """
    JSON: get the scores for each stage from practiscore.txt file
    """
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    score_list = list()
    for line in lines:
        items = line.split(" ")
        if items[0] == 'I':
            line = line.strip('I ')
            line = line.strip('\n')
            line = line.split(',')

            score_list.append({
                'stage': int(line[1]),
                'competitor': int(line[2]),
                'disqualify': True if line[3].lower() == 'yes' else False,
                'dnf': True if line[4].lower() == 'yes' else False,
                'A': int(line[5]),
                'B': int(line[6]),
                'C': int(line[7]),
                'D': int(line[8]),
                'M': int(line[9]),
                'NS': int(line[10]),
                'procedurals': int(line[11]),
                'penalties': int(line[19]),
                'time': float(line[25]),
                'total_points': int(line[27]),
                'hitfactor': float(line[28]),
                'stage_points': float(line[29]),
                'stage_place': int(line[30])
            })

    return {'scores': score_list}
