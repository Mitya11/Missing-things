import sqlite3
import argparse
from Announcement import scoring
from MessageHandler import MessageHandler
import numpy as np
from models.msgExtractor import BertTokenClassifier
from models.msgClassifier import BertSequenceClassifier

parser = argparse.ArgumentParser("update")
parser.add_argument('--text', type=str, default='Потерялась собака', help='text')
parser.add_argument('--count', type=int, default='100', help='text')

args = parser.parse_args()

def main():
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

    handler = MessageHandler("configs/bert-tiny-tokenizer",
                             BertSequenceClassifier(),
                             "configs/rubert-tokenizer",
                             BertTokenClassifier())
    handler.load()
    source_info = handler.pipeline(args.text)
    print(source_info)
    print("******************")

    for i in range(len(messanges)):
        messanges[i]["score"] = scoring(source_info, messanges[i])

    messanges.sort(key=lambda x: x["score"], reverse=True)
    connection.close()
    return messanges[:args.count]

<<<<<<< Updated upstream
simi = main()

for i in simi:
    print(i["text"])
    print("-------------------")
=======
#print(main())
>>>>>>> Stashed changes




