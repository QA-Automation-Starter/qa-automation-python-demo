# GitHub Copilot Instructions for qa-automation-python-demo

## Priority Guidelines

When generating code for this repository:

1. **Version Compatibility**: Always detect and respect Python >= 3.13 and exact versions of frameworks and libraries used
2. **Context Files**: Prioritize patterns and standards defined in `.github/skills/brownfield-developer-qa-automation-python-demo/references/`
3. **Codebase Patterns**: When context files don't provide specific guidance, scan the codebase for established patterns
4. **Architectural Consistency**: Maintain the layered, test-driven architecture (Tests → Steps → Configurations → Models)
5. **Code Quality**: Prioritize testability, maintainability, and consistency with existing code patterns

## Technology Stack - Locked Versions

Before generating code, respect these exact dependencies and versions:

### Language & Runtime
- **Python**: >= 3.13 (from pyproject.toml)
- **Runtime**: CPython 3.13

### Core Test Framework & Reporting
- **pytest**: latest (from dev-dependencies)
- **pytest-html**: latest
- **allure-pytest**: latest

### Core Testing Libraries (Locked Versions)
| Dependency | Version | Purpose |
|------------|---------|---------|
| qa-testing-utils | 0.0.13 | Tracing, matchers, utilities |
| qa-pytest-commons | 0.0.13 | Common types (UiContext, UiElement, By) |
| qa-pytest-rest | 0.0.13 | REST test base classes (RestTests, RestSteps) |
| qa-pytest-webdriver | 0.0.13 | Selenium test base classes (SeleniumTests, SeleniumSteps) |
| qa-pytest-playwright | 0.0.13 | Playwright test base classes |
| PyHamcrest | 2.1.0 | Matchers for assertions |
| requests | transitive | HTTP client for REST steps |

### Build & Development Tools
- **PDM**: 2.24 (recommended)
- **autopep8**: latest (line length 80)
- **isort**: latest (black profile, line length 80)

### Configuration
- **Logging**: Python logging via logging.ini
- **Reporting**: pytest-html (report.html) + allure-pytest (allure-results/)

**CRITICAL**: When generating code that uses these libraries, ONLY use APIs and features available in the specified versions. Never suggest features from newer versions.

## Architecture - Layered Test-Driven Design

### Architectural Style
**Pattern**: Layered test automation with BDD-style step chaining. Tests compose actions through steps, which coordinate configurations and models.

### Layer Structure

#### Tests Layer
- **Location**: `tests/`
- **Naming**: `*_tests.py` with `*Tests` classes extending SeleniumTests, PlaywrightTests, or RestTests
- **Responsibility**: Define test scenarios, compose step sections, drive execution
- **Pattern**: 
  - Inherit from SeleniumTests, PlaywrightTests, or RestTests base classes
  - Define `_steps_type` and `_configuration` class attributes
  - Implement test methods named `should_*`
  - Use fluent Given/When/Then chaining: `self.steps.given.*.when.*.then.*`
  - Reusable section methods (e.g., `login_section()`) that return steps for composition
- **Example**: See `tests/terminalx_tests.py`, `tests/swagger_petstore_tests.py`

#### Steps Layer
- **Location**: `src/qa_automation_python_demo/*_steps.py`
- **Naming**: `*Steps` classes extending SeleniumSteps, PlaywrightSteps, or RestSteps
- **Responsibility**: Encapsulate UI/API actions and assertions; enable fluent Given/When/Then chaining
- **Pattern**:
  - Mark class with `@final`
  - All step methods return `Self` to enable chaining
  - Use `@Context.traced` decorator on meaningful actions for logging
  - Given steps: `def <action>(self) -> Self:`
  - When steps: `def <verb>(self, ...) -> Self:`
  - Then steps: `def the_<thing>(self, by_rule: Matcher) -> Self:`
  - Use `adapted_object()` and `adapted_iterator()` to transform elements
  - Hamcrest matchers for assertions (yields_item, contains_string_ignoring_case, etc.)
- **Example**: See `src/qa_automation_python_demo/terminalx_steps.py`, `src/qa_automation_python_demo/swagger_petstore_steps.py`

#### Configuration Layer
- **Location**: `src/qa_automation_python_demo/*_configuration.py` + `src/qa_automation_python_demo/configurations/*.ini`
- **Naming**: `*Configuration` classes extending SeleniumConfiguration, PlaywrightConfiguration, or RestConfiguration
- **Responsibility**: Load and manage environment/endpoint configuration from .ini files
- **Pattern**:
  - Configuration class loads .ini file matching class name
  - Provides properties accessed via `self.configured.<property>`
  - Loaded at test initialization via `_configuration = *Configuration()`
  - Use .ini format for environment variables and endpoints
