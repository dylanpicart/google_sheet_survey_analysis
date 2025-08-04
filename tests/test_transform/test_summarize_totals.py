import pandas as pd
import os

def test_totals_merge(tmp_path):
    path_younger = tmp_path / "consolidated_questions_younger.csv"
    path_older = tmp_path / "consolidated_questions_older.csv"
    pd.DataFrame({
        "Canonical Question": ["A", "B"], "Agree": [1, 2], "Disagree": [3, 4], "Overarching": ["X", "Y"]
    }).to_csv(path_younger, index=False)
    pd.DataFrame({
        "Canonical Question": ["A", "B"], "Agree": [4, 1], "Disagree": [1, 1], "Overarching": ["X", "Y"]
    }).to_csv(path_older, index=False)
    # Run core logic
    df_younger = pd.read_csv(path_younger)
    df_older = pd.read_csv(path_older)
    df_all = pd.concat([df_younger, df_older], ignore_index=True)
    response_cols = [col for col in df_all.columns if col not in ["Canonical Question", "Overarching"]]
    totals = df_all.groupby("Canonical Question", as_index=False)[response_cols].sum(numeric_only=True)
    assert "Agree" in totals.columns and "Disagree" in totals.columns
    # Should sum correctly
    a_row = totals[totals["Canonical Question"]=="A"].iloc[0]
    assert a_row["Agree"] == 5
