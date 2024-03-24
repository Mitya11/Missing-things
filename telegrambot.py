import configparser

import telebot
from pyrogram import Client
from update_messanges import update_database
from find_similarity import find_similarity
import io
from utils import forming_response, to_json

config = configparser.ConfigParser()
config.read("config.ini")
chats = config["Chats"]["chats"]

api_id = config["TelegramAPI"]["api_id"]
api_hash = config["TelegramAPI"]["api_hash"]
print("Подключение Telegram API.")
tg_api_session = Client('parser', api_id=api_id, api_hash=api_hash)
tg_api_session.start()
print("Подключено.")

vk_token = config["VKAPI"]["token"]
token = config["TelegramBot"]["token"]
bot = telebot.TeleBot(token,threaded=False)

chat_status = {}
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Привет, это бот который поможет найти потерянные вещи. Отправьте /lostitem для создания объявления о пропаже вещи!")

def send_message_to_user(user_id, message):
    bot.send_message(user_id, message)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def welcome_handler(message):
    global chat_status

    bot_status = ""
    if message.chat.id in chat_status:
        bot_status = chat_status[message.chat.id]
    def standart_response(msg):
        if len(msg) == 0:
            bot.send_message(message.chat.id, "Совпадения не найдены")
            return None
        print(len(msg))
        for i in range(len(msg)):
            try:
                if msg[i]["score"] != 0:
                    bot.send_message(message.chat.id, forming_response(msg[i]))
                    if msg[i]["media"] is not None:
                        bot.send_photo(message.chat.id, io.BytesIO(msg[i]["media"]))
            except:
                pass

        file_obj = to_json(msg)
        bot.send_document(message.chat.id,file_obj)
    print("Поступление сообщения:",message.text)
    if message.text == '/help':
        bot.send_message(message.chat.id, """/search - для поиска по ключевым словам
/update_database - для загрузки новых сообщений в базу данных
/get_json - получить все сообщения в json формате""")

    if message.text == '/update_database':
        update_database(tg_api_session,100,vk_token=vk_token)
        bot.send_message(message.chat.id, "База обновлена!")
    elif message.text == '/search':
        bot_status = "search_wait"
        bot.send_message(message.chat.id, "Введите сообщение.")
    elif message.text == '/find':
        bot_status = "find_wait"
        bot.send_message(message.chat.id, "Что вы нашли?")
    elif message.text == '/miss':
        bot_status = "miss_wait"
        bot.send_message(message.chat.id, "Что вы потеряли?")
    elif message.text == '/best_hands':
        bot_status = "best_hands_wait"
        bot.send_message(message.chat.id, "Кого вы хотели бы взять к себе?")

    elif bot_status == "search_wait":
        msg = find_similarity(message.text,[1,2,3],15)
        standart_response(msg)
        bot_status = ""

    elif bot_status == "find_wait":
        msg = find_similarity("Я нашёл "+message.text,[1],10)
        standart_response(msg)
        bot_status = ""

    elif bot_status == "miss_wait":
        msg = find_similarity("Я потерял "+message.text,[2],10)
        standart_response(msg)
        bot_status = ""

    elif bot_status == "best_hands_wait":
        msg = find_similarity("Я потерял "+message.text,[3],10)
        standart_response(msg)
        bot_status = ""

    elif '/get_json' == message.text:
        msg = find_similarity("Потерял вещь",[1,2,3],10000)
        file_obj = to_json(msg)
        bot.send_document(message.chat.id,file_obj)

    if bot_status == "" and message.chat.id in chat_status:
        del chat_status[message.chat.id]
    elif bot_status != "":
        chat_status[message.chat.id] = bot_status
bot.polling(none_stop=True, interval=0)