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


class Classification:
    def __init__(self):
        self.name = None
        self.number = None
        self.division = None
        self.div_abbv = None
        self.letter = None
        self.current = None
        self.high = None
        self.high_date = None


class Classifier:
    def __init__(self,
                 code: str = None
                 ):
        self.code = code
        self.title = None
        self.times = None

        def _title(classifier_code):
            try:
                (cursor, conn) = filehandler.open_database(scsa_database)
            except FileNotFoundError:
                raise FileNotFoundError
            except sqlite3.InterfaceError:
                raise FileNotFoundError

            cursor = conn.cursor()
            sql = '''SELECT DISTINCT stage FROM peaktime_classification
                         WHERE stage_id=?'''
            cursor.execute(sql, (classifier_code,))

            try:
                self.title = cursor.fetchall()[0][0]
            except:
                filehandler.close_database(cursor, conn)
                raise IndexError('DATABASE: Read error.')
            else:
                filehandler.close_database(cursor, conn)

        def _peaktime(classifier_code):
            try:
                (cursor, conn) = filehandler.open_database(scsa_database)
            except FileNotFoundError:
                raise FileNotFoundError
            except sqlite3.InterfaceError:
                raise FileNotFoundError

            cursor = conn.cursor()
            sql = '''SELECT division, time FROM peaktime_classification
                         WHERE stage_id=?'''
            cursor.execute(sql, (classifier_code,))

            try:
                data = cursor.fetchall()
            except:
                filehandler.close_database(cursor, conn)
                raise IndexError('DATABASE: Read error.')
            else:
                filehandler.close_database(cursor, conn)

            times = list()
            for div in scsa_divisions:
                for line in data:
                    if line[0] == div['short']:
                        times.append({
                            'div_abv': line[0],
                            'time': line[1]
                        })
                        break
            self.times = times

        if code is not None:
            _title(code)
            _peaktime(code)


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


def member_classification(member_number='L1834', name=None):
    url = "https://scsa.org/classification/" + str(member_number)
    soup = BeautifulSoup(requests.get(url, headers=HEADER, verify=False).content, features='lxml')

    table = soup.find('table', attrs={'class': 'table mb-0', 'id': 'classificationsTable'})
    current_classification = True
    try:
        rows = table.find_all('tr')
    except AttributeError:
        current_classification = False
        print('No Current Classification for', member_number)

    if current_classification is True:
        class_list = list()
        for i in range(1, len(rows)):
            row = rows[i].get_text().split('\n')
            scsa_class = Classification()
            scsa_class.name = name
            scsa_class.number = member_number
            scsa_class.division = row[1]
            scsa_class.div_abbv = row[2]
            scsa_class.letter = row[3]
            scsa_class.current = row[4]
            scsa_class.high = row[5]
            scsa_class.high_date = row[6]
            class_list.append(scsa_class)
        return class_list


def update_classification_records(start_date, end_date, file=scsa_database):
    start_unix = filehandler.Date(start_date).unix
    end_unix = filehandler.Date(end_date).unix

    try:
        (cursor, conn) = filehandler.open_database(file)
    except FileNotFoundError:
        raise FileNotFoundError
    except sqlite3.InterfaceError:
        raise FileNotFoundError

    sql = '''SELECT DISTINCT name,member,division FROM match_scores
             WHERE date_unix BETWEEN ? AND ?'''
    cursor.execute(sql, (start_unix, end_unix))

    try:
        data = cursor.fetchall()
    except:
        filehandler.close_database(cursor, conn)
        raise IndexError('DATABASE: Read error.')
    else:
        filehandler.close_database(cursor, conn)

    classification_list = list()
    for competitor in data:
        try:
            check_division(competitor[2])
        except ValueError:
            pass
        else:
            if competitor[1] != '':
                comp = member_classification(name=competitor[0], member_number=competitor[1])
                if comp is not None:
                    # classification_list = classification_list + comp
                    write_classification(comp, file=file)
    # write_classification(classification_list, file=file)


