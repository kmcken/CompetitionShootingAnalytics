from config import *
from Application import practiscore as ps


class Date:
    def __init__(self, date=None):
        self.text = None
        self.datetime = None
        self.unix = None

        def _unix(datestamp):
            return datetime.datetime.timestamp(datestamp)

        def _datetime(datestr):
            try:
                string = datestr.split('/')
                return datetime.datetime(2000 + int(string[2]), int(string[0]), int(string[1]))
            except:
                try:
                    string = datestr.split(' ')
                    string_day = string[0].split('-')
                    string_hour = string[1].split(':')
                    string_second = string_hour[2].split('.')
                    return datetime.datetime(int(string_day[0]), int(string_day[1]), int(string_day[2]),
                                             int(string_hour[0]), int(string_hour[1]), int(string_second[0]),
                                             int(string_second[1]), tzinfo=datetime.timezone.utc)
                except:
                    string = datestr.split(' ')
                    string_day = string[0].split('/')
                    string_hour = string[1].split(':')
                    if string[2] == 'PM' and int(string_hour[0]) < 12:
                        return datetime.datetime(int(string_day[2]) + 2000, int(string_day[0]), int(string_day[1]),
                                                 int(string_hour[0]) + 12, int(string_hour[1]), int(string_hour[2]),
                                                 tzinfo=datetime.timezone.utc)
                    else:
                        return datetime.datetime(int(string_day[2]) + 2000, int(string_day[0]), int(string_day[1]),
                                                 int(string_hour[0]), int(string_hour[1]), int(string_hour[2]),
                                                 tzinfo=datetime.timezone.utc)

        if isinstance(date, datetime.datetime):
            self.text = str(date)
            self.datetime = date
            self.unix = _unix(date)
        elif isinstance(date, float):
            self.text = str(datetime.datetime.fromtimestamp(date))
            self.datetime = datetime.datetime.fromtimestamp(date)
            self.unix = date
        elif isinstance(date, str):
            self.text = date
            self.datetime = _datetime(date)
            self.unix = _unix(self.datetime)


def new_json(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def add_to_json(file, data):
    with open(file, 'r') as f:
        jdata = json.load(f)
        jdata.update(data)  # add, remove, modify content

    # create randomly named temporary file to avoid
    # interference with other thread/asynchronous request
    tempfile = os.path.join(os.path.dirname(file), str(uuid.uuid4()))
    with open(tempfile, 'w', encoding='utf-8') as f:
        json.dump(jdata, f, indent=4)

    # rename temporary file replacing old file
    os.replace(tempfile, file)


def read_json(file):
    with open(file, 'r') as f:
        jdata = json.load(f)
    return jdata


def convert_to_json(path=root+'/Data/txtFiles/'):
    file_list = os.listdir(path)
    for file in file_list:
        if file.split('.')[-1] == 'txt':
            ps.txt_to_json(path + file)


def open_database(file=None):
    if file is None:
        raise FileNotFoundError('DATABASE: Missing database file input.')

    try:
        conn = sqlite3.connect(file)
    except sqlite3.InterfaceError:
        raise sqlite3.InterfaceError
    else:
        cursor = conn.cursor()
        return cursor, conn


def close_database(cursor, conn):
    cursor.close()
    conn.close()
