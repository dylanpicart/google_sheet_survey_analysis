import os
import pandas as pd
import yaml
import requests
from io import StringIO
from google.oauth2 import service_account
import google.auth.transport.requests
from dotenv import load_dotenv
from utils import setup_logging

logger = setup_logging("extract")


class FeedbackDataLoader:
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly", "https://www.googleapis.com/auth/drive.readonly"]

    def __init__(self, data_dir=None, yaml_path=None, service_account_file=None, headers=None):
        load_dotenv()
        self.data_dir = data_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "data"))
        self.yaml_path = yaml_path or os.path.join(self.data_dir, "configs", "links.yaml")
        self.service_account_file = service_account_file or os.getenv("GOOGLE_CREDS_PATH")
        self.headers = headers or self._make_headers()
        self._links_dict = None  # For @property
        self.student_feedback_dict = {"older": {}, "younger": {}}

    def _make_headers(self):
        credentials = service_account.Credentials.from_service_account_file(
            self.service_account_file, scopes=self.SCOPES
        )
        auth_req = google.auth.transport.requests.Request()
        credentials.refresh(auth_req)
        return {"Authorization": f"Bearer {credentials.token}"}

    def health_check(self):
        problems = []
        # Check YAML
        if not os.path.exists(self.yaml_path):
            problems.append(f"YAML config not found: {self.yaml_path}")
        # Check data_dir
        raw_dir = os.path.join(self.data_dir, "raw")
        try:
            os.makedirs(raw_dir, exist_ok=True)
            testfile = os.path.join(raw_dir, "test_perm.txt")
            with open(testfile, "w") as f:
                f.write("test")
            os.remove(testfile)
        except Exception as e:
            problems.append(f"Data directory not writable: {raw_dir} ({e})")
        # Check credentials
        if not os.path.exists(self.service_account_file):
            problems.append(f"Google service account file not found: {self.service_account_file}")
        else:
            try:
                _ = self._make_headers()  # Just to check credentials load
            except Exception as e:
                problems.append(f"Failed to initialize credentials: {e}")
        if problems:
            for msg in problems:
                logger.error(msg)
            raise RuntimeError("Health check failed:\n" + "\n".join(problems))
        logger.info("✅ Health check passed.")
        return True

    @property
    def links_dict(self):
        """
        Loads links.yaml only on first access and caches the result.
        Use .reload_links() to force refresh from disk.
        """
        if self._links_dict is None:
            with open(self.yaml_path, "r") as file:
                self._links_dict = yaml.safe_load(file)
        return self._links_dict

    def reload_links(self):
        """Force reload links.yaml on next access."""
        self._links_dict = None

    def download_all(self, year=None, category=None, school=None, tab=None):
        """Download all or filtered survey tabs based on links.yaml."""
        self.health_check()

        for y, categories in self.links_dict.items():
            if year and str(y) != str(year):
                continue
            for cat, schools in categories.items():
                if category and cat != category:
                    continue
                all_dfs = []
                logger.info(f"📅 Loading data for {y} - {cat}")
                for school_name, tabs in schools.items():
                    if school and school_name != school:
                        continue
                    for tab_name, details in tabs.items():
                        if tab and tab_name != tab:
                            continue
                        sheet_id = details["sheet_id"]
                        gid = details["gid"]
                        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

                        logger.info(f"⏳ Loading {school_name} - {tab_name}")

                        try:
                            response = requests.get(csv_url, headers=self.headers, timeout=15)
                            response.raise_for_status()
                            content = response.content.decode("utf-8", errors="replace")
                            df = pd.read_csv(StringIO(content))
                            df["School"] = school_name
                            df["Year"] = y
                            df["Tab"] = tab_name
                            all_dfs.append(df)
                            logger.info(f"✅ Successfully loaded {school_name} - {tab_name}")
                        except Exception as e:
                            logger.error(f"❌ Failed to load {school_name} - {tab_name}: {e}", exc_info=True)

                if all_dfs:
                    combined_df = pd.concat(all_dfs, ignore_index=True)
                    self.student_feedback_dict[cat][y] = combined_df
                    csv_path = os.path.join(self.data_dir, "raw", cat, f"sy{y}_{cat}_feedback.csv")
                    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
                    combined_df.to_csv(csv_path, index=False)
                    logger.info(f"💾 Saved combined DataFrame to {csv_path}")
        return self.student_feedback_dict


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Download all (or filtered) survey feedback CSVs from links.yaml.")
    parser.add_argument("--year", help="Year to process (e.g., '21-22')", default=None)
    parser.add_argument("--category", help="Category (older/younger)", default=None)
    parser.add_argument("--school", help="School name to filter", default=None)
    parser.add_argument("--tab", help="Tab name to filter", default=None)

    args = parser.parse_args()
    loader = FeedbackDataLoader()
    loader.download_all(year=args.year, category=args.category, school=args.school, tab=args.tab)
