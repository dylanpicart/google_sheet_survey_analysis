import pandas as pd
import os
from data.configs.question_mappings import QCON_MAP, RESCON_MAPPING

def standardize_df(df, year):
    df.rename(columns=lambda x: x.strip(), inplace=True)
    df['Canonical Question'] = df['Column'].map(QCON_MAP).fillna(df['Column'])
    value_cols = [col for col in df.columns if col != 'Column']
    col_map = {col: RESCON_MAPPING.get(col, col) for col in value_cols}
    df = df.rename(columns=col_map)

    # --- DEBUG INJECTION ---
    #if year == "20-21":
        # print("\n[DEBUG] 20-21 AFTER MAPPING, BEFORE GROUPBY")
        # print("Columns:", df.columns.tolist())
        #if "Maybe" in df.columns:
        #    print("Nonzero 'Maybe' rows:")
        #    print(df[df["Maybe"] != 0][["Column", "Maybe"]])
        #if "Neither Agree Nor Disagree" in df.columns:
        #    print("Nonzero 'Neither Agree Nor Disagree' rows:")
        #    print(df[df["Neither Agree Nor Disagree"] != 0][["Column", "Neither Agree Nor Disagree"]])
    # --- END DEBUG ---

    df = df.groupby('Canonical Question', as_index=False).sum(numeric_only=True)

    # --- DEBUG INJECTION ---
    #if year == "20-21":
        #print("\n[DEBUG] 20-21 AFTER GROUPBY")
        #print("Columns:", df.columns.tolist())
        #if "Maybe" in df.columns:
        #    print("Nonzero 'Maybe' rows after grouping:")
        #    print(df[df["Maybe"] != 0][["Canonical Question", "Maybe"]])
    # --- END DEBUG ---

    df['School Year'] = year
    response_cols = [col for col in df.columns if col not in ["Canonical Question", "School Year"]]
    return df[['School Year', 'Canonical Question'] + response_cols]

canon_to_over_df = pd.read_csv("data/processed/canonical_to_raw_overarching.csv")
canon_to_over_map = dict(zip(
    canon_to_over_df["Canonical Question"].str.strip().str.lower(),
    canon_to_over_df["Overarching"].str.strip().str.lower(),
))


def response_type(row):
    freq_cols = {"All The Time", "A Lot Of The Time", "Sometimes", "Not At All"}
    yesno_cols = {"Yes", "Maybe", "No"}
    has_freq = any(col in row and row[col] > 0 for col in freq_cols)
    has_yesno = any(col in row and row[col] > 0 for col in yesno_cols)
    if has_freq and not has_yesno:
        return "Frequency"
    elif has_yesno and not has_freq:
        return "YesNoMaybe"
    elif has_freq and has_yesno:
        return "Both"
    else:
        return "Other"

def sort_within_year(group, response_cols):
    # If 'School Year' not in group columns, add it back using group.name
    if 'School Year' not in group.columns:
        group['School Year'] = group.name
    group['row_sum'] = group[response_cols].sum(axis=1)
    sorted_group = group.sort_values(['response_type_sort', 'row_sum'], ascending=[True, False])
    return sorted_group.drop(columns='row_sum')

preferred_order = ["Yes", "Maybe", "No", "All the time", "A lot of the time", "Sometimes", "Not at all"]
fixed_cols = ['School Year', 'Canonical Question']

for group in ["younger", "older"]:
    data_dir = f"data/processed/{group}/summary/cons_resp"
    years = ["20-21", "21-22", "22-23", "23-24", "24-25"]
    years_files = [
        (year, f"{data_dir}/sy{year}_{group.upper()}_ENGLISH_questions_consolidated_summary.csv")
        for year in years
    ]

    frames = []
    for year, fp in years_files:
        if not os.path.exists(fp):
            print(f"Warning: File not found: {fp} (skipping this year)")
            continue
        df = pd.read_csv(fp)
        frames.append(standardize_df(df, year))

    if not frames:
        print(f"No files found for group: {group}. Skipping.")
        continue

    merged = pd.concat(frames, ignore_index=True).fillna(0)

    # Preferred order for response columns
    all_response_cols = [col for col in merged.columns if col not in fixed_cols]
    all_response_cols_lc = [col.lower() for col in all_response_cols]
    final_response_cols = []
    for col in preferred_order:
        if col.lower() in all_response_cols_lc:
            idx = all_response_cols_lc.index(col.lower())
            final_response_cols.append(all_response_cols[idx])
    extra_cols = [col for col in all_response_cols if col not in final_response_cols]
    final_cols = fixed_cols + final_response_cols + sorted(extra_cols)

    merged = merged[final_cols]

        # Grouping and sorting by response type and row sum within year
    merged['Response Type'] = merged.apply(response_type, axis=1)
    response_type_order = {"Frequency": 0, "YesNoMaybe": 1, "Both": 2, "Other": 3}
    merged['response_type_sort'] = merged['Response Type'].map(response_type_order).fillna(99)

    response_cols = [col for col in merged.columns if col not in fixed_cols + ['Response Type', 'response_type_sort']]
    school_year_order = ["20-21", "21-22", "22-23", "23-24", "24-25"]
    merged['School Year'] = pd.Categorical(merged['School Year'], categories=school_year_order, ordered=True)
    merged = merged.sort_values('School Year')

    # ---- One pythonic groupby, future-proof ----
    merged = (
        merged
        .groupby('School Year', group_keys=False, sort=False, observed=False)
        .apply(lambda g: sort_within_year(g, response_cols), include_groups=False)
        .reset_index(drop=True)
    )


    # Now, always explicitly set column order after groupby-apply
    merged = merged[[*fixed_cols, *final_response_cols, *sorted(extra_cols)]]
    
    for col in final_response_cols + sorted(extra_cols):
        if pd.api.types.is_numeric_dtype(merged[col]):
            merged[col] = merged[col].astype(int)
            
    # Normalize and map to overarching
    merged["Normalized Canonical"] = merged["Canonical Question"].str.strip().str.lower()
    merged["Overarching"] = merged["Normalized Canonical"].map(canon_to_over_map)
    merged.drop(columns=["Normalized Canonical"], inplace=True)

    # Output file
    output_dir = "data/processed"
    os.makedirs(output_dir, exist_ok=True)
    output_file = f"{output_dir}/consolidated_questions_{group}.csv"
    merged.to_csv(output_file, index=False)
    print(f"Saved: {output_file}")
