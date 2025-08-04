#!/bin/bash
set -euo pipefail
# -e: Exit if any command fails
# -u: Treat unset variables as error
# -o pipefail: Catch failures in piped commands

# Function to run a Python ETL step and check for script existence/success
run_step() {
    script_path="$1"
    step_desc="$2"
    if [[ ! -f "$script_path" ]]; then
        echo "❌ ERROR: Script not found: $script_path"
        exit 1
    fi
    echo "=== $step_desc ==="
    if python "$script_path"; then
        echo "✅ SUCCESS: $step_desc"
    else
        echo "❌ ERROR: $step_desc failed."
        exit 1
    fi
}

# Function to check that a file or directory exists (halts if missing)
check_exists() {
    path="$1"
    desc="$2"
    if [[ ! -e "$path" ]]; then
        echo "❌ ERROR: Expected output not found: $desc ($path)"
        exit 1
    fi
    echo "✅ Found: $desc ($path)"
}

echo "=== STARTING ETL PIPELINE ==="

# --------------------
# EXTRACT STAGE
# --------------------
run_step "scripts/extract/scrape_drive_links.py" "1. Scraping drive links"
# Downloads raw data from Google Drive or other source

run_step "scripts/extract/load_feedback_data.py" "2. Loading feedback data"
# Loads, standardizes, and cleans raw CSVs

run_step "scripts/extract/translate_spanish_csv.py" "3. Translating Spanish CSVs"
# Translates Spanish survey files to English

run_step "scripts/extract/raw_audit.py" "4. Auditing questions"
# Audits and extracts all unique question variations for mapping

# --- Extract/Raw output checks ---
# These files are essential for continuing to transform step
check_exists "data/processed/younger/feedback_SY20-21.csv" "Younger feedback SY20-21"
check_exists "data/processed/older/feedback_SY20-21.csv" "Older feedback SY20-21"
check_exists "question_samples_audit_older.csv" "Older Audit"
check_exists "question_samples_audit_younger.csv" "Younger Audit"

# --------------------
# TRANSFORM STAGE
# --------------------
run_step "scripts/transform/audit_map.py" "5. Mapping audit to canonical"
# Maps raw questions to canonical forms

run_step "scripts/transform/summary_tables.py" "6. Creating summary tables"
# Creates summary statistics/counts per question/option

run_step "scripts/transform/consolidate_responses.py" "7. Consolidating responses"
# Combines, aligns, and cleans all individual response data

run_step "scripts/transform/consolidate_questions.py" "8. Consolidating question summaries"
# Creates canonical-level summary tables

run_step "scripts/transform/summarize_totals.py" "9. Summarizing totals"
# Aggregates all data for cross-year, cross-group analysis

# --- Transform output checks ---
# These must exist before loading/export
check_exists "data/processed/consolidated_questions_younger.csv" "Younger consolidated questions"
check_exists "data/processed/consolidated_questions_older.csv" "Older consolidated questions"
check_exists "data/processed/canonical_question_totals.csv" "Canonical question totals"

# --------------------
# LOAD STAGE (REPORTING)
# --------------------
run_step "scripts/load/load_to_excel.py" "10. Creating Excel outputs"
# Combines final CSVs into Excel files for analysis and delivery

echo "=== PIPELINE COMPLETE ==="
