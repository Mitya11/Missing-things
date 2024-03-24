import sqlite3
from Announcement import scoring
from MessageHandler import handler
import numpy as np


def find_similarity(text,types,count):
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    messanges = cursor.execute("""SELECT * FROM announcement""").fetchall()
    messanges  = list(map(lambda x: dict(x),messanges))

    for i in range(len(messanges)):
        if not messanges[i]["object_vector"] is None:
            messanges[i]["object_vector"] = np.frombuffer(messanges[i]["object_vector"],dtype=np.float32)
        if not messanges[i]["features_vector"] is None:
            messanges[i]["features_vector"] = np.frombuffer(messanges[i]["features_vector"],dtype=np.float32)

    source_info = handler.pipeline(text)
    if not source_info:
        source_info = handler.pipeline("Потерял "+text)
    if not source_info:
        return []
    print("Объект:", source_info["object"])
    rel_messages = []
    for i in range(len(messanges)):
        messanges[i]["group_name"] = cursor.execute("SELECT name FROM groups WHERE id =" +str(messanges[i]["group_id"])).fetchone()["name"]
        messanges[i]["score"] = scoring(source_info, messanges[i])
        if messanges[i]["type"] not in types:
            messanges[i]["score"] = 0
        else:
            rel_messages.append(messanges[i])

    rel_messages.sort(key=lambda x: x["score"], reverse=True)
    connection.close()
    return rel_messages[:count]




