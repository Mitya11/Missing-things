import sqlite3
import argparse
from Announcement import scoring
from MessageHandler import MessageHandler
import numpy as np

parser = argparse.ArgumentParser("update")
parser.add_argument('--text', type=str, default='Потерялась собака', help='text')
parser.add_argument('--count', type=int, default='10', help='text')

args = parser.parse_args()

def main():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    messanges = cursor.execute("""SELECT * FROM announcement""").fetchall()
    messanges = b = list(map(lambda x: dict(x),messanges))

    for i in range(len(messanges)):
        if not messanges[i]["object_vector"] is None:
            messanges[i]["object_vector"] = np.frombuffer(messanges[i]["object_vector"],dtype=np.float32)
        if not messanges[i]["features_vector"] is None:
            messanges[i]["features_vector"] = np.frombuffer(messanges[i]["features_vector"],dtype=np.float32)

    import baseline
    handler = MessageHandler(baseline.Tokenizer(),
                             baseline.SimpleClassifier(),
                             baseline.Tokenizer(),
                             baseline.SimpleTokenClassifier())

    source_info = handler.pipeline(args.text)

    for i in range(len(messanges)):
        messanges[i]["score"] = scoring(source_info, messanges[i])

    messanges.sort(key=lambda x: x["score"], reverse=True)
    connection.close()
    return messanges[:args.count]

print(main())




