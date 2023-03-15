from config import *
from Utilities import filehandler
from six.moves.urllib.request import Request, urlopen
from bs4 import BeautifulSoup


class Classifier:
    def __init__(self, code=None, title=None, hhfs=False, file=classifier_list_file, hhf_file=classifier_hhf_file):
        self.code = code
        self.title = title
        self.hhfs = None

        def _title(classifier_code):
            df = pd.read_csv(file)
            try:
                self.title = df.loc[df.code == classifier_code].title.item()
            except ValueError:
                raise ValueError(str(classifier_code), 'is not in the classifier list.') from None
            else:
                self.code = classifier_code

        def _code(classifier_title):
            df = pd.read_csv(file)
            try:
                self.code = df.loc[df.title == classifier_title].code.item()
            except ValueError:
                raise ValueError(str(classifier_title), 'is not in the classifier list.') from None
            else:
                self.title = classifier_title

        def _hhfs(hhf_file):
            df = pd.read_csv(hhf_file)
            self.hhfs = df.loc[df.code == self.code]

        if code is not None:
            _title(self.code)

        if title is not None:
            _code(self.title)

        if hhfs is True:
            _hhfs(hhf_file)

    def hhf(self, division):
        if self.hhfs is None:
            raise ModuleNotFoundError("HHF's have not been initialized for", self.code, self.title)

        try:
            return self.hhfs.loc[self.hhfs.division.str.lower() == division.lower()].hhf.item()
        except:
            try:
                return self.hhfs.loc[self.hhfs.division_abv.str.lower() == division.lower()].hhf.item()
            except:
                raise NameError(division, 'is not a valid division.') from None

    def title(self, file=classifier_list_file):
        df = pd.read_csv(file)
        try:
            self.title = df.loc[df.code == self.code].title.item()
        except ValueError:
            raise ValueError(str(self.code), 'is not in the classifier list.') from None

    def code(self, file=classifier_list_file):
        df = pd.read_csv(file)
        try:
            self.code = df.loc[df.title == self.title].code.item()
        except ValueError:
            raise ValueError(str(self.title), 'is not in the classifier list.') from None


class Member:
    def __init__(self, name='NULL', number='NULL'):
        self.name = name
        self.number = number


class ClassifierScore:
    def __init__(self):
        self.uspsa = None
        self.practiscore = None
        self.event = None
        self.club = None
        self.level = None
        self.date = filehandler.Date()
        self.date_upload = filehandler.Date()
        self.classifier = Classifier()
        self.division = None
        self.member = Member()
        self.classification = None
        self.hit_factor = None
        self.points = None
        self.time = None
        self.classpct = None


