# Google Sheet Survey ETL Analysis

This project provides a robust, reproducible ETL (Extract, Transform, Load) pipeline for end-to-end analysis of multi-year, multi-language Google Sheet survey data, including raw extraction, cleaning, canonical mapping, advanced summaries, and executive-ready Excel outputs.

---

## **Pipeline Overview**

* **Input:** Raw survey CSVs (downloaded from Google Drive or other source folders).
* **Process:** Clean, normalize, translate, audit, map, summarize, and consolidate responses and questions.
* **Output:** Master Excel files for analysis; fully harmonized survey data for reporting or modeling.

---

## Project Structure

```
root/
│
├── Makefile                 # Run extract, transform, or load scripts
├── .venv/                   # Python virtual environment (not tracked)
├── creds/                   # Google API credentials (never tracked by git)
│
├── data/
│   ├── configs/             # Config files (YAML, mappings, links)
│   ├── raw/                 # All raw survey data (CSV, pre-clean)
│   └── processed/           # All cleaned, processed, and summary data
│
├── notebook/                # Jupyter notebooks and experiments
├── tests/                   # Unit tests and pipeline QA scripts
├── utils/                   # Shared Python utilities/helpers
│
├── scripts/
│   ├── extract/         # Scripts for data download, cleaning, auditing
│   ├── transform/       # Scripts for mapping, summaries, consolidation
│   └── load/                # Scripts for Excel/output/reporting
│
├── .env                     # Environment variables (never tracked)
├── .gitignore               # Files and folders excluded from git
├── README.md                # Project overview and documentation
├── SECURITY.md              # Security and responsible disclosure policy
└── requirements.txt         # Python dependencies

```
---

## **ETL Process**

**1. Extract**

* Download all raw survey CSVs (English, Spanish, etc.) for all years/cohorts.

### **Google API Extraction**

#### **Overview**

This pipeline’s first step (`scrape_drive_links.py`) automates the downloading of raw survey CSV files from Google Drive (or optionally Google Sheets, converted to CSV).
It uses the Google Drive and/or Google Sheets API for authenticated access to your organization’s files and ensures you always work with up-to-date, original data.

---

#### **Requirements**

* **Google Cloud Platform Project** with Drive and/or Sheets API enabled
* **Service Account credentials** (or OAuth2 credentials) with access to the relevant files/folders
* The following **Python packages**:

  * `google-api-python-client`
  * `google-auth-httplib2`
  * `google-auth-oauthlib`
  * `gspread` (for direct Google Sheets to CSV, optional)
  * `pandas`
  * `requests`
  * `tqdm` (optional, for progress bars)

**Install them with:**

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib gspread pandas requests tqdm
```

---

#### **Google API Setup**

1. **Create a Google Cloud project** at [https://console.cloud.google.com/](https://console.cloud.google.com/)
2. **Enable the APIs:**

   * Google Drive API
   * (Optionally) Google Sheets API
3. **Create and download a Service Account key** (JSON) or OAuth client secret.
4. **Share your survey folder/files** with the Service Account email (if using a Service Account).
5. **Save your credentials** (usually as `service_account.json` or `credentials.json`) in a secure location.

---

#### **Script Configuration**

* Place your credentials file in a known location (e.g., `secrets/service_account.json`).
* Set an environment variable or `.env` entry:

  ```
  GOOGLE_APPLICATION_CREDENTIALS=secrets/service_account.json
  ```
* Update `scrape_drive_links.py` to read your folder IDs or search queries as needed.

---

#### **How the Extraction Script Works**

* **Authenticates** with Google Drive using your credentials.
* **Lists all files** in a given folder or matching a search query.
* **Downloads** each file as CSV (either as a raw file or converts a Google Sheet to CSV).
* **Saves** each file into a local directory (e.g., `raw/` or `data/raw/`).

---

#### **Common Usage Example**

```bash
python -m scripts.extract.scrape_drive_links
```

This will:

* Authenticate using your Google credentials
* Download all target survey files (for each year/cohort) to your local `raw/` directory
* Ensure that your pipeline always starts with the latest official data

---

#### **Possible Extraction Script Features**

* **File type filtering** (only download `.csv` or `.gsheet`)
* **Date filtering** (only new/modified files)
* **Automatic conversion** of Google Sheets to CSV
* **Logging of all downloaded file names, IDs, and timestamps**
* **Parallel downloads** for large batches

---

#### **Error Handling**

* **Missing credentials**: Script halts and prints a clear message
* **API quota exceeded**: Script sleeps and retries (or halts with a warning)
* **No files found**: Script exits and prints which query/folder was empty
* **Partial download**: Script can be resumed/restarted safely

---

#### **Security**

* **Never commit credentials** (JSON) to git or public repos
* Restrict service account to “read-only” where possible

---

### **Pro Tips**

* Use **Google Groups** to give bulk file access to your service account.
* For one-off manual downloads, use Google Drive web UI, but for reproducibility, always prefer API automation.
* Keep your service account credentials and folder IDs in `.env` or as command-line args for flexibility.

---

**2. Transform**

* Standardize headers, clean rows, handle missing or malformed data.
* Translate Spanish CSVs to English.
* Audit all unique questions/options; map variations to canonical/overarching questions.
* Generate summary tables (Likert, frequency, Yes/No, etc.) per year and group.
* Consolidate all responses and question summaries across years and groups.
* Summarize totals for cross-year and cross-group analysis.

**3. Load**

* Export all final and intermediate outputs to Excel, with tabs for every summary and year/group.
* Provide “master summary” and “full data” workbooks for stakeholders.

---

## **Requirements**

* **Python 3.8+**
* **Required Python packages:**

  * `pandas`
  * `xlsxwriter`
  * (optionally: `openpyxl`, `numpy`, `unicodedata`, `regex`)
* **bash** (for pipeline orchestration)

Install requirements (example):

```bash
pip install pandas xlsxwriter openpyxl
```

---

## **How to Run the Pipeline**

### **Installation and Requirements**

1. **Clone this repository:**

   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```

