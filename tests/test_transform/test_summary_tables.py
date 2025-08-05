import os
import pandas as pd
from scripts.transform.summary_tables import value_count_table, process_all_summaries

def test_value_count_table_basic(monkeypatch):
    dummy_scale_orders = {
        "likert": [
            "Strongly Disagree", "Disagree", "Neither Agree nor Disagree", "Agree", "Strongly Agree"
        ],
        "yes_no_maybe": ["Yes", "Maybe", "No"]
    }

    # Patch SCALE_ORDERS in the module
    import scripts.transform.summary_tables as st_mod
    st_mod.SCALE_ORDERS = dummy_scale_orders

    df = pd.DataFrame({
        "Satisfaction": ["Agree", "Disagree", "Agree", "Neither Agree nor Disagree", "Agree"],
        "Trust": ["Yes", "No", "Yes", "Maybe", "No"]
    })
    summary = value_count_table(df, ["Satisfaction", "Trust"])

    assert "Question" in summary.columns
    assert set(summary["Question"]) == {"Satisfaction", "Trust"}
    assert "Agree" in summary.columns
    assert "Disagree" in summary.columns
    # Should count correctly
    sat = summary[summary["Question"]=="Satisfaction"].iloc[0]
    assert sat["Agree"] == 3


def test_process_all_summaries(tmp_path, monkeypatch):
    # Setup dummy data/dirs
    data_dir = tmp_path / "data" / "processed" / "younger"
    summary_dir = data_dir / "summary"
    os.makedirs(data_dir, exist_ok=True)
    # Write a dummy input CSV
    input_csv = data_dir / "sample.csv"
    pd.DataFrame({
        "Satisfaction": ["Agree", "Disagree", "Agree", "Neither Agree nor Disagree", "Agree"],
        "Trust": ["Yes", "No", "Yes", "Maybe", "No"]
    }).to_csv(input_csv, index=False)

    # Use a minimal scale order mapping
    dummy_scale_orders = {
        "likert": [
            "Strongly Disagree", "Disagree", "Neither Agree nor Disagree", "Agree", "Strongly Agree"
        ],
        "yes_no_maybe": ["Yes", "Maybe", "No"]
    }
    # Patch SCALE_ORDERS in the module
    import scripts.transform.summary_tables as st_mod
    st_mod.SCALE_ORDERS = dummy_scale_orders

    # Call modular function with test folder
    process_all_summaries(
        folders={"younger": str(data_dir)},
        scale_orders=dummy_scale_orders
    )

    # Assert: Output file exists and contents are correct
    output_csv = summary_dir / "sample_summary.csv"
    assert output_csv.exists()
    summary = pd.read_csv(output_csv)
    assert "Question" in summary.columns
    assert set(summary["Question"]) == {"Satisfaction", "Trust"}
    assert "Agree" in summary.columns
    # Check counts match expected
    sat = summary[summary["Question"] == "Satisfaction"].iloc[0]
    assert sat["Agree"] == 3

