import pytest
import os
import sys
import yaml
from unittest.mock import patch, MagicMock

def test_generate_yaml_structure(monkeypatch, tmp_path):
    # 1. Setup test environment
    # Patch working directory to project root (assuming you run pytest from root)
    monkeypatch.chdir(os.path.abspath(os.path.dirname(__file__) + "/../.."))
    os.makedirs("data/configs", exist_ok=True)

    # 2. Patch env vars for creds and folder id (if needed by script)
    monkeypatch.setenv("GOOGLE_CREDS_PATH", str(tmp_path / "fake_creds.json"))
    monkeypatch.setenv("ROOT_FOLDER_ID", "fake-root-folder-id")

    # 3. Patch all network calls to Google API
    with patch("scripts.extract.scrape_drive_links.authenticate_drive") as mock_auth_drive, \
         patch("scripts.extract.scrape_drive_links.list_subfolders") as mock_list_subfolders, \
         patch("scripts.extract.scrape_drive_links.list_sheets_in_folder") as mock_list_sheets, \
         patch("scripts.extract.scrape_drive_links.generate_sheet_tabs") as mock_generate_tabs:

        # Return MagicMock for service objects
        mock_auth_drive.return_value = (MagicMock(), MagicMock())

        # Years
        mock_list_subfolders.side_effect = [
            [{"id": "y1", "name": "SY23-24 Surveys"}],   # year_folders
            [{"id": "sfid", "name": "Student Feedback"}], # feedback_folders
            [{"id": "sch1", "name": "Test School"}],      # school_folders
        ]

        # One sheet in school folder
        mock_list_sheets.return_value = [{"id": "sheet123", "name": "Test Sheet"}]
        mock_generate_tabs.return_value = {"Form Responses": 456}

        # 4. Actually run the script under test
        from scripts.extract import scrape_drive_links

        # Check for output
        yaml_path = os.path.abspath("data/configs/links.yaml")
        assert os.path.exists(yaml_path), "YAML output file does not exist!"

        # 5. Validate the structure/content
        with open(yaml_path) as f:
            d = yaml.safe_load(f)
            assert "23-24" in d
            assert "Test School" in str(d)
            # ...expand with stricter asserts as needed...

        # 6. Clean up
        os.remove(yaml_path)