- **Example**: Configuration classes load `configurations/*.ini` matching their name (e.g., TerminalXConfiguration loads terminalx_configuration.ini)

#### Model Layer
- **Location**: `src/qa_automation_python_demo/model/`
- **Responsibility**: Domain objects (users, credentials, API payloads)
- **Pattern**:
  - Use dataclasses for immutable data transfer objects
  - `model/examples/` contains domain models (TerminalXUser, SwaggerPetstorePet, etc.)
  - Factory methods like `SwaggerPetstorePet.random()` and `SwaggerPetstorePet.from_(response)`
  - Credentials as simple dataclasses

### Dependency Rules - STRICT Enforcement

#### Allowed Dependencies
- Tests → Steps (call step methods)
- Tests → Configurations (instantiate and set via _configuration)
- Tests → Models (use domain objects)
- Steps → Configurations (access via self.configured)
- Steps → Models (receive and return domain objects)
- Steps → External libraries (Selenium, Playwright, requests, Hamcrest, qa-testing-utils)
- Configurations → Models (reference in properties)

#### Forbidden Dependencies - DO NOT VIOLATE
- **Models → Steps/Tests** (models must not know about test logic)
- **Configurations → Steps/Tests** (configs must not orchestrate)
- **Steps → Tests** (steps must not reference test infrastructure)
- **Circular dependencies** (refactor if detected)

### Extension Guidelines

#### Adding New Features
1. **Extend model objects** in `src/qa_automation_python_demo/model/` if new domain concepts needed
2. **Add step methods** to corresponding `*_steps.py` (terminalx_steps, swagger_petstore_steps, pw_terminalx_steps)
3. **Extend configuration** in `*_configuration.py` and corresponding `.ini` file if new settings needed
4. **Add test scenarios** in `tests/` as new `should_*` methods or new test classes
5. **Reuse step sections** across tests via helper methods that return steps (e.g., login_section)

#### Adding New Integration (UI or REST)
1. Create new `*_steps.py` extending appropriate base class (SeleniumSteps, PlaywrightSteps, RestSteps)
2. Create new `*_configuration.py` extending appropriate base class
3. Create new `configurations/*.ini` for settings
4. Create new test class extending appropriate base class (SeleniumTests, PlaywrightTests, RestTests)

## Naming Conventions - Strict Adherence Required

### File Names (snake_case)
| Type | Convention | Example |
|------|------------|---------|
| Step modules | snake_case | `terminalx_steps.py`, `swagger_petstore_steps.py` |
| Configuration modules | snake_case | `terminalx_configuration.py` |
| Test modules | snake_case | `terminalx_tests.py`, `swagger_petstore_tests.py` |
| Configuration files | snake_case | `terminalx_configuration.ini` |

### Classes (PascalCase)
| Type | Convention | Example |
|------|------------|---------|
| Steps classes | PascalCase | `TerminalXSteps`, `SwaggerPetstoreSteps` |
| Configuration classes | PascalCase | `TerminalXConfiguration`, `SwaggerPetstoreConfiguration` |
| Test classes | *Tests suffix | `TerminalXTests`, `SwaggerPetstoreTests` |
| Model classes | PascalCase | `TerminalXUser`, `SwaggerPetstorePet` |

### Methods & Variables (snake_case)
| Type | Convention | Example |
|------|------------|---------|
| Test methods | should_* | `should_login()`, `should_add()`, `should_find()` |
| Step Given | given.<action> | `given.terminalx()`, `given.swagger_petstore()` |
| Step When | when.<verb> | `when.logging_in_with()`, `when.searching_for()`, `when.adding()` |
| Step Then | then.the_<thing> | `then.the_user_logged_in()`, `then.the_available_pets()` |
| Methods/variables | snake_case | `searching_for()`, `login_section()`, `configured`, `ui_context` |
| Constants | UPPER_SNAKE_CASE | (not common in repo, use sparingly) |

### Imports Organization
Always use this order:
1. Standard library imports (`random`, `dataclasses`)
2. Third-party imports (hamcrest, qa-pytest-*, qa-testing-utils, requests)
3. Internal imports (`qa_automation_python_demo.*`)

Examples from codebase:
```python
import random
from typing import Iterator, Self, final

from hamcrest import is_  # type: ignore
from qa_pytest_webdriver import SeleniumTests
from qa_testing_utils import contains_string_ignoring_case, tracing, yields_item

from qa_automation_python_demo.model.examples.terminalx_user import TerminalXUser
from qa_automation_python_demo.terminalx_configuration import TerminalXConfiguration
from qa_automation_python_demo.terminalx_steps import TerminalXSteps
```

## Code Formatting Standards

