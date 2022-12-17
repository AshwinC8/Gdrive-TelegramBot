import logging
from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
# from .gsheets_main import upload_to_sheets
import csv

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

def entry(bot, update):
    global user_log
    # logging.info(update)  # comment out in production
    if update.message and update.message.text:
        chat_id = update.message.chat_id
        text = update.message.text
        if text=="/start":
            bot.sendMessage(
                    chat_id=chat_id,
                    text="Hello User, This bot can help you upload the files in the group directly to the google drive.",
                )
        elif text=="/help":           
            bot.sendMessage(
                    chat_id=chat_id,
                    text="* Upload the file into the chat\n* Login to Google account to upload to drive ",
                )
            