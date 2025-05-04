# Python Selenium Example Project

This is a minimal Python test automation project using **Selenium WebDriver** and **pytest**, structured to demonstrate clean, readable test code with a focus on search functionality and API-driven operations.

## Features

- ✅ Easy-to-read step-based test structure
- ✅ Pytest integration for flexible test discovery
- ✅ Selenium WebDriver example with Chrome
- ✅ REST API example
- ✅ GitHub Codespaces-compatible development container

## Project Structure

```
python-selenium/
├── .devcontainer/       # Development container setup for Codespaces
├── src/                 # Support code
├── tests/               # Test cases organized by feature
│   └── test_example.py  # Contains functional tests
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Project metadata
```

## Quick Start (Locally)

1. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the tests:
   ```bash
   pytest -v
   ```

## Using in GitHub Codespaces

This repository is fully configured to run in **GitHub Codespaces**:
- Python 3.13
- GitHub CLI

No setup is needed—just open in Codespaces and start coding.

> NOTE: Selenium tests will not work here, unless changed to work with
> SauceLabs, or similar remote browser testing service.


## Reports

1. `report.html` is generated in root-folder, just open it in a Web-browser
2. `allure-results` -- this requires running the Allure server

## Example Tests

```python
def should_find(self):
    self.login_section(random.choice(self._configuration.users))
    for word in ["hello", "kitty"]:
        (self.steps
            .when.searching_for(word)
            .then.the_search_hints(
                yields_item(contains_string_ignoring_case(word))))
```

```python
def should_add(self):
    random_pet = SwaggerPetstorePet.random()
    (self.steps
        .when.adding(random_pet)
        .then.the_available_pets(yields_item(is_(random_pet))))
```

## Requirements

- Python 3.10+
- Google Chrome (with drivers)

## TODO

- Add GitHub Actions workflow for CI
- Add browser matrix support (Safari, Edge)
- Extend test coverage (API + UI)