### Tool Configuration
- **Tool**: autopep8
- **Line Length**: 80 (STRICT - enforce in all generated code)
- **Indentation**: 4 spaces
- **Import Sorting**: isort with black profile
- **Quotes**: Mixed preference; double quotes preferred in XPath strings

### Type Hints
- Use explicit type hints with `typing` module (Self, Iterator, List, etc.)
- Generic test/step classes with type parameters: `SeleniumTests[StepsType, ConfigType]`
- Matcher type hints: `by_rule: Matcher[str]`, `by_rule: Matcher[Iterator[str]]`

### Headers & Comments
- **SPDX License Header**: All source files must start with:
  ```python
  # SPDX-FileCopyrightText: 2025 Adrian Herscu
  #
  # SPDX-License-Identifier: Apache-2.0
  ```
- **Docstrings**: Use for classes and public methods where intent is non-obvious
- **Inline Comments**: Minimize; write self-documenting code

## Testing Patterns - BDD-Style Integration Testing

### Test Structure
- **Discovery**: pytest.ini in pyproject.toml defines:
  - `python_files = "*.py"`
  - `python_classes = "*Tests"`
  - `python_functions = "should_*"`

### Integration Test Pattern (Current Approach)
1. Test class extends appropriate base: SeleniumTests, PlaywrightTests, RestTests
2. Declare `_steps_type = *Steps` and `_configuration = *Configuration()`
3. Compose test via fluent step chaining: `self.steps.given.*.when.*.then.*`
4. Use Hamcrest matchers for assertions
5. Extract reusable sections into helper methods returning steps
6. One test scenario per should_* method

### BDD Given/When/Then Pattern
- **Given**: Setup (e.g., `given.terminalx(driver)`)
- **When**: Action (e.g., `when.logging_in_with(user)`)
- **Then**: Assertion (e.g., `then.the_user_logged_in(is_(username))`)
- All methods return `Self` for chaining

### Assertion Matchers
Use Hamcrest matchers exclusively:
- `is_(value)` for equality
- `contains_string_ignoring_case(text)` for text matching
- `yields_item(matcher)` for collection items
- `tracing(matcher)` for logging during assertion

**Example from codebase**:
```python
def should_login(self):
    self.login_section(random.choice(self._configuration.users))

def login_section(self, user: TerminalXUser) -> TerminalXSteps:
    return (self.steps
            .given.terminalx(self.ui_context)
            .when.logging_in_with(user.credentials)
            .then.the_user_logged_in(is_(user.name)))
```

## Development Patterns - Proven Approaches

### Design Patterns in Use
| Pattern | Purpose | Where |
|---------|---------|-------|
| BDD Step Chaining | Fluent Given/When/Then | All tests and steps |
| Service/Adapter | Steps wrap UI/REST operations | *_steps.py classes |
| Configuration Object | Runtime settings from .ini | *_configuration.py |
| Data Transfer Objects | Domain models | `model/examples/*.py` |

### Error Handling
- Rely on underlying libraries (pytest, Selenium, requests)
- Let exceptions propagate (pytest captures and reports)
- Use Hamcrest matchers for assertion clarity

### Logging & Tracing
- **Framework**: Python logging via `logging.ini`
- **Tracing**: Apply `@Context.traced` decorator to meaningful step methods
- **Usage**: Automatically logs entry/exit with context

Example from codebase:
```python
@Context.traced
def logging_in_with(self, credentials: TerminalXCredentials) -> Self:
    return (self.clicking_login()
            .and_.typing(By.id("qa-login-email-input"), credentials.username)
            # ...
```

## Configuration Management

### .ini File Format
Configuration files in `src/qa_automation_python_demo/configurations/` follow ini format:
- Sections: `[section_name]`
- Properties: `key = value`
- Accessed via `self.configured.<property>` in steps

### Environment-Specific Configuration
Configuration classes extend base classes and load corresponding .ini files:
- TerminalXConfiguration → terminalx_configuration.ini
- SwaggerPetstoreConfiguration → swagger_petstore_configuration.ini
- RestConfiguration subclasses → respective .ini files

## Documentation Standards

### Documentation Level: Standard

### What to Document
- **Classes**: Document purpose, base class responsibility
- **Public Methods**: Document purpose and parameters in methods with non-obvious behavior
- **Parameters**: Document types and constraints
- **Return Values**: Implied by return type and method naming (should_* → None, step methods → Self)

### Example from Codebase
Most code is self-documenting via:
- Clear naming (`should_login`, `the_user_logged_in`)
- Type hints (`Matcher[str]`, `Iterator[SwaggerPetstorePet]`)
- Method chaining patterns
- Minimal inline comments

### When to Add Docstrings
- Complex configuration loading logic
- Non-obvious Hamcrest matcher usage
- Edge cases in step implementations

## Python-Specific Guidelines

