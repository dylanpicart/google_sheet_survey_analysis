from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import yaml
import os
import time
import random
from dotenv import load_dotenv

load_dotenv()

ROOT_FOLDER_ID = os.getenv("ROOT_FOLDER_ID")
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_CREDS_PATH")

SCOPES = [
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/spreadsheets.readonly'
]


def authenticate_drive():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds), build('sheets', 'v4', credentials=creds)


def exponential_backoff(request_func, *args, retries=7, **kwargs):
    for n in range(retries):
        try:
            return request_func(*args, **kwargs)
        except HttpError as error:
            if error.resp.status in [403, 429, 500, 503]:
                wait = min(60, (2 ** n) + random.uniform(0.5, 1.5))
                print(f"🔁 Retrying ({error.resp.status}) (attempt {n+1}/{retries}) after {wait:.1f}s...")
                time.sleep(wait)
            else:
                raise
        except Exception as e:
            wait = min(60, (2 ** n) + random.uniform(0.5, 1.5))
            print(f"🔁 Unexpected error '{e}' (attempt {n+1}/{retries}) — sleeping for {wait:.1f}s...")
            time.sleep(wait)
    raise RuntimeError("Max retries exceeded")


def list_subfolders(service, parent_id):
    query = f"'{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
    return exponential_backoff(service.files().list(q=query, pageSize=200).execute).get('files', [])


def list_sheets_in_folder(service, folder_id):
    query = f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.spreadsheet' and trashed=false"
    return exponential_backoff(service.files().list(q=query, pageSize=50).execute).get('files', [])


def categorize_school(school_name):
    older_keywords = ["High School", "HS", "Origins", "Rockaway", "Collegiate", "BLA", "Bronx Leadership Academy",
                      "Fordham Leadership Academy", "FLA", "Fordham", "New Visions"]
    return "older" if any(keyword.lower() in school_name.lower() for keyword in older_keywords) else "younger"


def generate_sheet_tabs(service, spreadsheet_id):
    request = service.spreadsheets().get(spreadsheetId=spreadsheet_id)
    sheet_metadata = exponential_backoff(request.execute)
    sheets = sheet_metadata.get('sheets', [])
    return {sheet['properties']['title']: sheet['properties']['sheetId'] for sheet in sheets}


TAB_NAMES = [
    "Form Responses", "Form Responses 1", "Form Responses 2", "Responses",
    "K-8 Responses (EN)", "K-8 Responses (SP)", "K-8 Responses (ENG)", "K-8 Responses (ESP)",
    "HS Responses (EN)", "HS Responses (SP)", "HS Responses (ENG)", "HS Responses (ESP)"
]


def find_relevant_tabs(tabs):
    return {tab: gid for tab, gid in tabs.items() if tab in TAB_NAMES}


if __name__ == "__main__":
    drive_service, sheets_service = authenticate_drive()

    valid_years = [
        "SY20-21 Surveys", "SY21-22 Surveys", "SY22-23 Surveys", "SY23-24 Surveys", "SY24-25 Surveys"
    ]

    year_folders = list_subfolders(drive_service, ROOT_FOLDER_ID)
    links_dict = {}

    for year_folder in year_folders:
        if year_folder['name'] not in valid_years:
            continue

        year_key = year_folder['name'].replace("SY", "").replace("-", "").replace(" Surveys", "")
        links_dict[year_key] = {"younger": {}, "older": {}}

        feedback_folders = list_subfolders(drive_service, year_folder['id'])
        student_feedback_folder = next(
            (f for f in feedback_folders if "student feedback" in f['name'].lower()), None)

        if not student_feedback_folder:
            continue

        school_folders = list_subfolders(drive_service, student_feedback_folder['id'])

        for school_folder in school_folders:
            school_name = school_folder['name']

            if any(phrase in school_name.lower() for phrase in ["unassigned forms", "sample", "sample survey"]):   
                print(f"⏩ Skipping folder '{school_name}' (Unassigned or Sample)")
                continue

            sheets = list_sheets_in_folder(drive_service, school_folder['id'])
            print(f"📁 School: {school_name} → {len(sheets)} sheet(s)")

            for sheet in sheets:
                sheet_name = sheet.get("name", "").lower()

                if "younger" in sheet_name:
                    category = "younger"
                    print(f"📘 Overriding category to 'younger' based on sheet name: {sheet['name']}")
                elif "older" in sheet_name:
                    category = "older"
                    print(f"📗 Overriding category to 'older' based on sheet name: {sheet['name']}")
                else:
                    category = categorize_school(school_name)
                    print(f"📂 Using school name categorization: {school_name} → {category}")

                try:
                    tabs = generate_sheet_tabs(sheets_service, sheet['id'])
                    print(f"🧾 Tabs in '{sheet['name']}': {list(tabs.keys())}")
                    time.sleep(2)  # 💤 stronger delay

                    relevant_tabs = find_relevant_tabs(tabs)
                    if not relevant_tabs:
                        print(f"⚠️ No matching tabs in '{sheet['name']}' — skipping")
                        continue

                    links_dict[year_key][category].setdefault(school_name, {}).update({
                        tab_name: {
                            "sheet_link": f"https://docs.google.com/spreadsheets/d/{sheet['id']}/edit#gid={gid}",
                            "sheet_id": sheet['id'],
                            "gid": gid,
                            "tab_name": tab_name
                        } for tab_name, gid in relevant_tabs.items()
                    })

                except Exception as e:
                    print(f"❌ Failed processing sheet '{sheet['id']}' due to error: {e}")

                time.sleep(2)  # 💤 again after full sheet processing

    output_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "../..", "data", "configs", "links.yaml"
    ))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as file:
        yaml.dump(links_dict, file, sort_keys=True)

    print(f"\n🎉 YAML successfully written to {output_path}")