# uses the GMail API to send emails to people
# Edited from the following source
# https://learndataanalysis.org/how-to-use-gmail-api-to-send-an-email-in-python/


import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request

def create_gmail_service(client_secret_file='client_secret.json', scope=['https://mail.google.com/']):
    # make sure the file is called client_secret.json
    pickle_file = 'gmail_token.pickle'

    credentials = None

    try:
        with open(pickle_file, 'rb') as token:
            credentials = pickle.load(token)
    except Exception as e:
        print('Error occured:', e)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            print("test")
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scope)
            credentials = flow.run_local_server()
        with open(pickle_file, 'wb') as token:
            pickle.dump(credentials, token)

    API_SERVICE_NAME = 'gmail'
    API_VERSION = 'v1'

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None