### Python Version: >= 3.13
- **Feature Ceiling**: Only use Python 3.13 features and libraries compatible with 3.13
- **Type Hints**: Use `typing.Self`, `typing.Iterator`, `typing.final` (3.13+)
- **Dataclasses**: Prefer dataclasses over manual __init__ for models
- **Type Generics**: Use in test/step class definitions: `SeleniumTests[StepsType, ConfigType]`

### Import Conventions
- Use `from typing import Self, Iterator, final` for type hints
- Use `from dataclasses import asdict, dataclass` for models
- Hamcrest imports: `from hamcrest import is_  # type: ignore`
- qa-testing-utils: `from qa_testing_utils import Context, adapted_object, adapted_iterator`
- qa-pytest-commons: `from qa_pytest_commons import By, UiContext, UiElement`

### Pattern Examples from Actual Code

**Step with Chaining and Tracing:**
```python
from typing import Self, final
from qa_testing_utils import Context

@final
class TerminalXSteps(SeleniumSteps[TerminalXConfiguration]):
    @Context.traced
    def logging_in_with(self, credentials: TerminalXCredentials) -> Self:
        return (self.clicking_login()
                .and_.typing(By.id("qa-login-email-input"), credentials.username)
                .and_.typing(By.id("qa-login-password-input"), credentials.password)
                .and_.submitting_login())
```

**Test with Composition:**
```python
def should_login(self):
    self.login_section(random.choice(self._configuration.users))

def login_section(self, user: TerminalXUser) -> TerminalXSteps:
    return (self.steps
            .given.terminalx(self.ui_context)
            .when.logging_in_with(user.credentials)
            .then.the_user_logged_in(is_(user.name)))
```

**REST Step with Adapted Objects:**
```python
@Context.traced
def the_available_pets(self, by_rule: Matcher[Iterator[SwaggerPetstorePet]]) -> Self:
    return self.the_invocation(Request(
        method=HttpMethod.GET,
        url=self.configured.resource_uri(path="pet/findByStatus"),
        params={"status": "available"}),
        adapted_object(lambda response: SwaggerPetstorePet.from_(response), by_rule))
```

## Brownfield Principles - Core Values

1. **Respect Existing Architecture**: Follow the layered pattern; don't "improve" the structure
2. **Code Reuse First**: Search for existing patterns before creating new code
3. **Forward Compatibility**: Don't break existing tests, steps, or configurations
4. **Refactor On-Demand**: Only refactor when necessary for clarity or to fix bugs
5. **Style Consistency**: Match existing code style and patterns exactly

## General Best Practices

### When Generating Code
1. **Scan Similar Files First**: Look at existing `*_tests.py`, `*_steps.py`, `*_configuration.py` for patterns
2. **Follow Naming Convention Exactly**: Match case, prefixes, suffixes from existing code
3. **Match Step Pattern**: All steps return `Self`, use `@Context.traced`, use fluent chaining
4. **Reuse Configuration Pattern**: Extend appropriate base class, create matching .ini file
5. **Apply Type Hints**: Use `Self`, `Matcher[T]`, generic type parameters
6. **Format to 80 Chars**: Respect line length limit
7. **Add SPDX Header**: All new Python files start with license header
8. **Use Hamcrest**: For all assertions in tests and steps

### Code Quality Checklist
- [ ] Follows naming convention (snake_case files, PascalCase classes)
- [ ] Imports organized: stdlib → third-party → internal
- [ ] Type hints present and accurate
- [ ] Line length ≤ 80 characters
- [ ] Steps return `Self` for chaining
- [ ] Configuration loaded from .ini file
- [ ] Models are dataclasses
- [ ] Test methods named `should_*`
- [ ] SPDX header present
- [ ] No cross-layer dependencies violated

## Project-Specific Guidance

### Before Generating Any Code
1. **Examine Similar Existing Code**: Look at `terminalx_tests.py`, `swagger_petstore_tests.py`, etc.
2. **Check Architectural Layer**: Determine if adding to Tests, Steps, Configurations, or Models
3. **Verify No Duplication**: Search for existing patterns that can be reused
4. **Respect Version Constraints**: Never use features beyond Python 3.13 or library versions listed

### Handling Ambiguity
- When requirements are unclear, refer to existing test patterns in `tests/`
- For EARS-style requirements, consult `.github/skills/brownfield-ears/`
- When in doubt, match the style of the most similar existing code

### Testing Integration Code
- Focus on integration testing (current project approach)
- Use fluent BDD patterns (Given/When/Then)
- Compose reusable step sections for code sharing
- Use Hamcrest matchers for clarity

---

**Generated from**: Blueprint generator + actual codebase analysis
**Last Updated**: 2025-02-23
**Reference**: `.github/skills/brownfield-developer-qa-automation-python-demo/`
