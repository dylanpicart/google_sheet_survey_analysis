import pandas as pd
from scripts.extract.raw_audit import audit_questions_and_write_csv


def test_audit_questions_and_write_csv(tmp_path):
    # Create dummy input CSV
    input_path = tmp_path / "feedback_2021.csv"
    pd.DataFrame({"Q1": [1, 2], "Q2": [3, 4]}).to_csv(input_path, index=False)

    # Minimal dummy mapping and helpers for testing
    dummy_mapping = {"Q1": "Question 1", "Q2": "Question 2"}

    def dummy_build_lookup(mapping):
        return mapping

    def dummy_audit_and_clean_columns(questions, lookup):
        return {q: {"canonical": lookup.get(q, ""), "reason": "test", "suggestions": []} for q in questions}

    # Patch helpers in the audit module
    import scripts.extract.raw_audit as raw_audit_mod

    raw_audit_mod.build_lookup = dummy_build_lookup
    raw_audit_mod.audit_and_clean_columns = dummy_audit_and_clean_columns

    output_csv = tmp_path / "audit_group_a.csv"
    output_excel = tmp_path / "audit_group_a.xlsx"
    audit_questions_and_write_csv(dummy_mapping, "Test", [str(input_path)], str(output_csv), str(output_excel))
    # Check output file
    assert output_csv.exists()
    df_audit = pd.read_csv(output_csv)
    assert "Raw Question" in df_audit.columns
    assert set(df_audit["Raw Question"]) == {"Q1", "Q2"}
    # Optional: check canonical mapping column exists and is correct
    assert set(df_audit["Canonical Mapping"]) == {"Question 1", "Question 2"}
