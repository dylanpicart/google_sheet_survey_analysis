import pandas as pd
import os
from scripts.transform.translate_spanish_csv import process_csv_file

def test_translate_spanish_and_merge(tmp_path):
    # Minimal dummy Spanish/English mapping for test
    df = pd.DataFrame({
        "¿Está satisfecho?": ["Sí", "No", "Sí"],
        "Satisfied?": ["", "", ""],   # Target English column, initially blank
    })
    infile = tmp_path / "input.csv"
    out_translated = tmp_path / "translated.csv"
    out_main = tmp_path / "ENONLY.csv"
    df.to_csv(infile, index=False)

    # Patch mappings for test run (monkeypatch if needed in real project)
    # Example: EN_SP_MAPPING = {"¿Está satisfecho?": "Satisfied?"}
    #          ANSWER_MAPPING = {"Sí": "Yes", "No": "No"}
    process_csv_file(str(infile), str(out_translated), str(out_main))

    # Check: translated file is created
    df_translated = pd.read_csv(out_translated)
    assert "Satisfied?" in df_translated.columns
    assert set(df_translated["Satisfied?"]) <= {"Yes", "No"}
    # Main output should have the correct English column with values
    df_main = pd.read_csv(out_main)
    assert set(df_main["Satisfied?"]) <= {"Yes", "No"}
