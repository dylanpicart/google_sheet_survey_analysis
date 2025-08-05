import pandas as pd
import re
import glob
import os
from data.configs import SCALE_ORDERS
from utils import setup_logging

logger = setup_logging("transform")

def simplify_column(col):
    match = re.search(r'\[(.*?)\]', col)
    return match.group(1) if match else col

def normalize(val):
    if pd.isnull(val):
        return val
    return str(val).strip().lower()

def best_scale_match(observed_responses, scale_orders, threshold=0.6):
    observed_norm = set(normalize(x) for x in observed_responses if pd.notnull(x))
    best_key = None
    best_score = 0
    for key, order in scale_orders.items():
        order_norm = [normalize(x) for x in order]
        order_set = set(order_norm)
        # Score: % of observed responses found in this scale order (Jaccard similarity)
        n_found = len(observed_norm & order_set)
        n_total = len(observed_norm | order_set)
        if n_total == 0:
            continue
        score = n_found / n_total
        if score > best_score:
            best_key = key
            best_score = score
    if best_score >= threshold:
        return best_key, scale_orders[best_key]
    return None, None

def value_count_table(df, columns, as_percent=False, round_to=1, scale_orders=None):
    if scale_orders is None:
        scale_orders = SCALE_ORDERS
    if isinstance(columns, str):
        columns = [columns]
    all_summaries = []
    for col in columns:
        # Normalize responses for matching
        values = df[col].dropna().map(normalize).unique()
        scale_key, order = best_scale_match(values, scale_orders)
        # If no good match, just use sorted observed values (original, not normalized)
        if order is None:
            order = sorted(df[col].dropna().unique(), key=lambda x: str(x))
        # Count responses, preserve original capitalization/format in output
        vc = df[col].value_counts().reindex(order, fill_value=0)
        if as_percent:
            vc = (vc / vc.sum() * 100).round(round_to)
        vc.name = col
        all_summaries.append(vc)
    summary_df = pd.DataFrame(all_summaries).fillna(0)
    summary_df.index.name = "Question"
    summary_df.reset_index(inplace=True)

    # Drop columns (except "Question") where all values are 0
    non_question_cols = summary_df.columns.difference(["Question"])
    summary_df = summary_df.loc[:, ["Question"] + [col for col in non_question_cols if summary_df[col].sum() > 0]]

    # Cast all columns except "Question" to int, if not as_percent
    if not as_percent:
        for col in summary_df.columns:
            if col != "Question":
                summary_df[col] = summary_df[col].astype(int)

    return summary_df

def process_all_summaries(folders=None, scale_orders=None):
    folders = folders or {
        "younger": "data/processed/younger/",
        "older": "data/processed/older/"
    }
    scale_orders = scale_orders or SCALE_ORDERS

    for group, folder in folders.items():
        logger.info(f"\n=== Checking group: {group} ===")
        logger.info(f"Folder: {folder}")
        files_found = glob.glob(os.path.join(folder, '*.csv'))
        logger.info(f"Files found: {files_found}")

        summary_dir = os.path.join(folder, "summary")
        os.makedirs(summary_dir, exist_ok=True)
        csv_paths = glob.glob(os.path.join(folder, "*.csv"))

        for path in csv_paths:
            base = os.path.splitext(os.path.basename(path))[0]
            out_csv = os.path.join(summary_dir, f"{base}_summary.csv")
            if os.path.basename(path).startswith("summary"):
                logger.info(f"  Skipping {path} (is a summary file)")
                continue
            logger.info(f"  Processing {path}")
            df = pd.read_csv(path)
            df_simplified = df.copy()
            df_simplified.columns = [simplify_column(c) for c in df_simplified.columns]
            meta_cols = ["School Year", "School", "Grade", "Tab"]
            question_cols = [c for c in df_simplified.columns if c not in meta_cols]
            logger.info(f"    Question columns: {question_cols}")
            if not question_cols:
                logger.warning("    No question columns found. Skipping.")
                continue
            summary = value_count_table(df_simplified, question_cols, scale_orders=scale_orders)
            summary.to_csv(out_csv, index=False)
            logger.info(f"    Saved summary to {out_csv}\n")

if __name__ == "__main__":
    process_all_summaries()
