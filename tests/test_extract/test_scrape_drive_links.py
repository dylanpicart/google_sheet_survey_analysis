import os
import yaml
from unittest.mock import patch, MagicMock


def test_generate_yaml_structure(monkeypatch, tmp_path):
    # Patch working directory to project root (assuming you run pytest from root)
    monkeypatch.chdir(os.path.abspath(os.path.dirname(__file__) + "/../.."))
    os.makedirs("data/configs", exist_ok=True)

    # Patch env vars for creds and folder id
    fake_creds = tmp_path / "fake_creds.json"
    fake_creds.write_text("{}")  # dummy json content
    monkeypatch.setenv("GOOGLE_CREDS_PATH", str(fake_creds))
    monkeypatch.setenv("ROOT_FOLDER_ID", "fake-root-folder-id")

    # Patch all network calls to Google API
    with patch("scripts.extract.scrape_drive_links.authenticate_drive") as mock_auth_drive, patch(
        "scripts.extract.scrape_drive_links.list_subfolders"
    ) as mock_list_subfolders, patch(
        "scripts.extract.scrape_drive_links.list_sheets_in_folder"
    ) as mock_list_sheets, patch(
        "scripts.extract.scrape_drive_links.generate_sheet_tabs"
    ) as mock_generate_tabs:

        # Setup mocks
        mock_auth_drive.return_value = (MagicMock(), MagicMock())
        mock_list_subfolders.side_effect = [
            [{"id": "y1", "name": "SY23-24 Surveys"}],  # year_folders
            [{"id": "sfid", "name": "Student Feedback"}],  # feedback_folders
            [{"id": "sch1", "name": "Test School"}],  # school_folders
        ]
        mock_list_sheets.return_value = [{"id": "sheet123", "name": "Test Sheet"}]
        mock_generate_tabs.return_value = {"Form Responses": 456}

        # Run modularized function directly!
        from scripts.extract.scrape_drive_links import generate_links_yaml

        # Use test paths to avoid touching real data
        test_output = tmp_path / "links.yaml"
        generate_links_yaml(
            root_folder_id="fake-root-folder-id",
            service_account_file=str(fake_creds),
            output_path=str(test_output),
            valid_years=["SY23-24 Surveys"],
        )

        # Check output file
        assert test_output.exists(), "YAML output file does not exist!"

        # Validate content
        with open(test_output) as f:
            d = yaml.safe_load(f)
            assert "2324" in d
            assert "Test School" in str(d)

        # Clean up (tmp_path auto-cleans)
