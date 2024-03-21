import sqlite3

connection = sqlite3.connect('database.db')

cursor = connection.cursor()

cursor.execute("""
               CREATE TABLE groups (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
city TEXT, 
type TEXT
);""")

cursor.execute("""
INSERT INTO groups (name,city) VALUES ('nsknahodka','Новосибирск');""")
connection.commit()

cursor.execute("""CREATE TABLE announcement (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               text TEXT NOT NULL,
               object TEXT,
               features TEXT,
               location TEXT,
               datetime INTEGER,
               object_vector BLOB,
               features_vector BLOB,
               group_id INT,
               FOREIGN KEY (group_id) REFERENCES groups(id)
               );""")
connection.commit()



connection.close()