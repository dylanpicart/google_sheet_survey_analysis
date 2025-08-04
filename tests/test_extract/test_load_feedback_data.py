import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import os

@patch("load_feedback_data.requests.get")
def test_load_and_clean_sheet(mock_get, tmp_path, monkeypatch):
    # Mock the .yaml file reading
    dummy_links = {
        "2023": {
            "younger": {
                "Test School": {
                    "Form Responses": {
                        "sheet_id": "sid",
                        "gid": "gid"
                    }
                }
            }
        }
    }
    # Patch YAML loading in the module
    monkeypatch.setattr("load_feedback_data.links_dict", dummy_links)
    # Mock requests.get to return a dummy CSV
    class DummyResponse:
        def __init__(self, content):
            self.content = content
        def raise_for_status(self): pass
    dummy_csv = "Q1,Q2\nYes,No\nNo,Yes"
    mock_get.return_value = DummyResponse(dummy_csv.encode("utf-8"))
    # Patch credentials, headers, DATA_DIR
    monkeypatch.setattr("load_feedback_data.headers", {})
    monkeypatch.setattr("load_feedback_data.DATA_DIR", str(tmp_path))
    # Run the logic
    from scripts.extract import load_feedback_data
    out = tmp_path / "raw" / "younger" / "sy2023_younger_feedback.csv"
    assert out.exists()
    df = pd.read_csv(out)
    assert "Q1" in df.columns and "Q2" in df.columns
    assert set(df.Q1) == {"Yes", "No"}
