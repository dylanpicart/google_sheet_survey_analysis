import pandas as pd
import os
from scripts.transform.consolidate_questions import consolidate_questions

def test_consolidate_questions_groupby(tmp_path):
    # Set up dummy per-year input CSVs
    year = "20-21"
    group = "younger"
    input_dir = tmp_path / group / "summary" / "cons_resp"
    input_dir.mkdir(parents=True, exist_ok=True)
    input_fp = input_dir / f"sy{year}_{group.upper()}_ENGLISH_questions_consolidated_summary.csv"
    pd.DataFrame({
        "Column": ["A", "A", "B"],
        "Agree": [2, 3, 1],
        "Disagree": [0, 1, 1]
    }).to_csv(input_fp, index=False)

    # Dummy mappings
    qcon_map = {"A": "A", "B": "B"}
    rescon_mapping = {"Agree": "Agree", "Disagree": "Disagree"}
    canon_to_over_map = {"a": "Group1", "b": "Group2"}

    # Define output file
    output_fp = tmp_path / f"consolidated_questions_{group}.csv"

    # Call the function
    consolidate_questions(
        group=group,
        years_files=[(year, str(input_fp))],
        qcon_map=qcon_map,
        rescon_mapping=rescon_mapping,
        canon_to_over_map=canon_to_over_map,
        output_file=str(output_fp)
    )

    # Assert output exists and has correct columns/mapping
    assert output_fp.exists()
    df_out = pd.read_csv(output_fp)
    assert "Canonical Question" in df_out.columns
    assert "Overarching" in df_out.columns
    assert set(df_out["Canonical Question"]) == {"A", "B"}
    assert set(df_out["Overarching"]) == {"Group1", "Group2"}
    # Check groupby sum
    a_row = df_out[df_out["Canonical Question"] == "A"].iloc[0]
    assert a_row["Agree"] == 5
    assert a_row["Disagree"] == 1
