import pandas as pd
import os

def standardize_df(df, year, qcon_map, rescon_mapping):
    df.rename(columns=lambda x: x.strip(), inplace=True)
    df['Canonical Question'] = df['Column'].map(qcon_map).fillna(df['Column'])
    value_cols = [col for col in df.columns if col != 'Column']
    col_map = {col: rescon_mapping.get(col, col) for col in value_cols}
    df = df.rename(columns=col_map)
    df = df.groupby('Canonical Question', as_index=False).sum(numeric_only=True)
    df['School Year'] = year
    response_cols = [col for col in df.columns if col not in ["Canonical Question", "School Year"]]
    return df[['School Year', 'Canonical Question'] + response_cols]

def response_type(row):
    freq_cols = {"All the time", "A lot of the time", "Sometimes", "Not at all"}
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
    if 'School Year' not in group.columns:
        group['School Year'] = group.name
    group['row_sum'] = group[response_cols].sum(axis=1)
    sorted_group = group.sort_values(['response_type_sort', 'row_sum'], ascending=[True, False])
    return sorted_group.drop(columns='row_sum')

def consolidate_questions(
    group,
    years_files,
    qcon_map,
    rescon_mapping,
    canon_to_over_map,
    output_file,
    preferred_order=None,
    fixed_cols=None
):
    preferred_order = preferred_order or ["Yes", "Maybe", "No", "All the time", "A lot of the time", "Sometimes", "Not at all"]
    fixed_cols = fixed_cols or ['School Year', 'Canonical Question']

    frames = []
    for year, fp in years_files:
        if not os.path.exists(fp):
            print(f"Warning: File not found: {fp} (skipping this year)")
            continue
        df = pd.read_csv(fp)
        frames.append(standardize_df(df, year, qcon_map, rescon_mapping))

    if not frames:
        print(f"No files found for group: {group}. Skipping.")
        return

    merged = pd.concat(frames, ignore_index=True).fillna(0)

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

    merged = (
        merged
        .groupby('School Year', group_keys=False, sort=False, observed=False)
        .apply(lambda g: sort_within_year(g, response_cols), include_groups=False)
        .reset_index(drop=True)
    )

    merged = merged[[*fixed_cols, *final_response_cols, *sorted(extra_cols)]]

    for col in final_response_cols + sorted(extra_cols):
        if pd.api.types.is_numeric_dtype(merged[col]):
            merged[col] = merged[col].astype(int)

    # Normalize and map to overarching
    merged["Normalized Canonical"] = merged["Canonical Question"].str.strip().str.lower()
    merged["Overarching"] = merged["Normalized Canonical"].map(canon_to_over_map)
    merged.drop(columns=["Normalized Canonical"], inplace=True)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    merged.to_csv(output_file, index=False)
    print(f"Saved: {output_file}")

def batch_consolidate_questions(
    groups,
    years_list,
    data_root,
    qcon_map,
    rescon_mapping,
    canon_to_over_map
):
    for group in groups:
        data_dir = os.path.join(data_root, group, "summary", "cons_resp")
        years_files = [
            (year, f"{data_dir}/sy{year}_{group.upper()}_ENGLISH_questions_consolidated_summary.csv")
            for year in years_list
        ]
        output_file = os.path.join(data_root, f"consolidated_questions_{group}.csv")
        consolidate_questions(
            group=group,
            years_files=years_files,
            qcon_map=qcon_map,
            rescon_mapping=rescon_mapping,
            canon_to_over_map=canon_to_over_map,
            output_file=output_file
        )

if __name__ == "__main__":
    from data.configs import QCON_MAP, RESCON_MAPPING
    canon_to_over_df = pd.read_csv("data/processed/audit/canonical_to_raw_overarching.csv")
    canon_to_over_map = dict(zip(
        canon_to_over_df["Canonical Question"].str.strip().str.lower(),
        canon_to_over_df["Overarching"].str.strip().str.lower(),
    ))
    years = ["20-21", "21-22", "22-23", "23-24", "24-25"]
    data_root = "data/processed"
    batch_consolidate_questions(
        groups=["younger", "older"],
        years_list=years,
        data_root=data_root,
        qcon_map=QCON_MAP,
        rescon_mapping=RESCON_MAPPING,
        canon_to_over_map=canon_to_over_map
    )
