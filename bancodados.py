import sqlite3

conn = sqlite3.connect("bancodados.db")

cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                senha TEXT NOT NULL
)""")

conn.commit()
conn.close()