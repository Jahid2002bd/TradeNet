import os
from telegram import Bot

def send_message(message: str) -> None:
    bot = Bot(token=os.getenv("7597308355:AAGevLTQSQnxP_6WDVNO6_Ks81lrCzYefcc"))
    bot.send_message(chat_id=os.getenv("7295931540"), text=message)
