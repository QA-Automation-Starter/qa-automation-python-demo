# qa-automation-python-demo Tech Stack

## Core Stack (Locked)

| Category | Technology | Version | Notes |
|----------|------------|---------|-------|
| Language | Python | $\ge 3.13$ | From pyproject.toml |
| Runtime | CPython | 3.13 | Local/Codespaces |
| Build | PDM | 2.24 (recommended) | Scripts in pyproject.toml |
| Test | pytest | latest | Test discovery via pytest.ini options |
| Reporting | pytest-html | latest | report.html |
| Reporting | allure-pytest | latest | Allure results in allure-results |

## Core Libraries

| Dependency | Version | Purpose |
|------------|---------|---------|
| qa-testing-utils | 0.0.13 | Tracing, matchers, utilities |
| qa-pytest-commons | 0.0.13 | Common types (UiContext, UiElement, By) |
| qa-pytest-rest | 0.0.13 | REST test base classes |
| qa-pytest-webdriver | 0.0.13 | Selenium test base classes |
| qa-pytest-playwright | 0.0.13 | Playwright test base classes |
| PyHamcrest | 2.1.0 | Matchers for assertions |
| requests | transitive | HTTP client for REST steps |

## Development Tools

| Dependency | Version | Purpose |
|------------|---------|---------|
| autopep8 | latest | Formatting (line length 80) |
| isort | latest | Import sorting (black profile) |

## Data Storage

| Type | Technology | Purpose |
|------|------------|---------|
| None | N/A | Tests target external systems (UI/REST) |

## Infrastructure

| Category | Technology | Config |
|----------|------------|--------|
| Logging | Python logging | logging.ini |
| Reporting | Allure | docs/reports (generated) |
| Browser | Selenium WebDriver | Chrome by default, Firefox optional |
| Browser | Playwright | Optional, via playwright install |
