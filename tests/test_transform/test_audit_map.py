# tests/test_transform/test_audit_map.py

import subprocess
import sys
import os
import pandas as pd

def test_audit_map_script_runs(tmp_path, monkeypatch):
    # Arrange: Patch working directories and any needed files
    # You may need to create dummy input CSVs as expected by your script
    # Example: data/processed/audit/SF_OA_Younger.csv, etc.
    data_dir = tmp_path / "data"
    (data_dir / "raw" / "younger").mkdir(parents=True, exist_ok=True)
    (data_dir / "raw" / "older").mkdir(parents=True, exist_ok=True)
    (data_dir / "processed" / "audit").mkdir(parents=True, exist_ok=True)
    (data_dir / "processed" / "younger").mkdir(parents=True, exist_ok=True)
    (data_dir / "processed" / "older").mkdir(parents=True, exist_ok=True)
    
    # Write minimal dummy question list CSVs
    pd.DataFrame({
        "Raw Question": ["How safe do you feel?"],
        "Sample Responses": ["Yes|No"]
    }).to_csv(data_dir / "processed" / "audit" / "SF_OA_Younger.csv", index=False)
    pd.DataFrame({
        "Raw Question": ["Is there an adult you trust?"],
        "Sample Responses": ["Yes|No"]
    }).to_csv(data_dir / "processed" / "audit" / "SF_OA_Older.csv", index=False)

    # Write minimal raw input CSVs
    pd.DataFrame({
        "How safe do you feel?": ["Yes", "No"],
        "School": ["Test School", "Test School"]
    }).to_csv(data_dir / "raw" / "younger" / "sy20-21_younger_feedback.csv", index=False)
    pd.DataFrame({
        "Is there an adult you trust?": ["Yes", "No"],
        "School": ["Test School", "Test School"]
    }).to_csv(data_dir / "raw" / "older" / "sy20-21_older_feedback.csv", index=False)

    # Monkeypatch CWD if necessary
    monkeypatch.chdir(tmp_path)
    
    # Act: Run the script as a subprocess
    script_path = os.path.abspath("scripts/transform/audit_map.py")
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    assert result.returncode == 0, f"Script failed: {result.stderr}"

    # Assert: Check for output CSV(s)
    output_csv = data_dir / "processed" / "younger" / "sy20-21_YOUNGER_ENGLISH_questions.csv"
    assert output_csv.exists()
    df = pd.read_csv(output_csv)
    assert "How safe do you feel?" in df.columns

    # Repeat checks for 'older' group as needed
