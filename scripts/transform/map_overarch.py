import pandas as pd
import re
import unicodedata

# --- File paths ---
summary_younger = "data/processed/consolidated_questions_younger.csv"
summary_older = "data/processed/consolidated_questions_older.csv"
audit_younger = "data/processed/audit/question_samples_audit_younger.csv"
audit_older = "data/processed/audit/question_samples_audit_older.csv"
output_file = "data/processed/audit/canonical_to_raw_overarching.csv"

def normalize(text):
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\xa0", " ").lower().strip()
    text = re.sub(r"\s+", " ", text)
    text = text.replace("’", "'").replace("“", '"').replace("”", '"')
    return text

def extract_bracketed(text):
    match = re.search(r"\[(.*?)\]", str(text))
    return normalize(match.group(1)) if match else None

def extract_overarching(text):
    match = re.split(r"\[.*?\]", str(text))
    return normalize(match[0]) if match else normalize(text)

def build_canonical_to_overarching(audit_df):
    audit_df["Canonical_Extracted"] = audit_df["Raw Question"].apply(extract_bracketed)
    audit_df["Overarching"] = audit_df["Raw Question"].apply(extract_overarching)
    canon_to_over = {}
    for _, row in audit_df.iterrows():
        if row["Canonical_Extracted"]:
            canon_to_over[row["Canonical_Extracted"]] = row["Overarching"]
        else:
            # Map the whole normalized question if there are no brackets (top-level question)
            canon_to_over[normalize(row["Raw Question"])] = normalize(row["Raw Question"])
    return canon_to_over


def add_overarching(summary_csv, canonical_to_overarching_map):
    df = pd.read_csv(summary_csv)
    canonical_col = None
    for col in df.columns:
        if col.strip().lower() == "canonical question":
            canonical_col = col
            break
        if col.strip().lower() == "column":
            canonical_col = col
    if canonical_col is None:
        canonical_col = df.columns[0]
    df["Normalized Canonical"] = df[canonical_col].apply(normalize)
    df["Overarching"] = df["Normalized Canonical"].map(canonical_to_overarching_map)
    # Fallback: if still missing, map to self (question is both sub and overarching)
    df.loc[df["Overarching"].isnull(), "Overarching"] = df.loc[df["Overarching"].isnull(), "Normalized Canonical"]
    out = df[[canonical_col, "Overarching"]].drop_duplicates()
    out = out.rename(columns={canonical_col: "Canonical Question"})
    return out


audit_y = pd.read_csv(audit_younger)
audit_o = pd.read_csv(audit_older)

# Build and merge the mappings from both audits
overarching_younger = build_canonical_to_overarching(audit_y)
overarching_older = build_canonical_to_overarching(audit_o)

# Merge, with older values winning if there is overlap
canon_to_overarching = {**overarching_younger, **overarching_older}

younger_map = add_overarching(summary_younger, canon_to_overarching)
older_map = add_overarching(summary_older, canon_to_overarching)

# Combine, drop duplicates
all_qs = pd.concat([younger_map, older_map], ignore_index=True)
all_qs = all_qs.drop_duplicates(subset=["Canonical Question", "Overarching"])
missing = all_qs[all_qs["Overarching"].isnull()]
print("Canonical questions missing an Overarching match:")
print(missing)
print("Total missing:", missing.shape[0])

all_qs.to_csv(output_file, index=False)
print(f"Saved mapping to: {output_file}")
print(all_qs.head(10))
