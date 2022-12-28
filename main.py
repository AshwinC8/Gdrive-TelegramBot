import config
import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_creds():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds
    

def start(update, context):
  context.bot.send_message(chat_id=update.effective_chat.id, text="Hello User, This bot can help you upload the files in the group directly to the google drive.")


def help(update, context):
  context.bot.send_message(chat_id=update.effective_chat.id, text="* Upload the file into the chat\n* Login to Google account to upload to drive ")


def file_handler(update, context):
  """handles the uploaded files"""
  file = context.bot.getFile(update.message.document.file_id)

  os.chdir(os.getcwd()+"/downloads/")
  file.download(update.message.document.file_name)
  os.chdir(os.getcwd()+"/../")

  document = update.message.document
  try:
        # create drive api client
        service = build('drive', 'v3', credentials=get_creds())

        file_metadata = {'name': document.file_name}
        media = MediaFileUpload('downloads/'+document.file_name,
                                mimetype=document.mime_type)
        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, media_body=media,).execute()
  except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

  doc = update.message.document
  filename = doc.file_name

  context.bot.send_message(chat_id=update.effective_chat.id, text="File Uploaded!")


def main():
    updater = Updater(token=config.TOKEN,use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(MessageHandler(Filters.document,file_handler))
    updater.start_polling()

if __name__ == '__main__':
    main()
