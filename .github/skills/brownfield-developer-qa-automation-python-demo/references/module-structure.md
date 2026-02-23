# qa-automation-python-demo Module Structure

## Project Type
**Structure**: Monolith (single Python package + tests)
**Modules**: 2 primary modules

## Module List

| Module | Path | Category | Responsibility |
|--------|------|----------|----------------|
| qa_automation_python_demo | src/qa_automation_python_demo | library | Steps, configurations, and models for UI/REST tests |
| tests | tests | tests | Scenario definitions using pytest |

## Dependencies

```
[tests] --> [qa_automation_python_demo]
[qa_automation_python_demo.steps] --> [qa_automation_python_demo.configurations]
[qa_automation_python_demo.steps] --> [qa_automation_python_demo.model]
[qa_automation_python_demo.configurations] --> [qa_automation_python_demo.model]
```

## Code Placement Guide

| Code Type | Module | Path |
|-----------|--------|------|
| REST endpoint steps | qa_automation_python_demo | src/qa_automation_python_demo/swagger_petstore_steps.py |
| UI steps (Selenium) | qa_automation_python_demo | src/qa_automation_python_demo/terminalx_steps.py |
| UI steps (Playwright) | qa_automation_python_demo | src/qa_automation_python_demo/pw_terminalx_steps.py |
| Selenium configuration | qa_automation_python_demo | src/qa_automation_python_demo/terminalx_configuration.py |
| Playwright configuration | qa_automation_python_demo | src/qa_automation_python_demo/pw_terminalx_configuration.py |
| REST configuration | qa_automation_python_demo | src/qa_automation_python_demo/swagger_petstore_configuration.py |
| Config files | qa_automation_python_demo | src/qa_automation_python_demo/configurations/*.ini |
| Models | qa_automation_python_demo | src/qa_automation_python_demo/model/** |
| Tests | tests | tests/*_tests.py |
