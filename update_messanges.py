import sqlite3
import argparse
from api_request import get_messages_from_vk
from MessageHandler import MessageHandler
import numpy as np

parser = argparse.ArgumentParser("update")
parser.add_argument('--count', type=int, default='10', help='count of request messanges from each group')
args = parser.parse_args()

TOKEN = None

def main():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    groups = cursor.execute("""SELECT * FROM groups""").fetchall()
    messages =[]
    for group in list(map(lambda x:x["name"] ,groups)):
        messages.extend(get_messages_from_vk(TOKEN,group,args.count))

    import baseline
    handler = MessageHandler(baseline.Tokenizer(),
                             baseline.SimpleClassifier(),
                             baseline.Tokenizer(),
                             baseline.SimpleTokenClassifier())

    processed_messages = []
    for message in messages:
        if len(message["text"])< 10 and not cursor.execute("SELECT 1 FROM announcement WHERE text = '{}'".format(message["text"])).fetchall():
            continue
        handle_result = handler.pipeline(message["text"])
        handle_result["text"] = message["text"]
        handle_result["datetime"] = message["date"]
        handle_result["group"] = message["group"]
        processed_messages.append(handle_result)

    for message in processed_messages:
        obj_vector = None
        feature_vector = None
        if not message["object_vector"] is None:
            obj_vector = np.array(message["object_vector"]).tobytes()
        if not message["features_vector"] is None:
            feature_vector = np.array(message["features_vector"]).tobytes()
        cursor.execute("""INSERT INTO announcement (text,object,features,location,datetime,object_vector,features_vector,group_id) 
                        VALUES (?,?,?,?,?,?,?,?);""",
                       (message["text"],message["object"],message["features"],message["location"],message["datetime"],
                        obj_vector,feature_vector, """SELECT id FROM groups WHERE name = '{}'""".format(message["group"])))
    connection.commit()
    connection.close()

main()