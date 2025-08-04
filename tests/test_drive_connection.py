from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()

SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_CREDS_PATH")
ROOT_FOLDER_ID = os.getenv("ROOT_FOLDER_ID")

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/drive.readonly']
)

service = build('drive', 'v3', credentials=creds)

results = service.files().list(
    q=f"'{ROOT_FOLDER_ID}' in parents and trashed=false",
    pageSize=10,
    fields="files(id, name, mimeType)"
).execute()

items = results.get('files', [])

print("Drive API Response:", items)
