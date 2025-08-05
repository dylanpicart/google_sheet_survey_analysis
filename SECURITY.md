# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project,  
**please report it privately** by emailing [dylanpicart@mail.adelphi.edu].  
Do **not** open a public issue for sensitive disclosures.  
We aim to respond within 3 business days.

## Handling of Sensitive Data

- **No personal, student, or staff data** is ever committed to this repository.
- **All secrets, API keys, and credentials** must be stored in `.env` files, the `creds/` folder, or a managed secrets vault, and are always included in `.gitignore`.
- **Raw data containing PII** is stored in secure, access-controlled locations and deleted after processing.
- **All survey responses are anonymized and aggregated** before any public export or dashboard.

## DevSecOps Practices

- **Dependency security:** All dependencies are pinned and regularly scanned for vulnerabilities (e.g., `pip-audit` in CI/CD).
- **Secrets management:** The repository is regularly scanned for accidental secrets using tools like `truffleHog` and/or `git-secrets`.
- **Static analysis:** Code quality and security are enforced with `ruff`, `flake8`, and `bandit`.
- **Logging:** All logs are rotated, stored only in `/logs`, and never include secrets, tokens, or PII. Logs are monitored for error patterns.
- **Principle of least privilege:** All service accounts and API keys are read-only and minimally scoped wherever possible.
- **Automated validation:** The pipeline includes input/output file validation, schema checks, and exception logging at every step.
- **Continuous Integration:** CI runs all linting, static analysis, testing, and dependency audits on each commit to main branches.

## Support Policy

Security patches are prioritized for active releases and the main branch.  
Archived branches are not routinely monitored for vulnerabilities.

## More Information

For general project guidelines, see [README.md](./README.md).
