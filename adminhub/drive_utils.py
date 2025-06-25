# drive_utils.py
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Define the required scopes
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = os.path.join(
    os.path.dirname(__file__), 'path/to/your_service_account.json'
)

def get_drive_service():
    """
    Returns an authorized Google Drive service instance.
    """
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build('drive', 'v3', credentials=credentials)
    return service

def upload_file(file_path, filename, parent_folder_id=None, mimetype=None):
    """
    Uploads a file to Google Drive.
    """
    service = get_drive_service()

    file_metadata = {'name': filename}
    if parent_folder_id:
        file_metadata['parents'] = [parent_folder_id]

    media = MediaFileUpload(file_path, mimetype=mimetype)
    uploaded_file = service.files().create(
        body=file_metadata, media_body=media, fields='id'
    ).execute()
    
    file_id = uploaded_file.get('id')

    # Set the file permission to 'public' (anyone with the link can view)
    set_public_permission(file_id)
    
    return file_id

def set_public_permission(file_id):
    """
    Sets the file permission so that anyone with the link can view the file.
    """
    service = get_drive_service()
    permission_body = {
        'type': 'anyone',
        'role': 'reader'
    }
    service.permissions().create(fileId=file_id, body=permission_body).execute()

def generate_file_viewer_link(file_id):
    """
    Generates a viewer link for embedding or redirection.
    """
    # Example: If the file is a PDF/video, you might embed it using Google Drive's viewer:
    return f"https://drive.google.com/file/d/{file_id}/preview"