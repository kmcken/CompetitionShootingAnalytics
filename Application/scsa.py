from config import *
from Utilities import filehandler
from bs4 import BeautifulSoup


class Score:
    def __init__(self):
        self.match_id = None
        self.event = None
        self.level = 1
        self.club = None
        self.date = None
        self.upload_date = None
        self.name = None
        self.member = None
        self.division = None
        self.classifier = None
        self.time = None


def match_results(match_id=1):
    url = "https://scsa.org/results/match/" + str(match_id)
    soup = BeautifulSoup(requests.get(url, headers=HEADER, verify=False).content, features='lxml')

    valid_match = False
    try:
        soup.find('div', attrs={'class': 'alert alert-danger'}).get_text()
    except AttributeError:
        valid_match = True
        print('Match ID', match_id)
    else:
        print('Match ID', match_id, 'is an invalid match')

    try:
        soup.find('h6', attrs={'class': 'm-4'}).get_text()
    except:
        pass
    else:
        valid_match = False

    if valid_match is True:
        # Get Match Info
        event = soup.find('div', attrs={'class': 'card-body'}).get_text().split('\n')
        event_name = event[2]
        try:
            event_level = int(event[4])
        except ValueError:
            event_level = 1

        club = event[6]
        if event[8] == '0/00/00':
            event_date = event[12]
        else:
            event_date = event[8]
        upload_date = event[12]

        # Get Classifier/Stage Info
        table = soup.find('table', attrs={'class': 'table m-0 table-custom'})
        rows = table.find_all('tr')
        classifier_stages = list()
        for i in range(1, len(rows)):
            row = rows[i].get_text().split('\n')
            if row[2] != '':
                classifier_stages.append([row[1], row[2]])

        # Get Scores
        table = soup.find('table', attrs={'class': 'table table-custom table-bordered'})
        rows = table.find_all('tr')

        scores = list()
        for i in range(1, len(rows)):
            row = rows[i].get_text().split('\n')
            if 'DQ' not in row:
                for stage in classifier_stages:
                    score = Score()
                    score.match_id = match_id
                    score.event = event_name
                    score.level = event_level
                    score.club = club
                    score.date = event_date
                    score.upload_date = upload_date
                    score.name = row[3].rstrip().lstrip()
                    if row[7].rstrip().lstrip() != '0':
                        score.member = row[7].rstrip().lstrip()
                    score.division = row[9]
                    score.classifier = stage[1]
                    try:
                        score.time = float(row[12 + int(stage[0])])
                    except:
                        pass
                    scores.append(score)
        return scores


def download_score(start_id=1, end_id=10000, file=scsa_database):
    for i in range(start_id, end_id):
        scores = match_results(i)
        if scores:
            write_match_result(scores, file)


def write_match_result(scores, file=scsa_database):
    try:
        (cursor, conn) = filehandler.open_database(file)
    except FileNotFoundError:
        raise FileNotFoundError
    except sqlite3.InterfaceError:
        raise FileNotFoundError

    for score in scores:
        cursor = conn.cursor()
        sql = '''INSERT INTO match_scores(match_id,event,level,date,date_unix,date_upload,name,member,division,stage,time)
                 VALUES(?,?,?,?,?,?,?,?,?,?,?)'''
        cursor.execute(sql, [score.match_id, score.event, score.level, score.date, filehandler.Date(score.date).unix,
                             score.upload_date, score.name, score.member, score.division, score.classifier, score.time])
        conn.commit()

    filehandler.close_database(cursor, conn)
