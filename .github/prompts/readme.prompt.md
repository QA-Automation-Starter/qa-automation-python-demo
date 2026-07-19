---
description: Generate or update README.md for this repo
---
You are updating this repository's README.md on disk.

Goal: produce a clear, accurate, and concise README for a Python QA automation demo repo. Use existing project facts; do not invent tools, scripts, or features.

Process:
1) Read README.md (if it exists) and update it rather than replacing blindly.
2) Read pyproject.toml, logging.ini, src/qa_automation_python_demo/, tests/, and docs/ (if present) to extract authoritative details (stack, scripts, structure, configuration, reporting).
3) Align content with the project's architecture and conventions.
4) Write the final content to README.md.

Required sections (adapt as needed):
- Project Overview
- Tech Stack (versions when available)
- Project Structure (high-level folders)
- Setup & Installation (prefer PDM, use commands defined in pyproject.toml)
- Running Tests (including available task scripts)
- Reporting (pytest-html and Allure, report output locations)
- Configuration (ini files, env/config locations)
- Logging (logging.ini usage)
- Contributing / Development Notes (keep brief)

Rules:
- Keep it accurate to this repo; if something is unknown, omit it.
- Keep instructions short and actionable.
- Use Markdown headings and bullet lists.
- When referencing paths, use repo-relative paths.
- If you update commands, ensure they match scripts in pyproject.toml.

Output:
- Update README.md in place (on disk).
- Provide a short summary of changes.