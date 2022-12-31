from config import *
from Utilities import practiscore as ps


def date_to_unix(date):
    date = date.split('/')
    date = datetime.datetime(2000 + int(date[2]), int(date[0]), int(date[1]))
    return int(time.mktime(date.timetuple()))


def unix_to_date(unix):
    return datetime.datetime.utcfromtimestamp(unix).strftime('%m/%d/%Y')


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

