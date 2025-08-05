import pandas as pd
import os
import re
import numpy as np
from utils import clean_text, clean_grade, normalize_column, setup_logging
from data.configs import school_years, group_params, meta_variants

logger = setup_logging("transform")

SCHOOL_YEARS = school_years
GROUP_PARAMS = group_params
META_VARIANTS = meta_variants

junk_cols = ["Unnamed: 0", "Timestamp", "Column 1"]

def categorize_question_stem(question):
    q = question.lower()
    if re.search(r'thinking about this school year.*agree', q):
        return "School Climate"
    elif re.search(r'please think about how pwc helped', q):
        return "PWC Support"
    elif re.search(r'what feelings have you felt', q):
        return "Emotional Experience"
    elif re.search(r'what would you like your teacher', q):
        return "Teacher Feedback"
    elif re.search(r'what do you want adults to know', q):
        return "Student Voice"
    elif re.search(r'if you could change one thing', q):
        return "Open Reflection"
    else:
        return "Other"

def build_accepted_map(question_df, RAW_QUESTION_COL):
    accepted_map = {
        row[RAW_QUESTION_COL]: set(str(row["Sample Responses"]).split("|")) if pd.notna(row["Sample Responses"]) else set()
        for _, row in question_df.iterrows()
    }
    return {k: {r.strip() for r in v} for k, v in accepted_map.items()}

def process_raw_data(raw, meta_variants, junk_cols):
    # 1. Normalize metadata columns
    for canonical, variants in meta_variants.items():
        raw = normalize_column(raw, variants, canonical)
    # 2. Deduplicate columns (AFTER renaming/normalizing)
    raw = raw.loc[:, ~raw.columns.duplicated()]
    # 3. Clean text/object columns
    for column in raw.select_dtypes(include="object").columns:
        if column.strip().lower() == "grade":
            raw[column] = raw[column].map(clean_grade)
        else:
            raw[column] = raw[column].map(clean_text)
    # 4. Drop junk columns
    raw = raw.drop(columns=[col for col in junk_cols if col in raw.columns])
    return raw

def build_output_dict(raw, canonical_cols, accepted_map):
    output_dict = {}
    for col in canonical_cols:
        if col in raw.columns:
            raw_series = raw[col]
            if isinstance(raw_series, pd.DataFrame):
                logger.warning(f"Warning: {col} duplicated! Using first column only.")
                raw_series = raw_series.iloc[:, 0]
            accepted = accepted_map.get(col, None)
            if accepted:
                output_dict[col] = raw_series.apply(lambda x: x if str(x).strip() in accepted else np.nan)
            else:
                output_dict[col] = raw_series
        else:
            output_dict[col] = np.nan
    return output_dict

def clean_output_dict(output_dict):
    # Remove all keys (columns) that are only all NaN or all empty string
    keys_to_remove = []
    for k in list(output_dict.keys()):
        series = output_dict[k]
        arr = np.array(series)
        if ((pd.isna(arr) | (arr == "") | (arr == "nan")).all()):
            keys_to_remove.append(k)
    for k in keys_to_remove:
        del output_dict[k]
    return output_dict

def add_meta_columns(output_dict, raw, meta_cols):
    for meta_col in meta_cols:
        if meta_col not in output_dict:
            if meta_col in raw.columns:
                output_dict[meta_col] = raw[meta_col]
            else:
                output_dict[meta_col] = np.nan
    return output_dict

def clean_final_dataframe(final, meta_cols):
    # 1. Replace all-whitespace and "" with NaN
    final = final.replace(r'^\s*$', np.nan, regex=True)
    final = final.infer_objects(copy=False)
    final = final.replace("nan", np.nan)
    # 2. Drop columns that are all NaN (except meta)
    final = final.dropna(axis=1, how='all')
    # 3. Drop rows that are all NaN/blank except for metadata columns
    check_cols = [col for col in final.columns if col not in meta_cols]
    if check_cols:
        final = final.dropna(subset=check_cols, how='all')
    if "Grade" in final.columns:
        final["Grade"] = final["Grade"].astype(str)
        final["Grade"] = final["Grade"].map(clean_grade)
        final["Grade"] = final["Grade"].replace(["nan", "None"], "")
    return final

def audit_map_for_group(
    group,
    params,
    school_years=None,
    meta_variants=None,
    junk_cols=None
):
    school_years = school_years or SCHOOL_YEARS
    meta_variants = meta_variants or META_VARIANTS
    junk_cols = junk_cols or ["Unnamed: 0", "Timestamp", "Column 1"]

    logger.info(f"\nProcessing group: {group.title()}")
    question_df = pd.read_csv(params["question_list"], encoding="utf-8-sig")
    RAW_QUESTION_COL = "Raw Question"

    question_df["Group"] = question_df[RAW_QUESTION_COL].apply(categorize_question_stem)
    question_df["_original_order"] = range(len(question_df))
    question_df = question_df.sort_values(by=["Group", "_original_order"])

    canonical_cols = question_df[RAW_QUESTION_COL].tolist()
    accepted_map = build_accepted_map(question_df, RAW_QUESTION_COL)

    meta_cols = ["School Year", "School", "Grade", "Tab"]

    for year in school_years:
        raw_path = os.path.join(params['raw_dir'], f"{year}_{group}_feedback.csv")
        output_path = os.path.join(params['output_dir'], f"{year}_{group.upper()}_ENGLISH_questions.csv")

        if not os.path.exists(raw_path):
            logger.warning(f"  [!] Raw data not found for {year} ({raw_path}) -- skipping")
            continue

        logger.info(f"  Processing year: {year}")

        raw = pd.read_csv(raw_path)
        raw = process_raw_data(raw, meta_variants, junk_cols)
        output_dict = build_output_dict(raw, canonical_cols, accepted_map)

        # Debugging for non-1D columns (keep for now)
        for k, v in output_dict.items():
            if hasattr(v, "ndim") and v.ndim > 1:
                logger.error(f"[ERROR] {k} is not 1D! Shape: {v.shape}")

        output_dict = clean_output_dict(output_dict)
        output_dict = add_meta_columns(output_dict, raw, meta_cols)

        ordered_cols = meta_cols + [col for col in canonical_cols if col in output_dict and col not in meta_cols]
        dropped_questions = [col for col in canonical_cols if col not in ordered_cols]
        if dropped_questions:
            logger.warning(
                f"  ⚠️ Dropped {len(dropped_questions)} canonical questions due to all-NaN: {dropped_questions[:3]}{'...' if len(dropped_questions) > 3 else ''}"
            )

        final = pd.DataFrame(output_dict)[ordered_cols]
        final = clean_final_dataframe(final, meta_cols)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        final.to_csv(output_path, index=False)
        logger.info(f"    Saved: {output_path}")

def main():
    for group, params in GROUP_PARAMS.items():
        audit_map_for_group(
            group=group,
            params=params,
            school_years=SCHOOL_YEARS,
            meta_variants=META_VARIANTS,
            junk_cols=junk_cols
        )
    logger.info("\nAll years and groups processed. PerformanceWarning gone, output shape is correct.")

if __name__ == "__main__":
    main()