2. **Set up your Python virtual environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # (On Windows: venv\Scripts\activate)
   ```

3. **Install all Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

---

4. **Run the pipeline with:**

   ```bash
   ./run_etl.sh
   ```

   *(Ensure it’s executable: `chmod +x run_etl.sh`)*

**This will:**

* Scrape and standardize raw data
* Translate (if needed)
* Audit, map, and consolidate all survey questions/responses
* Output results as `SF_Master_Summary.xlsx` and `SF_Master_Data.xlsx` in the `data/processed/` directory

---

### **Using the Makefile for Your ETL Pipeline**

This project includes a **Makefile** for easy automation and orchestration of the ETL workflow.

#### **Common Makefile Commands**

* **Run the full ETL pipeline (skipping Google Drive scraping and confirming before the final Excel output):**

  ```bash
  make pipeline
  ```

* **Run only the extract step (data loading, cleaning, translation, audit):**

  ```bash
  make extract
  ```

* **Run only the transform step (mapping, summary tables, consolidation):**

  ```bash
  make transform
  ```

* **Manually run the scraping step, if you need to update the survey links:**

  ```bash
  make scrape
  ```

* **Run only the final Excel export step:**

  ```bash
  make load
  ```

* **Clean processed data outputs:**

  ```bash
  make clean
  ```

* **Run all unit tests:**

  ```bash
  make test
  ```

---

#### **How it works**

* The Makefile allows you to run any ETL stage individually or in sequence.
* The default `pipeline` target skips the Google Drive scraping step and asks for confirmation before creating the final Excel output, so you won’t overwrite results by accident.
* You can always run the original `run_etl.sh` script for fully automated execution.

---

#### **Pro tip:**

**Always run `make` commands from the project root directory.**
The Makefile expects all scripts, data, and outputs to use the standard project structure.

---

## **Possible Approaches to Data Cleaning**

* **Column normalization:** Consistently rename and strip all headers (lowercase, no spaces, uniform naming).
* **String cleaning:** Remove leading/trailing whitespace, standardize punctuation/quotes, handle Unicode artifacts.
* **Missing value handling:** Remove or fill empty rows/cells, standardize “N/A”, handle outliers.
* **Canonical mapping:** Use `QCON_MAP` and audit mapping to ensure all question variations are consolidated.
* **Translation:** Ensure all responses/options are in English for cross-year consistency.

**Pro Tip:**
Keep logs of all dropped or transformed data for full transparency!

---

## **Next Steps (Pivot & Advanced Analysis)**

* **Multi-select/multi-pivot:** Use canonical mappings to group, count, and analyze all subquestions/options as part of overarching categories.
* **Percentages and rates:** Compute %Yes/No/Maybe per group/year/option.
* **Longitudinal tracking:** Analyze trends in responses across years and cohorts.
* **Visualization:** Use Excel or Python/Streamlit dashboards for charts, pivots, and interactive summaries.

---

## **Error Handling & Quality Assurance**

* **Each ETL step is checked:** Pipeline halts if a key script or file is missing or if any step fails.
* **Inter-step file checks:** Verifies output files from each phase before moving to the next.
* **Logging:** All errors and successes are printed to console (or optionally, a log file).
* **Custom checks:** Can be extended to email, Slack, or alert on failure for production.

**How to debug:**

* Inspect the output/error message to see where the process halted.
* Review intermediate outputs (CSV/Excel) to verify data at each stage.
* Re-run just the failed script for rapid iteration.

---
## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## **Author**

Developed by **Dylan Picart at Partnership With Children.**

Open an issue or submit a pull request!
For help running or customizing the pipeline, contact dylanpicart@mail.adelphi.edu.