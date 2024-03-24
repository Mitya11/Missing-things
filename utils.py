import io
import json
import base64

msg_types = {1:"Пропажа", 2:"Находка", 3:"Отдам в хорошие руки"}

def forming_response(msg):
    result = "Название канала: " + msg["group_name"] + "\n"
    if msg["from_user"] is not None:
        result += "Имя пользователя: " + msg["from_user"]  + "\n"
    if msg["contact"] is not None:
        result += "Контактные данные: " + msg["contact"]  + "\n"
    else:
        result += "Контактные данные: " + "Не указаны" + "\n"
    if msg["location"] is not None:
        result += "Контактные данные: " + msg["location"]  + "\n"
    else:
        result += "Контактные данные: " + "Не указано" + "\n"
    result += msg_types[msg["type"]] + " : " + msg["object"] + "\n\n"
    result += "Текст сообщения: \n" + msg["text"]
    return result

def to_json(msg):
    for i in range(len(msg)):
        if not msg[i]["object_vector"] is None:
            msg[i]["object_vector"] = msg[i]["object_vector"].tolist()
        if not msg[i]["features_vector"] is None:
            msg[i]["features_vector"] = msg[i]["features_vector"].tolist()
        if not msg[i]["media"] is None:
            msg[i]["media"] = base64.b64encode(msg[i]["media"]).decode('ascii')

    js = json.dumps(msg, ensure_ascii=False)
    file_obj = io.StringIO(initial_value=js)
    file_obj.name = "data.json"

    return file_obj