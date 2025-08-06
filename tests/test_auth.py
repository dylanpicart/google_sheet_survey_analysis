from google.oauth2 import service_account
import google.auth.transport.requests
import requests
import os
from dotenv import load_dotenv

load_dotenv()

SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_CREDS_PATH")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly", "https://www.googleapis.com/auth/drive.readonly"]

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

sheet_id = "101AXR1K_M6RlYP4bUmMBH8pY965z3mq70WeBlohailY"
gid = "554943180"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

# Proper auth flow to get Bearer token
auth_req = google.auth.transport.requests.Request()
credentials.refresh(auth_req)
headers = {"Authorization": f"Bearer {credentials.token}"}

response = requests.get(url, headers=headers)

print("Status code:", response.status_code)
if response.status_code == 200:
    print("✅ Access successful.")
    print(response.text[:500])
else:
    print("❌ Access failed. Response:", response.text)