def write_classification(data, file=scsa_database):
    try:
        (cursor, conn) = filehandler.open_database(file)
    except FileNotFoundError:
        raise FileNotFoundError
    except sqlite3.InterfaceError:
        raise FileNotFoundError

    for line in data:
        print(line.name, line.number, line.division, line.div_abbv,
              line.letter, line.current, line.high, line.high_date)
        cursor = conn.cursor()
        sql = '''INSERT INTO classification(name,number,division,div_abbv,class,current,high,high_date)
                 VALUES(?,?,?,?,?,?,?,?)
                 ON CONFLICT(name,number,division) DO UPDATE SET
                    name = EXCLUDED.name,
                    class = EXCLUDED.class,
                    current = EXCLUDED.current,
                    high = EXCLUDED.high,
                    high_date = EXCLUDED.high_date'''
        cursor.execute(sql, [line.number, line.division, line.name, line.div_abbv,
                             line.letter, line.current, line.high, line.high_date])
        conn.commit()
        try:
            cursor.execute(sql, [line.name, line.number, line.division, line.div_abbv,
                                 line.letter, line.current, line.high, line.high_date])
        except sqlite3.OperationalError:
            print(line.name, line.number, line.division, line.div_abbv,
                  line.letter, line.current, line.high, line.high_date)
        else:
            conn.commit()

    filehandler.close_database(cursor, conn)


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


def check_division(name, return_short=False, div_list=scsa_divisions):
    for division in div_list:
        if division['name'].lower() == name.lower():
            if return_short is True:
                return division['short']
            return division['name']
        if division['short'].lower() == name.lower():
            if return_short is True:
                return division['short']
            return division['name']
    raise ValueError(name, 'is not a division.')


def read_classifier_data(code, division, start_date, end_date, file=scsa_database):
    """
    Reads classifier data from the SQL database for a specific division and given data range

    :param code: SCSA stage number
    :type code: str
    :param division: Division
    :type division: str
    :param start_date: Start date MM/DD/YY
    :type start_date: str
    :param end_date: End date MM/DD/YY
    :type end_date: str
    :param file: database file path
    :type file: str
    :return: array of hit factors
    :rtype: np.array
    """

    start_unix = filehandler.Date(start_date).unix
    end_unix = filehandler.Date(end_date).unix

    try:
        (cursor, conn) = filehandler.open_database(file)
    except FileNotFoundError:
        raise FileNotFoundError
    except sqlite3.InterfaceError:
        raise FileNotFoundError

    sql = '''SELECT time FROM match_scores
             WHERE stage=? AND division=? AND date_unix BETWEEN ? AND ?'''
    cursor.execute(sql, (code, check_division(division, return_short=True), start_unix, end_unix))

    try:
        data = cursor.fetchall()
    except:
        filehandler.close_database(cursor, conn)
        raise IndexError('DATABASE: Read error.')
    else:
        filehandler.close_database(cursor, conn)
        return data


def read_classifier_info(code, division, file=scsa_database):
    try:
        (cursor, conn) = filehandler.open_database(file)
    except FileNotFoundError:
        raise FileNotFoundError
    except sqlite3.InterfaceError:
        raise FileNotFoundError

    sql = '''SELECT DISTINCT time, max_time, strings FROM peaktime_classification
             WHERE stage_id=? AND division=?'''
    cursor.execute(sql, (code, check_division(division, return_short=True)))

    try:
        data = cursor.fetchall()
    except:
        filehandler.close_database(cursor, conn)
        raise IndexError('DATABASE: Read error.')
    else:
        filehandler.close_database(cursor, conn)
        data = {'PeakTime': data[0][0], 'MaxTime': data[0][1], 'Strings': data[0][2]}
        return data


def read_classifier_count(start_date, end_date, file=scsa_database):
    """
    Reads list of unique classifiers used between the start and end dates

    :param start_date: Start date MM/DD/YY
    :type start_date: str
    :param end_date: End date MM/DD/YY
    :type end_date: str
    :param file: database file path
    :type file: str
    :return: list of classifiers
    :rtype: list
    """

    start_unix = filehandler.Date(start_date).unix
    end_unix = filehandler.Date(end_date).unix

    try:
        (cursor, conn) = filehandler.open_database(file)
    except FileNotFoundError:
        raise FileNotFoundError
    except sqlite3.InterfaceError:
        raise FileNotFoundError

    sql = '''SELECT DISTINCT date, stage FROM match_scores
             WHERE date_unix BETWEEN ? AND ?'''
    cursor.execute(sql, (start_unix, end_unix))

    try:
        data = cursor.fetchall()
    except:
        filehandler.close_database(cursor, conn)
        raise IndexError('DATABASE: Read error.')
    else:
        filehandler.close_database(cursor, conn)
    return data


