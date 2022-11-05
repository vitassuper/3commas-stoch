from telegram import Bot
import os

def send_notification(text):
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    token = os.getenv('TELEGRAM_BOT_TOKEN')

    bot = Bot(token)

    bot.send_message(chat_id, text)
