# Makefile for Modular ETL

.PHONY: all pipeline extract transform load clean test

# Run all except scraping Google Drive links (skipped by design)
pipeline: extract transform confirm_load

# Run only extract (excluding scrape_drive_links)
extract:
	python -m scripts.extract.load_feedback_data
	python -m scripts.extract.raw_audit

# Run only transform
transform:
	python -m scripts.transform.translate_spanish_csv
	python -m scripts.transform.audit_map
	python -m scripts.transform.summary_tables
	python -m scripts.transform.consolidate_responses
	python -m scripts.transform.consolidate_questions
	python -m scripts.transform.summarize_totals

# (Optional) Run the scrape_drive_links step explicitly
scrape:
	python -m scripts.extract.scrape_drive_links

# Load step (Excel output) with confirmation
confirm_load:
	@read -p "⚠️  Do you want to run the final load (Excel output)? [Y/N]: " yn; \
	if [ "$$yn" = "y" ] || [ "$$yn" = "Y" ]; then \
		make load; \
	else \
		echo "Skipped load step."; \
	fi

load:
	python -m scripts.load.load_to_excel

clean:
	rm -rf data/processed/*

test:
	pytest -v

lint:
	ruff check . && flake8 . && bandit -r .

