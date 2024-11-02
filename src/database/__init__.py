import sqlite3
from os import environ

db_path = environ["DB_PATH"]

try: 
    connection = sqlite3.connect(db_path)
    c = connection.cursor()


    c.execute('CREATE TABLE URL (uuid TEXT, url_encrypted TEXT, cap INTEGER, PRIMARY KEY(uuid ASC))')


    connection.commit()

    connection.close()
except sqlite3.OperationalError as e:
    if 'table URL already exists' in e.args[0]:
        pass 
    else:
        raise e
