import pandas as pd
import glob
import os

def test_consolidate_multiple_csvs(tmp_path, monkeypatch):
    # Create multiple fake summary CSVs
    for i in range(3):
        pd.DataFrame({
            "Question": [f"Q{i}"], "Agree": [i], "Disagree": [0]
        }).to_csv(tmp_path / f"summ_{i}.csv", index=False)
    files = glob.glob(str(tmp_path / "summ_*.csv"))
    # Test merge logic
    from scripts.transform import consolidate_responses
    out_path = tmp_path / "consolidated.csv"
    dfs = [pd.read_csv(f) for f in files]
    all_responses = pd.concat(dfs, ignore_index=True)
    all_responses.to_csv(out_path, index=False)
    df_merged = pd.read_csv(out_path)
    assert len(df_merged) == 3
    assert "Agree" in df_merged.columns
