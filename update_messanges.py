import sqlite3
from api_request import get_messages_from_vk,get_messanges_from_telegram
import numpy as np
from tqdm import tqdm
from MessageHandler import handler
import re


def update_database(tg_api_session,count,vk_token = None):
    print("Подключение к базе данных.")
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    groups = cursor.execute("""SELECT * FROM groups""").fetchall()
    messages =[]
    for group in list(groups):
        try:
            if group["type"] == "vk" and vk_token:
                messages.extend(get_messages_from_vk(vk_token,group["name"],count))
            elif group["type"] == "telegram":
                messages.extend(get_messanges_from_telegram(tg_api_session, group["id"], count))
        except:
            continue
    processed_messages = []
    for message in tqdm(messages):
        if len(message["text"])< 10 or cursor.execute("SELECT 1 FROM announcement WHERE text = ?",(message["text"],)).fetchall():
            continue
        handle_result = handler.pipeline(message["text"])
        if handle_result == False:
            continue
        handle_result["from_user"] = message["from_user"]
        handle_result["text"] = message["text"]
        handle_result["datetime"] = message["date"]
        handle_result["group"] = message["group"]
        """img_bytes = tg_api_session.download_media(message=message["media"],
                                       file_name=str(message["from_user"])  + ".jpg",
                                       in_memory=True) #если сообщение успешно, загружаем медиа
        bytes = img_bytes.getbuffer().tobytes()"""
        handle_result["media"] = None
        handle_result["contact"] = None
        contact = re.findall("\+"+"\d[^\d]{,3}"*10+"\d",handle_result["text"]) + re.findall("\d[^\d]{,3}"*10+"\d",handle_result["text"])
        if contact:
            handle_result["contact"] = contact[0]

        processed_messages.append(handle_result)

    for message in processed_messages:
        obj_vector = None
        feature_vector = None
        if not message["object_vector"] is None:
            obj_vector = np.array(message["object_vector"]).tobytes()
        if not message["features_vector"] is None:
            feature_vector = np.array(message["features_vector"]).tobytes()
        group_query ="SELECT id FROM groups WHERE name = '{}'".format(message["group"])
        cursor.execute("""INSERT INTO announcement (from_user,text,object,features,location,datetime,object_vector,features_vector,type,media,contact,group_id) 
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,(""" + group_query+"""));""",
                       (message["from_user"],message["text"],message["object"],message["features"],message["location"],message["datetime"],
                        obj_vector,feature_vector,message["type"],message["media"],message["contact"]))
    connection.commit()
    connection.close()
    print("База обновлена!")
