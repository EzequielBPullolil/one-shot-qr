import sqlite3
import os

db_path = os.getenv("DB_PATH")


if not db_path:
    raise EnvironmentError("La variable de entorno DB_PATH no está definida.")


with sqlite3.connect(db_path) as conn:
    connection = sqlite3.connect(db_path)
    c = connection.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS URL (
            uuid TEXT, 
            url_encrypted TEXT,
            cap INTEGER,
            PRIMARY KEY(uuid ASC))
    ''')
