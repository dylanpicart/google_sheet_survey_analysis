import unicodedata
import re
import pandas as pd


def normalize_column(df, variants, canonical_name):
    """
    Rename a column in df from any variant name to canonical_name.
    Adds the column if not present.
    """
    col = next((c for c in df.columns if c.strip().lower() in [v.lower() for v in variants]), None)
    if col:
        df = df.rename(columns={col: canonical_name})
    if canonical_name not in df.columns:
        df[canonical_name] = ""
    return df


def normalize_text(s):
    """
    Robust text normalization: handles None/NaN, strips, lowercases,
    removes Unicode/emoji symbols, collapses whitespace.
    """
    if pd.isnull(s):
        return ""
    s = str(s)
    # Remove emoji/unicode symbols
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.category(c).startswith("So"))
    s = s.lower().strip()
    # Collapse multiple spaces to one
    s = re.sub(r"\s+", " ", s)
    return s
