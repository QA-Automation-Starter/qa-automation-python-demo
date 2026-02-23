# qa-automation-python-demo Coding Conventions

## Naming

### Files
| Type | Convention | Example |
|------|------------|---------|
| Python modules | snake_case | terminalx_steps.py |
| Tests | snake_case | swagger_petstore_tests.py |
| Configurations | snake_case | terminalx_configuration.ini |

### Code
| Type | Convention | Example |
|------|------------|---------|
| Classes | PascalCase | TerminalXSteps, SwaggerPetstoreTests |
| Test classes | *Tests suffix | TerminalXTests |
| Test methods | should_* | should_login, should_add |
| Methods/vars | snake_case | searching_for, login_section |
| Constants | UPPER_SNAKE_CASE | (not common in repo) |

## Formatting

- **Tool**: autopep8
- **Config**: pyproject.toml [tool.autopep8]
- **Indentation**: 4 spaces
- **Line length**: 80
- **Quotes**: Mixed, prefer double quotes in XPath strings

## Import Organization
1. Standard library
2. Third-party libraries
3. Internal package imports (qa_automation_python_demo.*)

## Type Hints and Generics
- Use typing annotations (Self, Iterator, List).
- Generic test/step classes with type parameters.

## Comments and Headers
- SPDX license header at top of source files.
- Docstrings for classes and public methods where helpful.

## Git Conventions

### Commit Format
- Not defined in repository.

### Branch Naming
- Not defined in repository.
