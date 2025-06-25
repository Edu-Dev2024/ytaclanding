from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

# Scopes – for uploading files to the user's drive (limited to file scope)
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Path to your downloaded credentials.json from Google Cloud Console
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), 'credentials.json')

# Local token to store access/refresh tokens after initial login
TOKEN_FILE = os.path.join(os.path.dirname(__file__), 'token.json')


def get_drive_service():
    creds = None
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
    creds = flow.run_local_server()
    print("Redirect URI used:", creds.token_uri)
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)


def upload_file_to_folder(file_path, filename, mimetype, folder_id):
    service = get_drive_service()
    file_metadata = {
        'name': filename,
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, mimetype=mimetype)

    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webViewLink'
    ).execute()

    return uploaded_file.get('id'), uploaded_file.get('webViewLink')
