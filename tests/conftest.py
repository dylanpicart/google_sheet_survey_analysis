import pytest
import pandas as pd
import yaml
import os

############################
# Dummy Data and Mappings  #
############################

@pytest.fixture
def dummy_qcon_map():
    """Canonical question mapping for test purposes."""
    return {
        "How safe do you feel?": "Feelings of Safety",
        "Is there an adult you trust?": "Trusted Adult",
        "Satisfied?": "Satisfaction",
        "Q1": "Feelings of Safety",
        "Q2": "Trust",
    }

@pytest.fixture
def dummy_en_sp_mapping():
    """English-Spanish column mapping."""
    return {
        "¿Está satisfecho?": "Satisfied?",
        "¿Confía en adultos?": "Trust?",
        "¿Cómo se siente?": "How do you feel?"
    }

@pytest.fixture
def dummy_answer_mapping():
    """Spanish cell value mapping."""
    return {
        "Sí": "Yes",
        "No": "No",
        "Tal vez": "Maybe",
        "Satisfecho": "Satisfied",
        "Insatisfecho": "Unsatisfied"
    }

@pytest.fixture
def dummy_links_yaml(tmp_path):
    """Dummy links.yaml structure for extract tests."""
    links = {
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
    path = tmp_path / "links.yaml"
    with open(path, "w") as f:
        yaml.safe_dump(links, f)
    return path

#########################
# DataFrame/CSV Helpers #
#########################

@pytest.fixture
def dummy_dataframe():
    """Simple DataFrame for value count/summary tests."""
    return pd.DataFrame({
        "Satisfied?": ["Yes", "No", "Yes"],
        "Trust": ["Yes", "No", "Maybe"]
    })

@pytest.fixture
def write_csv(tmp_path):
    """Helper: write a dict to a CSV file and return path."""
    def _write_csv(name, data):
        path = tmp_path / name
        pd.DataFrame(data).to_csv(path, index=False)
        return path
    return _write_csv

@pytest.fixture
def write_yaml(tmp_path):
    """Helper: write dict as YAML and return path."""
    def _write_yaml(name, data):
        path = tmp_path / name
        with open(path, "w") as f:
            yaml.safe_dump(data, f)
        return path
    return _write_yaml

#############################
# Google/Env Patch Fixtures #
#############################

@pytest.fixture(autouse=True)
def patch_env_vars(monkeypatch, tmp_path):
    """Patch env vars for all tests, use temp paths for creds/yaml."""
    monkeypatch.setenv("GOOGLE_CREDS_PATH", str(tmp_path / "fake_creds.json"))
    monkeypatch.setenv("ROOT_FOLDER_ID", "test_folder_id")
    monkeypatch.setenv("PYTHONHASHSEED", "42")  # for determinism
    # ...add more as needed

@pytest.fixture
def fake_service_account_file(tmp_path):
    """Create a fake Google creds JSON file."""
    creds = {
        "type": "service_account",
        "project_id": "dummy",
        "private_key_id": "dummy",
        "private_key": "-----BEGIN PRIVATE KEY-----\nFAKE\n-----END PRIVATE KEY-----\n",
        "client_email": "dummy@dummy.iam.gserviceaccount.com",
        "client_id": "1234567890",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dummy"
    }
    path = tmp_path / "fake_creds.json"
    import json
    with open(path, "w") as f:
        json.dump(creds, f)
    return path

#########################
# Dummy Utility Fixtures#
#########################

@pytest.fixture
def dummy_scale_orders():
    """Minimal Likert/scale mapping for summary tests."""
    return {
        "likert_1": [
            "Strongly Disagree", "Disagree", "Neither Agree nor Disagree", "Agree", "Strongly Agree"
        ],
        "yes_no_maybe": [
            "Yes", "Maybe", "No"
        ]
    }

@pytest.fixture
def dummy_summary_map():
    """Dummy summary mapping for column normalization."""
    return {
        "yes": "Yes",
        "no": "No",
        "maybe": "Maybe",
        "strongly disagree": "Disagree",
        "disagree": "Disagree",
        "agree": "Agree",
        "strongly agree": "Agree"
    }


def test_mapping_usage(dummy_qcon_map):
    assert dummy_qcon_map["How safe do you feel?"] == "Feelings of Safety"


def test_csv_write(write_csv):
    path = write_csv("test.csv", {"A": [1,2], "B": [3,4]})
    df = pd.read_csv(path)
    assert "A" in df.columns


def test_creds(fake_service_account_file):
    assert fake_service_account_file.exists()
