# qa-automation-python-demo Architecture

## Architecture Style

**Pattern**: Layered test automation architecture with BDD-style steps.

## Layer Structure

### Tests Layer
- **Responsibility**: Define scenarios, compose sections, drive execution.
- **Location**: tests/
- **Components**: *Tests classes extending SeleniumTests, PlaywrightTests, RestTests.

### Steps Layer
- **Responsibility**: Encapsulate UI/API actions and assertions; provide fluent Given/When/Then chaining.
- **Location**: src/qa_automation_python_demo/*_steps.py
- **Components**: SeleniumSteps, PlaywrightSteps, RestSteps subclasses.

### Configuration Layer
- **Responsibility**: Environment and endpoint configuration loaded from .ini files.
- **Location**: src/qa_automation_python_demo/*_configuration.py and src/qa_automation_python_demo/configurations/*.ini
- **Components**: SeleniumConfiguration, PlaywrightConfiguration, RestConfiguration subclasses.

### Model Layer
- **Responsibility**: Domain objects used by tests and steps.
- **Location**: src/qa_automation_python_demo/model/**
- **Components**: dataclasses for credentials, users, and API payloads.

### Matchers/Utilities
- **Responsibility**: Assertions and tracing, imported from qa-testing-utils and hamcrest.
- **Location**: External dependency usage within tests and steps.

## Dependency Rules

### Allowed
- Tests → Steps
- Tests → Configurations
- Tests → Models
- Steps → Configurations
- Steps → Models
- Steps → External libraries (Selenium/Playwright/requests/Hamcrest)
- Configurations → Models

### Forbidden
- Models → Steps/Tests
- Configurations → Steps/Tests
- Steps → Tests
- Circular dependencies

## Extension Guidelines

### Adding Features
1. Add/extend model objects in src/qa_automation_python_demo/model.
2. Add step methods to corresponding *_steps.py.
3. Add/extend configuration in *_configuration.py and .ini if needed.
4. Add tests in tests/ as *Tests classes using should_* methods.

### Adding Modules
1. Add new configuration + steps pair aligned to Selenium/Playwright/Rest base class.
2. Add configuration .ini under src/qa_automation_python_demo/configurations/.
3. Add tests in tests/ using new steps/configuration.
