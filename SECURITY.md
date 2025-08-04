# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project,  
please report it by emailing [dylanpicart@mail.adelphi.edu].  
Do **not** open a public issue for sensitive disclosures.

## Handling of Sensitive Data

- No personal, student, or staff data is ever committed to this repository.
- All secrets, API keys, and credentials must be kept in `.env` files or cloud secrets managers, and are always included in `.gitignore`.
- All survey responses are anonymized and aggregated before public export.
- Raw data containing PII is stored in secure locations and deleted after processing.

## DevSecOps Practices

- All dependencies are kept up to date and regularly scanned for vulnerabilities (e.g., `pip-audit`).
- Service accounts and API keys are read-only and least-privilege by default.
- The pipeline includes file checks and validation at every step.

## Support Policy

Security patches are prioritized for active releases and main branches.  
Old/archived branches are **not** monitored for vulnerabilities.

## More Information

For general project guidelines, see [README.md](./README.md).

