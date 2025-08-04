#!/bin/bash
set -euo pipefail

run_step() {
    module_path="$1"
    step_desc="$2"
    echo "=== $step_desc ==="
    if python -m "$module_path"; then
        echo "✅ SUCCESS: $step_desc"
    else
        echo "❌ ERROR: $step_desc failed."
        exit 1
    fi
}

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
run_step "scripts.extract.scrape_drive_links" "1. Scraping drive links"
run_step "scripts.extract.load_feedback_data" "2. Loading feedback data"
run_step "scripts.extract.translate_spanish_csv" "3. Translating Spanish CSVs"
run_step "scripts.extract.raw_audit" "4. Auditing questions"

check_exists "data/processed/younger/feedback_SY20-21.csv" "Younger feedback SY20-21"
check_exists "data/processed/older/feedback_SY20-21.csv" "Older feedback SY20-21"
check_exists "question_samples_audit_older.csv" "Older Audit"
check_exists "question_samples_audit_younger.csv" "Younger Audit"

# --------------------
# TRANSFORM STAGE
# --------------------
run_step "scripts.transform.audit_map" "5. Mapping audit to canonical"
run_step "scripts.transform.summary_tables" "6. Creating summary tables"
run_step "scripts.transform.consolidate_responses" "7. Consolidating responses"
run_step "scripts.transform.consolidate_questions" "8. Consolidating question summaries"
run_step "scripts.transform.summarize_totals" "9. Summarizing totals"

check_exists "data/processed/consolidated_questions_younger.csv" "Younger consolidated questions"
check_exists "data/processed/consolidated_questions_older.csv" "Older consolidated questions"
check_exists "data/processed/canonical_question_totals.csv" "Canonical question totals"

# --------------------
# LOAD STAGE (REPORTING)
# --------------------
run_step "scripts.load.load_to_excel" "10. Creating Excel outputs"

echo "=== PIPELINE COMPLETE ==="