def match_results(match_id=1):
    url = "https://uspsa.org/match-results-details?index=" + str(match_id)
    soup = BeautifulSoup(requests.get(url, headers=HEADER, verify=False).content, features='lxml')

    valid_match = False
    try:
        soup.find('div', attrs={'class': 'alert alert-danger'}).get_text()
    except AttributeError:
        valid_match = True
        print('Match ID', match_id)

    try:
        soup.find('div', attrs={'class': 'card-body d-none d-lg-block'}).get_text().split('\n')
    except AttributeError:
        valid_match = False
    else:
        url = r"https://uspsa.org/match-results-details?index=" + str(match_id) + "&action=stages"
        soup = BeautifulSoup(requests.get(url, headers=HEADER, verify=False).content, features='lxml')
        try:
            soup.find('table', attrs={'class': 'table table-striped table-responsive'}).findAll("tr")
        except AttributeError:
            valid_match = False

    if valid_match is True:
        event = soup.find('div', attrs={'class': 'card-body d-none d-lg-block'}).get_text().split('\n')
        event_name = None
        event_date = None
        event_upload = None
        event_club = None
        for i in range(0, len(event)):
            if event[i] == "Match Name":
                event_name = event[i + 1]
            if event[i] == "Match Date":
                event_date = filehandler.Date(event[i + 1])
            if event[i] == "Results Uploaded":
                event_upload = filehandler.Date(event[i + 1])
            if event[i] == "Host Club":
                event_club = event[i + 1]

        url = r"https://uspsa.org/match-results-details?index=" + str(match_id) + "&action=stages"
        soup = BeautifulSoup(requests.get(url, headers=HEADER, verify=False).content, features='lxml')

        table = soup.find('table', attrs={'class': 'table table-striped table-responsive'}).findAll("tr")
        stages = list()
        for i in range(1, len(table) - 1):
            row = table[i].get_text().split('\n')
            try:
                stages.append([row[1].lstrip().rstrip(), Classifier(code=row[8].lstrip().rstrip())])
            except ValueError:
                pass
            except IndexError:
                pass

        divisions = (['Open', 'Limited', 'Production', 'Revolver', 'Single%20Stack', 'Carry%20Optics', 'PCC', 'Limited%2010', 'Limited%20Optics'])
        scores = list()
        for stage in stages:
            for div in divisions:
                url = r"https://uspsa.org/match-results-details?index=" + str(match_id) + "&division=" + div + "&stage=" + stage[0][0] + "&guntype=Pistol"
                soup = BeautifulSoup(requests.get(url, headers=HEADER, verify=False).content, features='lxml')
                try:
                    table = soup.find('table', attrs={'class': 'table table-striped table-responsive'}).findAll("tr")
                except:
                    pass
                else:
                    for i in range(1, len(table)):
                        row = table[i].get_text().split('\n')
                        score = ClassifierScore()
                        score.uspsa = match_id
                        score.event = event_name
                        score.club = event_club
                        score.date = event_date
                        score.date_upload = event_upload
                        score.member = Member(name=row[2], number=row[3])
                        score.classification = row[4]
                        score.classifier = stage[1]
                        score.division = div.replace("%20", ' ')
                        score.hit_factor = float(row[8])
                        score.time = float(row[7])
                        score.points = int(row[5])
                        classpct = row[11].replace(r'\xa0', '')
                        try:
                            score.classpct = float(''.join([n for n in classpct if n.isdigit()])) / 100
                        except:
                            pass
                        scores.append(score)
        return scores
    print('Match ID', match_id, 'is an invalid match')


def write_match_result(scores, file=uspsa_database):
    try:
        (cursor, conn) = filehandler.open_database(file)
    except FileNotFoundError:
        raise FileNotFoundError
    except sqlite3.InterfaceError:
        raise FileNotFoundError

    for score in scores:
        cursor = conn.cursor()
        sql = '''INSERT INTO match_scores(match_id,practiscore_id,event,club,level,date,date_unix,upload_date,upload_date_unix,classifier_code,classifier_title,member_name,member_number,class,division,hitfactor,class_pct,points,time)
                 VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
        cursor.execute(sql, [score.uspsa, score.practiscore, score.event, score.club, score.level, score.date.text,
                             score.date.unix, score.date_upload.text, score.date_upload.unix, score.classifier.code,
                             score.classifier.title, score.member.name, score.member.number, score.classification,
                             score.division, score.hit_factor, score.classpct, score.points, score.time])
        conn.commit()

    filehandler.close_database(cursor, conn)


def download_score(start_id=1, end_id=10000, file=uspsa_database):
    for i in range(start_id, end_id):
        scores = match_results(i)
        if scores:
            write_match_result(scores, file)


class Club:
    def __int__(self):
        self.id = None
        self.code = None
        self.name = None
        self.section = None
        self.address = None
        self.city = None
        self.state = None
        self.zip = None
        self.md = None
        self.md_phone = None
        self.md_email = None
        self.sc = None
        self.sc_email = None

    def write_db(self, file=uspsa_database):
        try:
            (cursor, conn) = filehandler.open_database(file)
        except FileNotFoundError:
            raise FileNotFoundError
        except sqlite3.InterfaceError:
            raise FileNotFoundError

        try:
            sc_email = self.sc_email.lower()
        except:
            sc_email = self.sc_email

        try:
            md_email = self.md_email.lower()
        except:
            md_email = self.md_email

        cursor = conn.cursor()
        sql = '''INSERT INTO clubs(id,name,code,address,city,state,zip,contact_name,contact_phone,contact_email,section,section_coordinator,section_email)
                 VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)'''
        cursor.execute(sql, [self.id, self.name, self.code, self.address, self.city, self.state, self.zip, self.md,
                             self.md_phone, md_email, self.section, self.sc, sc_email])
        conn.commit()
        filehandler.close_database(cursor, conn)


def update_club(name, code, file=uspsa_database):
    try:
        (cursor, conn) = filehandler.open_database(file)
    except FileNotFoundError:
        raise FileNotFoundError
    except sqlite3.InterfaceError:
        raise FileNotFoundError

    cursor = conn.cursor()
    sql = '''UPDATE match_scores
             SET club_code=?
             WHERE club=?'''
    cursor.execute(sql, [code, name])
    conn.commit()
    filehandler.close_database(cursor, conn)


def classification(division='Open', member='L3137'):
    url = "https://uspsa.org/classification/" + member
    # soup = BeautifulSoup(requests.get(url, headers=HEADER, proxies=PROXY, verify=False).content, features='lxml')
    soup = BeautifulSoup(requests.get(url, headers=HEADER, verify=False).content, features='lxml')
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


def check_division(name, return_short=False, div_list=uspsa_divisions):
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


def read_classifier_data(code, division, start_date, end_date, file=uspsa_database):
    """
    Reads classifier data from the SQL database for a specific division and given data range

    :param code: USPSA stage number
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

    sql = '''SELECT hitfactor FROM match_scores
             WHERE classifier_code=? AND division=? AND date_unix BETWEEN ? AND ?'''
    cursor.execute(sql, (code, check_division(division), start_unix, end_unix))

    try:
        data = cursor.fetchall()
    except:
        filehandler.close_database(cursor, conn)
        raise IndexError('DATABASE: Read error.')
    else:
        filehandler.close_database(cursor, conn)
    return np.array(data).reshape(len(data))


def read_classifier_count(start_date, end_date, file=uspsa_database):
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

    sql = '''SELECT DISTINCT date, classifier_code FROM match_scores
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


