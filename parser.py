from pyrogram import Client
import settings as set


def ParseChat():
    app = Client('parser', api_id=set.api_id, api_hash=set.api_hash)
    app.start()
    for chat in set.chats:
        history = app.get_chat_history(chat_id=chat)
        for message in history:
            if message.from_user is not None:
                if message.text is not None:
                    print(message.text)
                if message.caption is not None:
                    print(message.caption)
                print(message.date)
                print(message.id)
                print(message.from_user.username)
                print(message.chat.username)
                print(message.chat.id)
                if message.media is not None:
                    app.download_media(message=message,
                                       file_name= str(message.chat.username) + "-" + str(message.id) + ".jpg")
                print("-----")


def ParseChannel():
    app = Client('parser', api_id=set.api_id, api_hash=set.api_hash)
    app.start()
    for channel in set.channels:
        history = app.get_chat_history(chat_id=channel)
        for message in history:
            if message is not None:
                if message.text is not None:
                    print(message.text)
                if message.caption is not None:
                    print(message.caption)
                print(message.sender_chat.username)
                print(message.date)
                print(message.id)
                print(message.chat.username)
                print(message.chat.id)
                if message.media is not None:
                    app.download_media(message=message,
                                       file_name= str(message.chat.username) + "-" + str(message.id) + ".jpg")
                print("-----")

ParseChannel()
