import pandas as pd
from scripts.transform.summarize_totals import summarize_totals


def test_summarize_totals(tmp_path):
    # Setup dummy input files
    path_younger = tmp_path / "consolidated_questions_younger.csv"
    path_older = tmp_path / "consolidated_questions_older.csv"
    output_fp = tmp_path / "canonical_question_totals.csv"
    pd.DataFrame(
        {
            "Canonical Question": ["A", "B"],
            "Agree": [1, 2],
            "Disagree": [3, 4],
            "Overarching": ["X", "Y"],
            "School Year": ["21-22", "21-22"],
        }
    ).to_csv(path_younger, index=False)
    pd.DataFrame(
        {
            "Canonical Question": ["A", "B"],
            "Agree": [4, 1],
            "Disagree": [1, 1],
            "Overarching": ["X", "Y"],
            "School Year": ["22-23", "22-23"],
        }
    ).to_csv(path_older, index=False)

    # Run function
    summarize_totals(
        consolidated_younger_fp=str(path_younger), consolidated_older_fp=str(path_older), output_fp=str(output_fp)
    )

    # Assert output
    assert output_fp.exists()
    df = pd.read_csv(output_fp)
    assert "Agree" in df.columns and "Disagree" in df.columns
    assert "Canonical Question" in df.columns
    assert "Overarching" in df.columns
    # Sums are correct
    a_row = df[df["Canonical Question"] == "A"].iloc[0]
    assert a_row["Agree"] == 5
    assert a_row["Disagree"] == 4
    b_row = df[df["Canonical Question"] == "B"].iloc[0]
    assert b_row["Agree"] == 3
    assert b_row["Disagree"] == 5
    # Overarching column mapping preserved
    assert set(df["Overarching"]) == {"X", "Y"}
