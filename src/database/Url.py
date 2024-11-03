'''
    UrlModel module container
'''
import sqlite3
from os import environ

db_path = environ["DB_PATH"]


class UrlModel:
    '''
        ImproveOffers an interface to manage URL table in the DB
    '''
    @staticmethod
    def create(uuid: str, encrypted_url: bytes, cap: int):
        '''
            Persists a URL record associated with the encrypted URL
        '''
        connection = sqlite3.connect(db_path)
        c = connection.cursor()
        c.execute(
            'INSERT INTO URL (uuid, url_encrypted, cap) VALUES(?,?,?)',
            (uuid, encrypted_url, cap))
        connection.commit()
        connection.close()

    @staticmethod
    def read_and_decrease_cap(uuid: str) -> (str, int):
        '''
            Fetch one ROW assoc with id @uuid and decrease it cap in one,
            if the cap after decrease the cap is lower than 0 delete the row
        '''
        connection = sqlite3.connect(db_path)
        c = connection.cursor()
        c.execute('SELECT url_encrypted, cap FROM URL WHERE uuid = ?', (uuid,))

        data = c.fetchone()
        if data is None:
            return ""

        url_encrypted, cap = data

        print(url_encrypted, cap)
        new_cap = cap-1
        if new_cap <= 0:
            c.execute('DELETE FROM URL WHERE uuid=?', (uuid,))
        else:
            c.execute('UPDATE URL SET cap = ? WHERE uuid = ?', (new_cap, uuid))

        connection.commit()
        connection.close()

        return (url_encrypted, cap)
