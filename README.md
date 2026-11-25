# Mini-VulnFinBot — Production-Grade DevSecOps & AI Security Pipeline

## 1. Project Description
**Mini-VulnFinBot** is a simplified AI-powered financial assistant built with Python and Flask. This project demonstrates how to integrate automated security controls (SAST, SCA, Container Scanning, DAST, and AI-Specific Security Testing) into a GitHub Actions CI/CD pipeline starting from an empty repository.

## 2. Technologies & Security Tools
- **Backend:** Python 3.12, Flask, Gunicorn
- **Testing:** pytest
- **SAST:** Bandit, Semgrep (custom rules)
- **Dependency Scanning (SCA):** pip-audit
- **Containerization & Image Scanning:** Docker, Trivy
- **DAST:** OWASP ZAP Baseline Scanner
- **CI/CD & Reporting:** GitHub Actions, GitHub Actions Artifacts

## 3. Project Architecture
```text
vulnfinbot-secure-pipeline/
├── app/
│   ├── __init__.py          # Flask app factory, security headers, error handlers
│   └── routes.py            # /health and /api/chat endpoints + AI guardrails
├── tests/
│   ├── __init__.py
│   ├── test_app.py          # Functional & input validation unit tests
│   └── test_ai_security.py  # AI security tests & Markdown report generator
├── security/
│   └── semgrep/
│       └── rules.yml        # Custom Semgrep security rules
├── reports/                 # Generated security reports (uploaded as CI artifacts)
├── .github/
│   └── workflows/
│       └── security-pipeline.yml
├── Dockerfile
├── requirements.txt
└── run.py