import pandas as pd
from scripts.transform.audit_map import audit_map_for_group


def test_audit_map_for_group(tmp_path, monkeypatch):
    # Arrange: Create dummy input and output dirs
    data_dir = tmp_path / "data"
    (data_dir / "raw" / "younger").mkdir(parents=True, exist_ok=True)
    (data_dir / "processed" / "younger").mkdir(parents=True, exist_ok=True)

    # Dummy group params for "younger"
    params = {
        "raw_dir": str(data_dir / "raw" / "younger" / ""),
        "question_list": str(data_dir / "processed" / "audit" / "SF_OA_Younger.csv"),
        "output_dir": str(data_dir / "processed" / "younger" / ""),
    }
    (data_dir / "processed" / "audit").mkdir(parents=True, exist_ok=True)
    pd.DataFrame({"Raw Question": ["How safe do you feel?"], "Sample Responses": ["Yes|No"]}).to_csv(
        params["question_list"], index=False
    )

    # Minimal raw input CSV (for one year)
    year = "sy20-21"
    input_csv = data_dir / "raw" / "younger" / f"{year}_younger_feedback.csv"
    pd.DataFrame(
        {
            "How safe do you feel?": ["Yes", "No"],
            "School": ["A", "B"],  # Make two distinct schools, not both "Test School"
        }
    ).to_csv(input_csv, index=False)

    # Monkeypatch school_years, meta_variants, and junk_cols as needed for minimal reproducibility
    school_years = ["sy20-21"]
    meta_variants = {"School": ["School"], "Grade": ["Grade"], "School Year": ["Year"], "Tab": ["Tab"]}
    junk_cols = []

    # Act: Call the modularized group function
    audit_map_for_group(
        group="younger", params=params, school_years=school_years, meta_variants=meta_variants, junk_cols=junk_cols
    )

    # Assert: Output file created and contains expected columns
    output_csv = data_dir / "processed" / "younger" / f"{year}_YOUNGER_ENGLISH_questions.csv"
    assert output_csv.exists()
    df = pd.read_csv(output_csv)
    assert "How safe do you feel?" in df.columns
    assert "School" in df.columns
    assert set(df["How safe do you feel?"]) == {"Yes", "No"}
