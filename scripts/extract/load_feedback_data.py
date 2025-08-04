import os
import pandas as pd
import yaml
import requests
from io import StringIO
from google.oauth2 import service_account
import google.auth.transport.requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Path definitions
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'data'))
YAML_PATH = os.path.join(DATA_DIR, 'configs', 'links.yaml')

# OAuth Credentials setup
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_CREDS_PATH")

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

auth_req = google.auth.transport.requests.Request()
credentials.refresh(auth_req)
headers = {'Authorization': f'Bearer {credentials.token}'}

# Load YAML configuration
with open(YAML_PATH, 'r') as file:
    links_dict = yaml.safe_load(file)

# Dictionary to store DataFrames
student_feedback_dict = {"older": {}, "younger": {}}

# Loop through years and categories
for year, categories in links_dict.items():
    for category, schools in categories.items():
        all_dfs = []
        print(f"\n📅 Loading data for {year} - {category}")

        for school, tabs in schools.items():
            for tab_name, details in tabs.items():
                sheet_id = details['sheet_id']
                gid = details['gid']
                csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

                print(f"⏳ Loading {school} - {tab_name}")

                try:
                    response = requests.get(csv_url, headers=headers)
                    response.raise_for_status()

                    # Safely decode response content, handling emojis and other special chars
                    content = response.content.decode('utf-8', errors='replace')

                    df = pd.read_csv(StringIO(content))
                    df['School'] = school
                    df['Year'] = year
                    df['Tab'] = tab_name
                    all_dfs.append(df)

                    print(f"✅ Successfully loaded {school} - {tab_name}")

                except Exception as e:
                    print(f"❌ Failed to load {school} - {tab_name}: {e}")

        # Concatenate and store in dictionary
        if all_dfs:
            combined_df = pd.concat(all_dfs, ignore_index=True)
            student_feedback_dict[category][year] = combined_df

            # Correct file naming with category and year
            csv_path = os.path.join(DATA_DIR, 'raw', category, f"sy{year}_{category}_feedback.csv")
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)
            combined_df.to_csv(csv_path, index=False)
            print(f"💾 Saved combined DataFrame to {csv_path}")
