import pandas as pd
import glob
import os
import re
from utils import setup_logging

logger = setup_logging("load")


def extract_year_and_group(filename):
    m = re.search(r"sy(\d{2}-\d{2})_(OLDER|YOUNGER)", filename, re.I)
    if m:
        year = m.group(1)
        group = m.group(2).capitalize()
        return year, group
    return "Unknown", "Unknown"


def write_master_excel(
    output_master,
    master_totals_path,
    older_summary_path,
    younger_summary_path,
    responses_dirs,  # e.g., {"younger": "...", "older": "..."}
):
    with pd.ExcelWriter(output_master, engine="xlsxwriter") as writer:
        # 1. Master Summary
        if os.path.exists(master_totals_path):
            df = pd.read_csv(master_totals_path)
            df.to_excel(writer, sheet_name="Master Summary", index=False)
            logger.info(f"Added Master Summary from {master_totals_path}")
        else:
            logger.warning(f"Master totals file not found: {master_totals_path}")

        # 2. Older/Younger Summary
        for csv_path, sheet_name in [
            (older_summary_path, "Older Summary"),
            (younger_summary_path, "Younger Summary"),
        ]:
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path)
                df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
                logger.info(f"Added {sheet_name} from {csv_path}")
            else:
                logger.warning(f"{sheet_name} file not found: {csv_path}")

        # 3. All Responses as SY {year} {Group} Responses
        for group, data_dir in responses_dirs.items():
            csvs = sorted(glob.glob(os.path.join(data_dir, "*.csv")))
            for csv_path in csvs:
                fname = os.path.basename(csv_path)
                year, grp = extract_year_and_group(fname)
                if year != "Unknown" and grp != "Unknown":
                    sheet = f"SY {year} {grp} Responses"[:31]
                    df = pd.read_csv(csv_path)
                    df.to_excel(writer, sheet_name=sheet, index=False)
                    logger.info(f"Added responses: {sheet} from {csv_path}")

    logger.info(f"Saved SF_Master_Summary Excel to: {output_master}")


def main():
    output_master = "data/processed/SF_Master_Summary.xlsx"
    master_totals_path = "data/processed/canonical_question_totals.csv"
    older_summary_path = "data/processed/consolidated_questions_older.csv"
    younger_summary_path = "data/processed/consolidated_questions_younger.csv"
    responses_dirs = {"younger": "data/processed/younger", "older": "data/processed/older"}
    write_master_excel(
        output_master=output_master,
        master_totals_path=master_totals_path,
        older_summary_path=older_summary_path,
        younger_summary_path=younger_summary_path,
        responses_dirs=responses_dirs,
    )


if __name__ == "__main__":
    main()
