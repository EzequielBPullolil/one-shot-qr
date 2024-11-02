import sqlite3
from os import environ

db_path = environ["DB_PATH"]
class UrlModel:
    def create(uuid:str, encryptedUrl: bytes, cap: int):
        connection = sqlite3.connect(db_path)
        c = connection.cursor()
        c.execute(f'INSERT INTO URL (uuid, url_encrypted, cap) VALUES(?,?,?)', (uuid, encryptedUrl, cap))
        connection.commit()
        connection.close()


    def read_and_decrease_cap(uuid: str) -> str:
        connection = sqlite3.connect(db_path)
        c = connection.cursor()
        c.execute('SELECT url_encrypted, cap FROM URL WHERE uuid = ?', (uuid,))

        data = c.fetchone()
        if data == None:
            return ""


        url_encrypted, cap = data

        print(url_encrypted, cap)
        cap -= 1
        if cap <= 0:
            c.execute('DELETE FROM URL WHERE uuid=?', (uuid,))
        else:
            c.execute('UPDATE URL SET cap = ? WHERE uuid = ?', (cap, uuid))

        connection.commit()
        connection.close()

        return url_encrypted