# QA Automation Python Demo

## Project Overview
Python demo project for QA automation using pytest with step-based (BDD-style)
test structure. Includes examples for Selenium WebDriver, Playwright, and REST.

## Tech Stack
- Python >= 3.13
- pytest
- Selenium WebDriver
- Playwright
- requests (transitive)
- PyHamcrest
- Reporting: pytest-html, allure-pytest

## Project Structure
```
.
├── src/qa_automation_python_demo/   # Steps, configurations, models
├── tests/                           # Test scenarios (*Tests classes)
├── docs/reports/                    # Generated Allure report
├── allure-results/                  # Allure raw results
├── logging.ini                      # Logging configuration
├── report.html                      # pytest-html report
└── pyproject.toml                   # Project metadata and scripts
```

## Setup & Installation
Requirements:
- Python 3.13
- PDM (recommended)

Install dependencies:
- `pdm run install-deps`

Optional (for Playwright browser setup):
- `pdm run playwright-install`

## Running Tests
- `pdm run test-all`

Other available scripts are defined in [pyproject.toml](pyproject.toml).

## Reporting
- pytest-html report: report.html (root)
- Allure results: allure-results/
- Generate Allure report: `pdm run allure-generate`
- Allure report output: docs/reports/index.html

## Configuration
Configuration classes live in src/qa_automation_python_demo/*_configuration.py
and corresponding ini files are in
src/qa_automation_python_demo/configurations/.

## Logging
Logging is configured via logging.ini. Test runs also write to pytest.log.

## Contributing / Development Notes
- Follow existing step-based patterns in tests/*_tests.py.
- Keep naming and formatting aligned with the current codebase.