def read_match_count(start_date, end_date, file=scsa_database):
    """
    Reads list of unique matches used between the start and end dates

    :param start_date: Start date MM/DD/YY
    :type start_date: str
    :param end_date: End date MM/DD/YY
    :type end_date: str
    :param file: database file path
    :type file: str
    :return: unique match count
    :rtype: int
    """

    start_unix = filehandler.Date(start_date).unix
    end_unix = filehandler.Date(end_date).unix

    try:
        (cursor, conn) = filehandler.open_database(file)
    except FileNotFoundError:
        raise FileNotFoundError
    except sqlite3.InterfaceError:
        raise FileNotFoundError

    sql = '''SELECT COUNT(DISTINCT match_id) FROM match_scores
             WHERE date_unix BETWEEN ? AND ?'''
    cursor.execute(sql, (start_unix, end_unix))

    try:
        data = cursor.fetchall()
    except:
        filehandler.close_database(cursor, conn)
        raise IndexError('DATABASE: Read error.')
    else:
        filehandler.close_database(cursor, conn)
    return data[0][0]


def read_score_count(start_date, end_date, file=scsa_database):
    """
    Reads count of scores between the start and end dates

    :param start_date: Start date MM/DD/YY
    :type start_date: str
    :param end_date: End date MM/DD/YY
    :type end_date: str
    :param file: database file path
    :type file: str
    :return: unique match count
    :rtype: int
    """

    start_unix = filehandler.Date(start_date).unix
    end_unix = filehandler.Date(end_date).unix

    try:
        (cursor, conn) = filehandler.open_database(file)
    except FileNotFoundError:
        raise FileNotFoundError
    except sqlite3.InterfaceError:
        raise FileNotFoundError

    sql = '''SELECT division FROM match_scores
             WHERE date_unix BETWEEN ? AND ?'''
    cursor.execute(sql, (start_unix, end_unix))

    try:
        data = cursor.fetchall()
    except:
        filehandler.close_database(cursor, conn)
        raise IndexError('DATABASE: Read error.')
    else:
        filehandler.close_database(cursor, conn)
    return data


def read_data(code, division, start_date, end_date, file=scsa_database):
    """
    Reads all data from the SQL database for a specific division and given data range

    :param code: SCSA stage number
    :type code: str
    :param division: Division
    :type division: str
    :param start_date: Start date MM/DD/YY
    :type start_date: str
    :param end_date: End date MM/DD/YY
    :type end_date: str
    :param file: database file path
    :type file: str
    :return: array of hit factors
    :rtype: np.array
    """

    start_unix = filehandler.Date(start_date).unix
    end_unix = filehandler.Date(end_date).unix

    try:
        (cursor, conn) = filehandler.open_database(file)
    except FileNotFoundError:
        raise FileNotFoundError
    except sqlite3.InterfaceError:
        raise FileNotFoundError

    sql = '''SELECT stage, time FROM match_scores
             WHERE stage=? AND division=? AND date_unix BETWEEN ? AND ?'''
    cursor.execute(sql, (code, check_division(division), start_unix, end_unix))

    try:
        data = cursor.fetchall()
    except:
        filehandler.close_database(cursor, conn)
        raise IndexError('DATABASE: Read error.')
    else:
        filehandler.close_database(cursor, conn)
    return np.array(data).reshape(len(data))


def read_member_numbers(start_date, end_date, file=scsa_database):
    """
    Reads list of unique member numbers used between the start and end dates

    :param start_date: Start date MM/DD/YY
    :type start_date: str
    :param end_date: End date MM/DD/YY
    :type end_date: str
    :param file: database file path
    :type file: str
    :return: unique match count
    :rtype: list
    """

    start_unix = filehandler.Date(start_date).unix
    end_unix = filehandler.Date(end_date).unix

    try:
        (cursor, conn) = filehandler.open_database(file)
    except FileNotFoundError:
        raise FileNotFoundError
    except sqlite3.InterfaceError:
        raise FileNotFoundError

    sql = '''SELECT DISTINCT member FROM match_scores
             WHERE date_unix BETWEEN ? AND ?'''
    cursor.execute(sql, (start_unix, end_unix))

    try:
        data = cursor.fetchall()
    except:
        filehandler.close_database(cursor, conn)
        raise IndexError('DATABASE: Read error.')
    else:
        filehandler.close_database(cursor, conn)
        members = list()
        for item in data:
            members.append(item[0])
        return members
