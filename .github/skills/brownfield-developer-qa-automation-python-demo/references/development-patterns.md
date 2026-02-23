# qa-automation-python-demo Development Patterns

## Design Patterns

| Pattern | Purpose | Example |
|---------|---------|---------|
| BDD Step Chaining | Fluent Given/When/Then for readability | tests/terminalx_tests.py |
| Service/Adapter | Steps wrap UI/REST operations | *_steps.py subclasses |
| Configuration Object | Load runtime settings from .ini | *_configuration.py + configurations/*.ini |
| Data Transfer Objects | Dataclasses for credentials/users/pets | model/examples/*.py |

## Error Handling

### Exception Hierarchy
- Not customized; relies on underlying libraries and pytest.

### Error Response Format
- REST assertions use Hamcrest matchers on parsed responses.

## Logging

- **Framework**: Python logging
- **Config**: logging.ini
- **Tracing**: qa_testing_utils.Context.traced decorator on step methods

## Testing

### Structure
- tests/*_tests.py with *Tests classes
- Test discovery via pytest.ini options in pyproject.toml

### Unit Test Pattern
- Not used; tests are functional/integration style.

### Integration Test Pattern
1. Instantiate test class via pytest.
2. Use .steps with Given/When/Then chaining.
3. Assertions via Hamcrest matchers (yields_item, contains_string_ignoring_case).

### UI Test Pattern
- SeleniumTests or PlaywrightTests base class
- UiContext from qa-pytest-commons
- Selectors via By.id / By.xpath

### REST Test Pattern
- RestTests base class
- requests.Session in steps
- Request objects with HttpMethod and resource_uri
