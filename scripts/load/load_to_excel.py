import pandas as pd
import glob
import os
import re

def extract_year_and_group(filename):
    m = re.search(r"sy(\d{2}-\d{2})_(OLDER|YOUNGER)", filename, re.I)
    if m:
        year = m.group(1)
        group = m.group(2).capitalize()
        return year, group
    return "Unknown", "Unknown"

output_master = "data/processed/SF_Master_Summary.xlsx"
with pd.ExcelWriter(output_master, engine='xlsxwriter') as writer:
    # 1. Master Summary
    master_totals_path = "data/processed/canonical_question_totals.csv"
    if os.path.exists(master_totals_path):
        df = pd.read_csv(master_totals_path)
        df.to_excel(writer, sheet_name="Master Summary", index=False)

    # 2. Older/Younger Summary
    for csv_path, sheet_name in [
        ("data/processed/consolidated_questions_older.csv", "Older Summary"),
        ("data/processed/consolidated_questions_younger.csv", "Younger Summary"),
    ]:
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            df.to_excel(writer, sheet_name=sheet_name[:31], index=False)

    # 3. All Responses as SY {year} {Group} Responses
    for group in ["younger", "older"]:
        data_dir = f"data/processed/{group}"
        csvs = sorted(glob.glob(os.path.join(data_dir, "*.csv")))
        for csv_path in csvs:
            fname = os.path.basename(csv_path)
            year, grp = extract_year_and_group(fname)
            # Only add tabs for files matching "sy??-??" pattern
            if year != "Unknown" and grp != "Unknown":
                sheet = f"SY {year} {grp} Responses"[:31]
                df = pd.read_csv(csv_path)
                df.to_excel(writer, sheet_name=sheet, index=False)

print(f"Saved SF_Master_Summary Excel to: {output_master}")
