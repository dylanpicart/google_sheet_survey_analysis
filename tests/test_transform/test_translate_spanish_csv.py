import pandas as pd
from scripts.transform import translate_spanish_csv


def test_translate_spanish_and_merge(tmp_path):
    df = pd.DataFrame(
        {
            "¿Está satisfecho?": ["Sí", "No", "Sí"],
            "Satisfied?": ["", "", ""],
        }
    )
    infile = tmp_path / "input.csv"
    out_translated = tmp_path / "translated.csv"
    out_main = tmp_path / "ENONLY.csv"
    df.to_csv(infile, index=False)

    # The mapping must be English -> Spanish!
    dummy_EN_SP_MAPPING = {"Satisfied?": "¿Está satisfecho?"}
    dummy_ANSWER_MAPPING = {"Sí": "Yes", "No": "No"}
    dummy_cols_to_drop = []

    def normalize_text(s):
        return str(s).strip().lower()

    translate_spanish_csv.process_csv_file(
        str(infile),
        str(out_translated),
        str(out_main),
        EN_SP_MAPPING=dummy_EN_SP_MAPPING,
        ANSWER_MAPPING=dummy_ANSWER_MAPPING,
        cols_to_drop=dummy_cols_to_drop,
        normalize_text=normalize_text,
    )

    df_translated = pd.read_csv(out_translated)
    assert "Satisfied?" in df_translated.columns
    assert set(df_translated["Satisfied?"]) <= {"Yes", "No"}
    df_main = pd.read_csv(out_main)
    assert set(df_main["Satisfied?"]) <= {"Yes", "No"}
