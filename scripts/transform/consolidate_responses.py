import pandas as pd
import os
import unicodedata
import re
from summary_tables import SCALE_ORDERS
from utils import normalize_text


def get_summary_col_mapping(scale_orders):
    summary_map = {}

    # Frequency mapping (all keys and their values, plus new variants)
    frequency_map = {
        "All the time": ["Very Frequently (every day or almost every day)", "All the time"],
        "A lot of the time": ["Frequently (several times a week)", "A lot of the time", "A lot"],
        "Sometimes": [" Rarely (less than once a week) ", "Occasionally (around once a week)", "Sometimes", "A little"],
        "Not at all": ["Not at All", "Not at all"]
    }
    for bucket, variants in frequency_map.items():
        for v in variants:
            summary_map[normalize_text(v)] = bucket

    # Likert 3-bucket mapping
    disagree_keys = [
        "Strongly Disagree", "Disagree", "Disagree a lot", "Disagree a little"
    ]
    neither_keys = [
        "Neither Agree nor Disagree", "Neither", "No change was needed", "Neither Agree Nor Disgree"
    ]
    agree_keys = [
        "Agree", "Agree some of the time", "Agree a lot", "Strongly Agree"
    ]
    for scale in scale_orders:
        for v in scale_orders[scale]:
            nv = normalize_text(v)
            if v in disagree_keys:
                summary_map[nv] = "Disagree"
            elif v in neither_keys:
                summary_map[nv] = "Neither Agree Nor Disagree"
            elif v in agree_keys:
                summary_map[nv] = "Agree"
            elif scale.startswith("yes_no_maybe"):
                if nv in ["yes", "y", "sí", "si", "yes, i felt happier"]:
                    summary_map[nv] = "Yes"
                elif nv in ["no", "no, i felt the same"]:
                    summary_map[nv] = "No"
                elif nv in ["maybe", "tal vez", "perhaps"]:
                    summary_map[nv] = "Maybe"
    return summary_map


SUMMARY_MAP = get_summary_col_mapping(SCALE_ORDERS)

canon_to_over_df = pd.read_csv("data/processed/audit/canonical_to_raw_overarching.csv")
canon_to_over_map = dict(zip(
    canon_to_over_df["Canonical Question"].str.strip().str.lower(),
    canon_to_over_df["Overarching"].str.strip().str.lower(),
))

def consolidate_summary(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    question_col = df.columns[0]

    # Find which columns to sum into which bucket
    columns = list(df.columns)
    bucket_to_cols = {}
    for col in columns:
        if col == question_col: continue
        mapped = SUMMARY_MAP.get(norm(col), None)
        if mapped:
            bucket_to_cols.setdefault(mapped, []).append(col)

    buckets = list(bucket_to_cols.keys())

    # Desired output order
    desired_order = [
        "All the time", "A lot of the time", "Sometimes", "Not at all",
        "Agree", "Neither Agree Nor Disagree", "Disagree", "Yes", "Maybe", "No"
    ]
    # Only include buckets present in this summary
    output_order = ["Column"] + [c for c in desired_order if c in buckets]

    # Build all rows
    rows = []
    for i, row in df.iterrows():
        new_row = {"Column": row[question_col]}
        for bucket in buckets:
            val = 0
            for vcol in bucket_to_cols[bucket]:
                if vcol in row:
                    try:
                        val += float(row[vcol])
                    except (ValueError, KeyError, TypeError):
                        pass
            new_row[bucket] = int(val)
        rows.append(new_row)

    consolidated = pd.DataFrame(rows)
    consolidated = consolidated.reindex(columns=output_order)

    # Add overarching question column
    consolidated["Normalized Canonical"] = consolidated["Column"].str.strip().str.lower()
    consolidated["Overarching"] = consolidated["Normalized Canonical"].map(canon_to_over_map)
    consolidated.drop(columns=["Normalized Canonical"], inplace=True)


    # Save
    consolidated.to_csv(output_csv, index=False)
    print(f"Saved consolidated summary: {output_csv}")


def batch_consolidate_summary(summary_dir):
    summary_files = [f for f in os.listdir(summary_dir) if f.endswith(".csv")]
    outdir = os.path.join(summary_dir, "cons_resp")
    os.makedirs(outdir, exist_ok=True)
    for f in summary_files:
        infile = os.path.join(summary_dir, f)
        outfile = os.path.join(outdir, f.replace("_summary", "_consolidated_summary"))
        consolidate_summary(infile, outfile)

if __name__ == "__main__":
    batch_consolidate_summary("data/processed/younger/summary")
    batch_consolidate_summary("data/processed/older/summary")
