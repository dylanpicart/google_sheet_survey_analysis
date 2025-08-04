import pandas as pd
import os

def test_extract_questions(tmp_path, monkeypatch):
    # Create dummy processed input CSV
    input_path = tmp_path / "feedback_2021.csv"
    pd.DataFrame({"Q1": [1,2], "Q2": [3,4]}).to_csv(input_path, index=False)
    monkeypatch.chdir(tmp_path)
    # Patch input path in raw_audit
    from scripts.extract import raw_audit
    # Now test: audit output file is created and contains expected columns
    output_path = tmp_path / "audit_group_a.csv"
    assert output_path.exists()
    df_audit = pd.read_csv(output_path)
    assert "Raw Question" in df_audit.columns
    assert set(df_audit["Raw Question"]) == {"Q1", "Q2"}
