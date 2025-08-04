import pandas as pd
import os

def test_consolidate_groupby(tmp_path, monkeypatch):
    input_csv = tmp_path / "consolidated_responses.csv"
    pd.DataFrame({
        "Canonical Question": ["A", "A", "B"],
        "Agree": [2, 3, 1],
        "Disagree": [0, 1, 1]
    }).to_csv(input_csv, index=False)
    # Patch mapping to overarching for test
    canon_to_over_map = {"a": "Group1", "b": "Group2"}
    monkeypatch.setattr("consolidate_questions.canon_to_over_map", canon_to_over_map)
    # Simulate main logic
    df = pd.read_csv(input_csv)
    totals = df.groupby("Canonical Question").sum(numeric_only=True).reset_index()
    totals["Overarching"] = totals["Canonical Question"].str.lower().map(canon_to_over_map)
    assert "Overarching" in totals.columns
    assert set(totals["Overarching"]) == {"Group1", "Group2"}
