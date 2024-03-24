import sqlite3

connection = sqlite3.connect('database.db')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

a = cursor.execute(""" SELECT * FROM announcement""").fetchall()

b = list(map(lambda x: dict(x),a))
connection.close()