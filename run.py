import time
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

SCOPES = ['https://mail.google.com/']

def get_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def delete_old_emails():
    service = get_service()
    query = "older_than:6m"
    total_deleted = 0

    while True:
        results = service.users().messages().list(
            userId='me', q=query, maxResults=500
        ).execute()

        messages = results.get('messages', [])

        if not messages:
            print(f"All done! Total deleted: {total_deleted}")
            break

        message_ids = [msg['id'] for msg in messages]
        service.users().messages().batchDelete(
            userId='me',
            body={'ids': message_ids}
        ).execute()

        total_deleted += len(message_ids)
        print(f"Deleted {total_deleted} emails so far...")

        time.sleep(1)

if __name__ == '__main__':
    delete_old_emails()