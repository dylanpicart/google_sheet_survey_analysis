import pandas as pd
import os
from scripts.transform.consolidate_responses import consolidate_summary

def test_consolidate_summary(tmp_path):
    # Create a dummy summary input CSV
    input_csv = tmp_path / "input_summary.csv"
    df = pd.DataFrame({
        "Column": ["Q1", "Q2"],
        "Agree": [3, 1],
        "Disagree": [0, 2],
        "Neither Agree nor Disagree": [1, 1]
    })
    df.to_csv(input_csv, index=False)

    # Minimal dummy summary_map (bucket mapping) and overarching mapping
    summary_map = {
        "agree": "Agree",
        "disagree": "Disagree",
        "neither agree nor disagree": "Neither Agree Nor Disagree"
    }
    canon_to_over_map = {
        "q1": "Safety",
        "q2": "Trust"
    }

    output_csv = tmp_path / "consolidated.csv"
    consolidate_summary(
        input_csv=str(input_csv),
        output_csv=str(output_csv),
        summary_map=summary_map,
        canon_to_over_map=canon_to_over_map
    )

    # Assert output CSV is created and correct
    df_out = pd.read_csv(output_csv)
    assert "Column" in df_out.columns
    assert "Agree" in df_out.columns
    assert "Disagree" in df_out.columns
    assert "Neither Agree Nor Disagree" in df_out.columns
    assert "Overarching" in df_out.columns
    # Check the correct mappings
    assert set(df_out["Column"]) == {"Q1", "Q2"}
    assert set(df_out["Overarching"]) == {"Safety", "Trust"}
    assert df_out.loc[df_out["Column"]=="Q1", "Agree"].iloc[0] == 3
    assert df_out.loc[df_out["Column"]=="Q2", "Disagree"].iloc[0] == 2
