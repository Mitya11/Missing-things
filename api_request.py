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
            for i in range(len(messages)): messages[i]["group"] = group
            count -=100
            j +=1
            time.sleep(1)
        except Exception as e:
            print(e)
    return messages
