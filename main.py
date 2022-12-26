import config
import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def start(update, context):
  context.bot.send_message(chat_id=update.effective_chat.id, text="Hello User, This bot can help you upload the files in the group directly to the google drive.")


def help(update, context):
  context.bot.send_message(chat_id=update.effective_chat.id, text="* Upload the file into the chat\n* Login to Google account to upload to drive ")


def file_handler(update, context):
  """handles the uploaded files"""
  file = context.bot.getFile(update.message.document.file_id)

  cDir = os.getcwd()
  os.chdir(cDir+"/downloads/")
  file.download(update.message.document.file_name)
  os.chdir(cDir+"/../")

  doc = update.message.document
  filename = doc.file_name

  context.bot.send_message(chat_id=update.effective_chat.id, text="✅ File Downloaded!")


def main():
    updater = Updater(token=config.TOKEN,use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(MessageHandler(Filters.document,file_handler))
    updater.start_polling()

if __name__ == '__main__':
    main()
