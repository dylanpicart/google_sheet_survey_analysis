import re
import numpy as np
import pandas as pd

def remove_emojis(text):
    if not isinstance(text, str):
        return text
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002700-\U000027BF"  # Dingbats
        "\U000024C2-\U0001F251"  # Enclosed characters
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

def is_sample_or_metadata(text):
    if not isinstance(text, str):
        return False
    # Add more "junk" or "metadata" patterns as needed
    patterns = [
        r"\bsample\b",
        r"dhdhdghd",
        r"asdasd",
        r"\bfake\b",
        r"\btest\b"
    ]
    text_lower = text.lower()
    for pattern in patterns:
        if re.search(pattern, text_lower):
            return True
    return False

def clean_text(text):
    """Cleans emojis and sample/metadata patterns, robust to NaN and non-strings."""
    if not isinstance(text, str):
        if pd.isna(text):
            return np.nan  # preserve NaN if that's what you want
        return ""         # for floats/ints/None, treat as blank string

    text = remove_emojis(text)
    if is_sample_or_metadata(text):
        return ""  # or np.nan, or "REMOVED"
    return text.strip()

def clean_grade(val):
    val = str(val).strip().upper()
    val = re.sub(r"\s+", "", val)  # Remove all spaces
    if val in {"K", "KINDERGARTEN"}:
        return "K"
    if val in {"PK", "PRE-K", "PREK", "PREKINDERGARTEN"}:
        return "PK"
    # If val is a digit (or a decimal like "1.0"), keep as number (as string)
    if val.replace(".", "", 1).isdigit():
        return str(int(float(val))) if "." in val else val
    if val and val not in {"", "NAN", "NONE", "NULL"}:
        return val
    return ""
