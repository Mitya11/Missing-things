import requests
import time
VERSION = 5.131
def get_messages_from_vk(token,group,count,data = None):
    messages = []
    j = 0
    while count > 0:
        try:
            data = requests.get('https://api.vk.com/method/wall.get',
                                params={'access_token': token,
                                        'v': VERSION,
                                        'domain': group,
                                        'count': count,
                                        'filter': str('owner'),
                                        "offset": j * 100}, timeout=5).json()
            messages.extend(list(map(lambda x: x, data["response"]["items"])))
            for i in range(len(messages)):
                messages[i]["group"] = group
                messages[i]["from_user"] = None
                messages[i]["media"] = None

            count -=100
            j +=1
            time.sleep(1)
        except Exception as e:
            print(e)
    return messages

def get_messanges_from_telegram(app,channel,count):
    history = app.get_chat_history(chat_id=channel,limit=count)
    messanges = []
    last_media = None
    #p = list(history)
    for message in history:
        try:
            if message.from_user is None:
                username = None
            elif message.from_user.username is None:
                username = message.from_user.first_name
            else:
                username = message.from_user.username

            if message.from_user is not None and message.text is not None:
                messanges.append({"text":message.text, "group":message.chat.title, "from_user":username,"date": message.date,"media":last_media})
                last_media= None

            if message.media is not None:
                if message.caption is not None:
                    messanges.append({"text":message.caption, "group":message.chat.title, "from_user":username,"date": message.date,"media":message})
                else:
                    last_media = message
        except:
            continue
    return messanges