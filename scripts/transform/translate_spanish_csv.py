import pandas as pd
import os
from data.configs import EN_SP_MAPPING, ANSWER_MAPPING, cols_to_drop
from utils import normalize_text

def build_reverse_mapping(mapping, normalize_text):
    """Builds mapping from normalized Spanish to English."""
    return {normalize_text(v): k for k, v in mapping.items()}

def build_normalized_answer_mapping(mapping, normalize_text):
    """Builds mapping from normalized Spanish answer to English."""
    return {normalize_text(k): v for k, v in mapping.items()}

def find_spanish_columns(df, reverse_mapping, normalize_text):
    return [col for col in df.columns if normalize_text(col) in reverse_mapping]

def build_spanish_to_english(spanish_cols, reverse_mapping, normalize_text):
    return {col: reverse_mapping.get(normalize_text(col), col) for col in spanish_cols}

def translate_column_answers(df, answer_mapping, normalize_text):
    for col in df.columns:
        df[col] = df[col].map(lambda cell: answer_mapping.get(normalize_text(cell), cell))
    return df

def drop_normalized_columns(df, cols_to_drop, normalize_text):
    norm_to_real = {normalize_text(col): col for col in df.columns}
    for col in cols_to_drop:
        ncol = normalize_text(col)
        if ncol in norm_to_real:
            df = df.drop(columns=[norm_to_real[ncol]])
    return df

def merge_translations_into_main(df, df_translated, spanish_to_english, normalize_text):
    main_norm = {normalize_text(c): c for c in df.columns}
    for sp_col, en_col in spanish_to_english.items():
        trans_norm = normalize_text(en_col)
        if trans_norm in main_norm and en_col in df_translated.columns:
            real_en_col = main_norm[trans_norm]
            mask = df[real_en_col].isna() | (df[real_en_col].astype(str).str.strip() == "")
            fill_vals = df_translated[en_col].where(
                ~df_translated[en_col].isna() & (df_translated[en_col].astype(str).str.strip() != ""))
            df[real_en_col] = df[real_en_col].astype("string")
            df.loc[mask, real_en_col] = fill_vals[mask].astype("string")
        elif en_col in df_translated.columns:
            df[en_col] = df_translated[en_col]
    return df

def process_csv_file(
    infile, out_translated, out_main,
    EN_SP_MAPPING=None,
    ANSWER_MAPPING=None,
    cols_to_drop=None,
    normalize_text=None
):
    # Use real configs if not injected
    if EN_SP_MAPPING is None:
        from data.configs import EN_SP_MAPPING as REAL_EN_SP_MAPPING
        EN_SP_MAPPING = REAL_EN_SP_MAPPING
    if ANSWER_MAPPING is None:
        from data.configs import ANSWER_MAPPING as REAL_ANSWER_MAPPING
        ANSWER_MAPPING = REAL_ANSWER_MAPPING
    if cols_to_drop is None:
        from data.configs import cols_to_drop as REAL_cols_to_drop
        cols_to_drop = REAL_cols_to_drop
    if normalize_text is None:
        from utils import normalize_text as REAL_normalize_text
        normalize_text = REAL_normalize_text


    reverse_mapping = build_reverse_mapping(EN_SP_MAPPING, normalize_text)
    answer_mapping = build_normalized_answer_mapping(ANSWER_MAPPING, normalize_text)

    df = pd.read_csv(infile)
    spanish_cols = find_spanish_columns(df, reverse_mapping, normalize_text)
    if not spanish_cols:
        print(f"No Spanish columns found in {infile}")
        return

    spanish_to_english = build_spanish_to_english(spanish_cols, reverse_mapping, normalize_text)

    # Translate Spanish columns (header + answers)
    df_spanish = df[spanish_cols].copy()
    df_translated = df_spanish.rename(columns=spanish_to_english)
    df_translated = translate_column_answers(df_translated, answer_mapping, normalize_text)
    df_translated.to_csv(out_translated, index=False)
    print(f"Saved translated columns: {out_translated}")

    df = merge_translations_into_main(df, df_translated, spanish_to_english, normalize_text)
    df = df.drop(columns=spanish_cols, errors='ignore')
    df = drop_normalized_columns(df, cols_to_drop, normalize_text)
    df.to_csv(out_main, index=False)
    print(f"Saved main file with Spanish columns replaced: {out_main}")

def batch_translate_dir(in_dir):
    for file in os.listdir(in_dir):
        if file.endswith(".csv") and "SPANISH" not in file and "translated" not in file and "ENONLY" not in file:
            infile = os.path.join(in_dir, file)
            out_translated = os.path.join(in_dir, f"translated_only_{file}")
            out_main = os.path.join(in_dir, f"ENONLY_{file}")
            process_csv_file(infile, out_translated, out_main)

def main():
    batch_translate_dir("data/processed/younger")

if __name__ == "__main__":
    main()
