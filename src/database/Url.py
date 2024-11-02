import sqlite3
from os import environ

db_path = environ["DB_PATH"]
class UrlModel:
    def create(uuid:str, encryptedUrl: bytes, cap: int):
        connection = sqlite3.connect(db_path)
        c = connection.cursor()
        print(encryptedUrl.decode())
        c.execute(f'INSERT INTO URL (uuid, url_encrypted, cap) VALUES(?,?,?)', (uuid, encryptedUrl.decode(), cap))
        connection.commit()
        connection.close()


    def read():
        pass