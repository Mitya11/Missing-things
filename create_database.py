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
INSERT INTO groups (id,name,city,type) VALUES (-1002120650535,'Parse2','Пенза','telegram'),
                                              (-1002120920125,'ParseChannel','Пенза','telegram'),
                                              (1,'bnpenza','Пенза','vk');""")
connection.commit()

cursor.execute("""CREATE TABLE announcement (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               from_user TEXT,
               text TEXT NOT NULL,
               object TEXT,
               features TEXT,
               location TEXT,
               datetime INTEGER,
               object_vector BLOB,
               features_vector BLOB,
               type INTEGER,
               media BLOB,
               contact TEXT,
               group_id INT,
               FOREIGN KEY (group_id) REFERENCES groups(id)
               );""")
connection.commit()



connection.close()