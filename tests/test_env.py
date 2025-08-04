import os
from dotenv import load_dotenv

load_dotenv()

print("ROOT_FOLDER_ID:", os.getenv("ROOT_FOLDER_ID"))
print("GOOGLE_CREDS_PATH:", os.getenv("GOOGLE_CREDS_PATH"))