def read_match_count(start_date, end_date, file=uspsa_database):
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


def read_member_division_count(start_date, end_date, member, division, file=uspsa_database):
    """
    Counts scores by division of specified member between the start and end dates

    :param start_date: Start date MM/DD/YY
    :type start_date: str
    :param end_date: End date MM/DD/YY
    :type end_date: str
    :param member: member number
    :type member: str
    :param division: division name
    :type division: str
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

    sql = '''SELECT COUNT(hitfactor) FROM match_scores
             WHERE member_number=? AND division=? AND date_unix BETWEEN ? AND ?'''
    cursor.execute(sql, (member, division, start_unix, end_unix))

    try:
        data = cursor.fetchall()
    except:
        filehandler.close_database(cursor, conn)
        raise IndexError('DATABASE: Read error.')
    else:
        filehandler.close_database(cursor, conn)
    return data[0][0]


def read_member_numbers(start_date, end_date, file=uspsa_database):
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

    sql = '''SELECT DISTINCT member_number FROM match_scores
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


def read_member_list(start_date, end_date, file=uspsa_database):
    """
    Returns a list of members

    :param start_date: Start date MM/DD/YY
    :type start_date: str
    :param end_date: End date MM/DD/YY
    :type end_date: str
    :param file: database file path
    :type file: str
    :return: data
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

    sql = '''SELECT DISTINCT member_number FROM match_scores
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
            if item[0].upper() not in members:
                members.append(item[0])
        return members


def read_member_classification_list(start_date, end_date, member_number, division, file=uspsa_database):
    """
    Returns a list of members

    :param start_date: Start date MM/DD/YY
    :type start_date: str
    :param end_date: End date MM/DD/YY
    :type end_date: str
    :param member_number: Member Number
    :type member_number: str
    :param division: division long name
    :type division: str
    :param file: database file path
    :type file: str
    :return: data
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

    sql = '''SELECT DISTINCT class, date, match_id FROM match_scores
             WHERE member_number=? AND division=? AND date_unix BETWEEN ? AND ?
             ORDER BY date_unix ASC'''
    cursor.execute(sql, (member_number, division, start_unix, end_unix))

    try:
        data = cursor.fetchall()
    except:
        filehandler.close_database(cursor, conn)
        raise IndexError('DATABASE: Read error.')
    else:
        filehandler.close_database(cursor, conn)
        return data


def classifier_list(file=classifier_list_file):
    df = pd.read_csv(file)
    return df
