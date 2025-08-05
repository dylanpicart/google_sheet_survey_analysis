import pandas as pd
import glob
from collections import defaultdict
from utils import clean_text, clean_grade
from data.configs import (
    YOUNGER_QUESTION_MAPPING,
    OLDER_QUESTION_MAPPING,
    build_lookup,
    audit_and_clean_columns,
)

def audit_questions_and_write_csv(mapping, mapping_name, csv_paths, output_csv, output_excel):
    lookup = build_lookup(mapping)
    question_cleaned_samples = defaultdict(set)
    question_raw_samples = defaultdict(set)

    GRADE_COLS = ["grade", "grado"]  # Add more grade column names as needed

    for path in csv_paths:
        df = pd.read_csv(path)
        for col in df.columns:

            # Only standardize for grade columns (case-insensitive match)
            if col.strip().lower() in GRADE_COLS:
                raw_samples = [clean_grade(s) for s in df[col].dropna().unique()]
                raw_samples_nonblank = [s for s in raw_samples if s and s.strip() != ""]
            else:
                # For all other columns, use raw string samples as-is
                raw_samples = [str(s) for s in df[col].dropna().unique()]
                raw_samples_nonblank = [s for s in raw_samples if s and s.strip() != ""]

            cleaned_samples = [clean_text(s) for s in raw_samples_nonblank]
            cleaned_samples_nonblank = [s for s in cleaned_samples if s.strip() != ""]
            if cleaned_samples_nonblank:
                question_cleaned_samples[col].update(cleaned_samples_nonblank)
                question_raw_samples[col].update(raw_samples_nonblank)

    questions = list(question_cleaned_samples.keys())
    audit = audit_and_clean_columns(questions, lookup)

    output_rows = []
    for q in questions:
        samples_str = " | ".join(map(str, question_cleaned_samples[q]))
        res = audit[q]
        if res["canonical"]:
            output_rows.append([
                q,
                res["canonical"],
                res["reason"],
                samples_str
            ])
        else:
            suggestions = "; ".join([f"{sug} ({score:.0f}%)" for sug, score in res["suggestions"]]) if res["suggestions"] else "No good suggestions"
            output_rows.append([
                q,
                "",
                suggestions,
                samples_str
            ])
    # Convert to DataFrame
    df_out = pd.DataFrame(output_rows, columns=[
        "Raw Question", "Canonical Mapping", "Reason/Suggestions", "Sample Responses"
    ])

    def has_real_sample(sample_str):
        # Checks for any non-empty (non-whitespace) sample in the '|' separated list
        return any(s.strip() != "" for s in str(sample_str).split("|"))

    df_out_filtered = df_out[df_out["Sample Responses"].apply(has_real_sample)].copy()

    # Overwrite CSV/Excel with filtered rows only
    df_out_filtered.to_csv(output_csv, index=False)
    df_out_filtered.to_excel(output_excel, index=False)
    print(f"{mapping_name} audit complete. Output written to {output_csv} and {output_excel}.")

# Paths for older and younger CSVs
younger_csv_paths = glob.glob("data/raw/younger/*.csv", recursive=True)
older_csv_paths   = glob.glob("data/raw/older/*.csv", recursive=True)

audit_questions_and_write_csv(
    YOUNGER_QUESTION_MAPPING,
    "Younger",
    younger_csv_paths,
    "data/processed/audit/question_samples_audit_younger.csv",
    "data/processed/audit/question_samples_audit_younger.xlsx"
)
audit_questions_and_write_csv(
    OLDER_QUESTION_MAPPING,
    "Older",
    older_csv_paths,
    "data/processed/audit/question_samples_audit_older.csv",
    "data/processed/audit/question_samples_audit_older.xlsx"
)
