import configparser
from pyrogram import Client
import sqlite3

config = configparser.ConfigParser()
config.read("config.ini")
chats = config["Chats"]["chats"]

api_id = config["TelegramAPI"]["api_id"]
api_hash = config["TelegramAPI"]["api_hash"]
print("Подключение Telegram API.")
tg_api_session = Client('parser', api_id=api_id, api_hash=api_hash)
tg_api_session.start()

me = tg_api_session.search_global()
chats = set()
i = 0
for message in me:
    if i > 3000:
        break
    if message.chat.title is not None:
        chats.add(tuple((message.chat.id,message.chat.title)))
    i+=1

connection = sqlite3.connect('database.db')

cursor = connection.cursor()

for i in chats:
    try:
        cursor.execute("""
INSERT INTO groups (id,name,city,type) VALUES (?,?,'Пенза','telegram'),;""",(i[0],i[1]))
    except:
        continue
connection.commit()