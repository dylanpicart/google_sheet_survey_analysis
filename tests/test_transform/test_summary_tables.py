import pandas as pd
import os
from scripts.transform.summary_tables import value_count_table

def test_value_count_table_basic():
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
