import pandas as pd
import os
import sys
import unicodedata
import re

# Import mappings
from data.configs import EN_SP_MAPPING, ANSWER_MAPPING, cols_to_drop
from utils import normalize_text

def build_reverse_normalized_mapping(mapping):
    return {normalize_text(v): k for k, v in mapping.items()}

def build_normalized_answer_mapping(mapping):
    return {normalize_text(k): v for k, v in mapping.items()}

REVERSE_EN_SP_MAPPING = build_reverse_normalized_mapping(EN_SP_MAPPING)
NORMALIZED_ANSWER_MAPPINGS = build_normalized_answer_mapping(ANSWER_MAPPING)

def translate_column_header(col):
    norm_col = normalize_text(col)
    return REVERSE_EN_SP_MAPPING.get(norm_col, col)

def translate_cell(cell):
    norm_cell = normalize_text(cell)
    return NORMALIZED_ANSWER_MAPPINGS.get(norm_cell, cell)

def drop_columns_by_normalized_match(df, cols_to_drop):
    norm_to_real = {normalize_text(col): col for col in df.columns}
    for col in cols_to_drop:
        ncol = normalize_text(col)
        if ncol in norm_to_real:
            df = df.drop(columns=[norm_to_real[ncol]])
    return df

def process_csv_file(infile, out_translated, out_main):
    df = pd.read_csv(infile)
    # Identify Spanish columns using mapping
    spanish_cols = [col for col in df.columns if normalize_text(col) in REVERSE_EN_SP_MAPPING]
    if not spanish_cols:
        print(f"No Spanish columns found in {infile}")
        return
    # For each Spanish column, get its mapped English column
    spanish_to_english = {col: translate_column_header(col) for col in spanish_cols}

    # Translate Spanish columns (header + answers)
    df_spanish = df[spanish_cols].copy()
    df_translated = df_spanish.rename(columns=spanish_to_english)
    for col in df_translated.columns:
        df_translated[col] = df_translated[col].map(translate_cell)
    df_translated.to_csv(out_translated, index=False)
    print(f"Saved translated columns: {out_translated}")

    # --- Robust transplant logic ---
    main_norm = {normalize_text(c): c for c in df.columns}

    for sp_col, en_col in spanish_to_english.items():
        trans_norm = normalize_text(en_col)
        if trans_norm in main_norm and en_col in df_translated.columns:
            real_en_col = main_norm[trans_norm]
            mask = df[real_en_col].isna() | (df[real_en_col].astype(str).str.strip() == "")
            fill_vals = df_translated[en_col].where(
                ~df_translated[en_col].isna() & (df_translated[en_col].astype(str).str.strip() != ""))
            df.loc[mask, real_en_col] = fill_vals[mask]
        elif en_col in df_translated.columns:
            df[en_col] = df_translated[en_col]

    # Drop the Spanish columns (errors='ignore' for safety)
    df = df.drop(columns=spanish_cols, errors='ignore')

    # --- Drop any remaining unwanted Spanish columns by normalized matching ---
    COLS_TO_DROP = cols_to_drop
    df = drop_columns_by_normalized_match(df, COLS_TO_DROP)

    df.to_csv(out_main, index=False)
    print(f"Saved main file with Spanish columns replaced: {out_main}")

def main():
    in_dir = "data/processed/younger"
    for file in os.listdir(in_dir):
        if file.endswith(".csv") and "SPANISH" not in file and "translated" not in file and "ENONLY" not in file:
            infile = os.path.join(in_dir, file)
            out_translated = os.path.join(in_dir, f"translated_only_{file}")
            out_main = os.path.join(in_dir, f"ENONLY_{file}")
            process_csv_file(infile, out_translated, out_main)

if __name__ == "__main__":
    main()
