import os
import pandas as pd
import yaml
from unittest.mock import patch
import pytest

from scripts.extract.load_feedback_data import FeedbackDataLoader

@pytest.mark.skipif(os.environ.get("CI") == "true", reason="No credentials in CI")
def test_load_and_clean_sheet(tmp_path, monkeypatch):
    # Create dummy links.yaml
    dummy_links = {"2023": {"younger": {"Test School": {"Form Responses": {"sheet_id": "sid", "gid": "gid"}}}}}
    data_dir = tmp_path / "data"
    raw_dir = data_dir / "raw" / "younger"
    config_dir = data_dir / "configs"
    raw_dir.mkdir(parents=True, exist_ok=True)
    config_dir.mkdir(parents=True, exist_ok=True)
    yaml_path = config_dir / "links.yaml"
    with open(yaml_path, "w") as f:
        yaml.safe_dump(dummy_links, f)
    fake_creds = tmp_path / "fake_creds.json"
    fake_creds.write_text("{}")  # dummy JSON for testing

    # Mock requests.get to return dummy CSV content
    dummy_csv = "Q1,Q2\nYes,No\nNo,Yes"

    class DummyResponse:
        def __init__(self, content):
            self.content = content

        def raise_for_status(self):
            pass

    with patch("scripts.extract.load_feedback_data.requests.get") as mock_get, patch.object(
        FeedbackDataLoader, "_make_headers", return_value={}
    ):
        mock_get.return_value = DummyResponse(dummy_csv.encode("utf-8"))
        # Instantiate loader with test paths
        loader = FeedbackDataLoader(
            data_dir=str(data_dir), yaml_path=str(yaml_path), service_account_file=str(fake_creds), headers={}
        )
        loader.download_all()  # Run the ETL

    # Check output file and data
    out = data_dir / "raw" / "younger" / "sy2023_younger_feedback.csv"
    assert out.exists()
    df = pd.read_csv(out)
    assert "Q1" in df.columns and "Q2" in df.columns
    assert set(df.Q1) == {"Yes", "No"}
    assert set(df.Q2) == {"No", "Yes"}
