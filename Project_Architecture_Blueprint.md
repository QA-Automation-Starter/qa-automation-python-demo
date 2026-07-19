# Project Architecture Blueprint

**Project**: qa-automation-python-demo  
**Generated**: February 23, 2026  
**Technology**: Python ≥ 3.13  
**Primary Pattern**: Layered Test Automation Architecture with BDD-Style Steps

---

## 1. Architecture Detection and Analysis

### Technology Stack Identification
Analysis of the project structure reveals:

- **Primary Language**: Python 3.13+
- **Build System**: PDM (Python Development Master) with scripts defined in `pyproject.toml`
- **Test Framework**: pytest with custom discovery options
- **UI Automation**: 
  - Selenium WebDriver (primary)
  - Playwright (secondary)
- **API Automation**: requests library wrapped in REST steps
- **Assertion Library**: PyHamcrest for fluent, readable matchers
- **Reporting**: 
  - pytest-html (HTML reports)
  - allure-pytest (Allure framework integration)
- **Custom Libraries**: 
  - qa-testing-utils (0.0.13) - tracing, matchers, utilities
  - qa-pytest-commons (0.0.13) - shared types and context
  - qa-pytest-rest (0.0.13) - REST test base classes
  - qa-pytest-webdriver (0.0.13) - Selenium base classes
  - qa-pytest-playwright (0.0.13) - Playwright base classes

### Architectural Pattern Detection
The codebase implements a **Layered Test Automation Architecture** with the following characteristics:

- **Folder Organization**: Clear separation between `tests/` and `src/qa_automation_python_demo/`
- **Dependency Flow**: Tests → Steps → Configurations/Models (unidirectional, top-down)
- **Interface Segregation**: Each application under test (AUT) has dedicated Steps and Configuration classes
- **Communication Mechanisms**: BDD-style fluent chaining through `given.when.then.and_` methods
- **Abstraction Pattern**: Framework-provided base classes (SeleniumTests, PlaywrightTests, RestTests) extended per AUT

---

## 2. Architectural Overview

### Core Principles

1. **Separation of Concerns**: Tests define scenarios; Steps encapsulate actions; Configurations manage environment settings; Models represent domain objects
2. **Fluent Readability**: BDD-style method chaining (Given/When/Then/And) makes test intentions clear
3. **Framework Abstraction**: Common test automation patterns abstracted into reusable base classes from qa-pytest-* libraries
4. **Configuration-Driven**: Runtime behavior controlled via INI files, enabling environment flexibility
5. **Type Safety**: Extensive use of Python type hints and generics for compile-time validation

### Architectural Boundaries

- **Tests ↔ Steps**: Tests compose steps but never implement actions directly
- **Steps ↔ Framework**: Steps wrap framework-specific operations (Selenium/Playwright/requests)
- **Configuration ↔ Environment**: Configuration classes load settings from INI files, isolating environment concerns
- **Models ↔ Data**: Dataclasses represent domain entities, used by both tests and steps

### Enforcement Mechanisms

- **Import rules**: Tests import steps and configurations but not vice versa
- **Base class hierarchy**: Enforces correct typing and framework integration
- **Generic type parameters**: Ensures type consistency between Tests, Steps, and Configurations

### Hybrid Patterns

The architecture combines:
- **Layered Architecture** for separation of concerns
- **BDD (Behavior-Driven Development)** for test expressiveness
- **Service/Adapter Pattern** where steps adapt UI/API frameworks
- **Configuration Object Pattern** for environment management

---

## 3. Architecture Visualization

### High-Level Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Tests Layer                          │
│  (pytest discovery, scenario definitions, *Tests classes)  │
└────────────────────────┬────────────────────────────────────┘
                         │ depends on
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                        Steps Layer                          │
│   (BDD actions, Given/When/Then, framework wrapping)       │
└──────────────┬──────────────────────────────┬───────────────┘
               │ depends on                   │ depends on
               ▼                              ▼
┌──────────────────────────┐   ┌──────────────────────────────┐
│  Configuration Layer     │   │      Model Layer             │
│  (Environment settings,  │   │  (Domain objects,            │
│   INI file loading)      │   │   dataclasses)               │
└──────────────────────────┘   └──────────────────────────────┘
```

### Component Interaction Diagram

```
┌──────────────────┐
│  AmazonTests     │
│  (extends        │
│   SeleniumTests) │
└────────┬─────────┘
         │ uses
         ▼
┌──────────────────────────┐     ┌──────────────────────────┐
│  AmazonSteps             │────▶│  AmazonConfiguration     │
│  (extends SeleniumSteps) │ uses│  (extends                │
└────────┬─────────────────┘     │   SeleniumConfiguration) │
         │                       └──────────────────────────┘
         │ wraps                              │ loads
         ▼                                    ▼
┌──────────────────┐              ┌──────────────────────────┐
│  Selenium        │              │  amazon_configuration    │
│  WebDriver API   │              │  .ini                    │
└──────────────────┘              └──────────────────────────┘
```

### Data Flow Diagram

```
Test Execution Flow:

1. pytest discovers tests/*_tests.py
   │
2. Test class instantiated with:
   ├─ _steps_type (e.g., AmazonSteps)
   └─ _configuration (e.g., AmazonConfiguration())
   │
3. Configuration loads settings from INI
   │
4. Test method invokes: self.steps.given.amazon(ui_context)
   │
5. Step chain executes:
   given.amazon(ctx) → when.searching_for("text") → then.signin_required()
   │
6. Each step method:
   ├─ Decorated with @Context.traced (logging)
   ├─ Interacts with WebDriver/Session
   └─ Returns Self for chaining
   │
7. Assertions use Hamcrest matchers
   │
8. Results captured by pytest-html and allure-pytest
```

---

## 4. Core Architectural Components

### 4.1 Tests Layer

**Purpose and Responsibility**:
- Define test scenarios as executable specifications
- Compose step chains to create meaningful test flows
- Trigger test execution via pytest
- Provide setup/teardown for test resources (WebDriver, requests.Session)

**Internal Structure**:
- Test classes extend framework base classes: `SeleniumTests`, `PlaywrightTests`, or `RestTests`
- Each test class declares:
  - `_steps_type`: The Steps class to instantiate
  - `_configuration`: The Configuration instance to use
- Test methods named with `should_*` prefix (pytest discovery pattern)
- Optional `setup_method()` override for custom initialization

**Interaction Patterns**:
- Access steps via `self.steps` property (inherited from base test class)
- Access UI context via `self.ui_context` (for UI tests)
- Access REST session via `self._rest_session` (for REST tests)
- Fluent chaining: `self.steps.given.X().when.Y().then.Z()`

**Evolution Patterns**:
- New test scenarios: Add `should_*` methods to existing test class
- New AUT (Application Under Test): Create new `*Tests` class extending appropriate base
- Custom WebDriver setup: Override `setup_method()`

**Example**:
```python
class AmazonTests(SeleniumTests[AmazonSteps[AmazonConfiguration], AmazonConfiguration]):
    _steps_type = AmazonSteps
    _configuration = AmazonConfiguration()

    def should_checkout(self):
        (self.steps
         .given.amazon(self.ui_context)
         .when.searching_for("mobile phone")
         .and_.selecting_result(2)
         .and_.adding_to_cart()
         .and_.proceed_to_checkout()
         .then.signin_required())
```

---

### 4.2 Steps Layer

**Purpose and Responsibility**:
- Encapsulate UI/API actions as reusable, atomic operations
- Provide BDD-style fluent interface (given/when/then/and_)
- Wrap framework-specific APIs (Selenium, Playwright, requests)
- Implement assertions using Hamcrest matchers
- Trace execution for debugging and reporting

**Internal Structure**:
- Step classes extend framework base: `SeleniumSteps`, `PlaywrightSteps`, or `RestSteps`
- Generic type parameter specifies Configuration type
- Each method decorated with `@Context.traced` for automatic logging
- Methods return `Self` to enable chaining
- Helper methods from base classes: `typing()`, `clicking()`, `the_element()`, `invoking()`, `the_invocation()`

**Interaction Patterns**:
- Initialized by test framework with configuration instance
- Access configuration via `self.configured` property
- Receive driver/session from test via initial step method (e.g., `amazon(driver)`)
- Chain methods inherit context (driver/session) through instance state

**Evolution Patterns**:
- New actions: Add methods to existing Steps class
- New AUT: Create new Steps class extending appropriate base
- Complex flows: Compose multiple step methods
- Custom assertions: Use `adapted_object()` with Hamcrest matchers

**Example**:
```python
class AmazonSteps[TConfiguration: AmazonConfiguration](SeleniumSteps[TConfiguration]):
    @Context.traced
    def amazon(self, driver: UiContext[UiElement]) -> Self:
        return self.ui_context(driver).at(self.configured.entry_point)

    @Context.traced
    def searching_for(self, text: str) -> Self:
        return (self.typing(By.id("twotabsearchtextbox"), text)
                .and_.clicking(By.id("nav-search-submit-button")))

    @Context.traced
    def signin_required(self) -> Self:
        return self.the_element(
            By.id("signin-heading"),
            adapted_object(lambda element: element.text, is_("Sign in")))
```

---

### 4.3 Configuration Layer

**Purpose and Responsibility**:
- Load environment-specific settings from INI files
- Provide runtime configuration to steps
- Manage base URLs, credentials, timeouts, and other settings
- Enable environment switching without code changes

**Internal Structure**:
- Configuration classes extend framework base: `SeleniumConfiguration`, `PlaywrightConfiguration`, or `RestConfiguration`
- Inherit `parser` property (ConfigParser instance) from base class
- INI files stored in `src/qa_automation_python_demo/configurations/`
- Minimal implementation - most logic in base classes

**Interaction Patterns**:
- Instantiated by test class as class-level attribute
- Accessed by steps via `self.configured`
- Base classes provide properties like `entry_point`, `base_url`, `resource_uri(path)`
- Custom properties can be added by reading from `self.parser`

**Evolution Patterns**:
- New settings: Add to INI file and access via `self.configured.parser`
- New AUT: Create Configuration class + INI file
- Environment variants: Maintain separate INI files or use environment variables

**Example**:
```python
# amazon_configuration.py
class AmazonConfiguration(SeleniumConfiguration):
    pass

# configurations/amazon_configuration.ini
[ui]
entry_point = https://www.amazon.com

[users]
test_user = user@example.com:password123
```

---

### 4.4 Model Layer

**Purpose and Responsibility**:
- Define domain objects used by tests and steps
- Provide type-safe data structures with Python dataclasses
- Encapsulate serialization/deserialization logic
- Generate test data (e.g., random instances)

**Internal Structure**:
- Location: `src/qa_automation_python_demo/model/`
- Organization: 
  - `model/credentials.py` - Authentication data
  - `model/examples/*_credentials.py` - AUT-specific credentials
  - `model/examples/*_user.py` - User domain objects
  - `model/examples/*_pet.py` - API domain objects
- Decorated with `@dataclass` and `@to_string()` (from qa-testing-utils)
- Implement factory methods: `random()`, `from_(response)`

**Interaction Patterns**:
- Imported by both tests and steps
- Used for method parameters and return values
- Serialized via `asdict()` for API requests
- Deserialized via static `from_()` methods

**Evolution Patterns**:
- New domain objects: Create dataclass in `model/examples/`
- Data factories: Add static methods to dataclass
- Complex transformations: Add instance methods or utility functions

**Example**:
```python
@dataclass(eq=True, frozen=True)
@to_string()
class SwaggerPetstorePet:
    name: str
    status: str

    @staticmethod
    def random() -> SwaggerPetstorePet:
        return SwaggerPetstorePet(name=str(uuid4()), status="available")

    @staticmethod
    def from_(response: Response) -> Iterator[SwaggerPetstorePet]:
        return (
            SwaggerPetstorePet(name=pet["name"], status=pet["status"])
            for pet in response.json()
            if "name" in pet and "status" in pet
        )
```

---

## 5. Architectural Layers and Dependencies

### Layer Structure

```
┌──────────────────────────────────────────────────┐
│ Tests Layer                                      │  ← pytest entry point
│ (tests/*.py)                                     │
└────────┬─────────────────────────────────────────┘
         │ depends on ↓
┌────────▼─────────────────────────────────────────┐
│ Steps Layer                                      │  ← Action encapsulation
│ (src/qa_automation_python_demo/*_steps.py)      │
└────────┬──────────────────────────┬──────────────┘
         │                          │
         │ depends on ↓             │ depends on ↓
┌────────▼──────────────┐   ┌───────▼──────────────┐
│ Configuration Layer   │   │ Model Layer          │
│ (*_configuration.py + │   │ (model/*.py)         │
│  configurations/*.ini)│   │                      │
└───────────────────────┘   └──────────────────────┘
```

### Dependency Rules

**Allowed**:
- Tests → Steps (compose step chains)
- Tests → Configurations (declare `_configuration`)
- Tests → Models (create domain objects)
- Steps → Configurations (access via `self.configured`)
- Steps → Models (method parameters and return values)
- Steps → External libraries (Selenium, Playwright, requests, Hamcrest)
- Configurations → Models (load credentials, parse complex settings)

**Forbidden** (enforced by convention and imports):
- Models → Steps/Tests (models are pure data)
- Configurations → Steps/Tests (configurations are passive)
- Steps → Tests (steps don't know about test structure)
- Circular dependencies between any layers

### Abstraction Mechanisms

1. **Generic Type Parameters**: 
   - Tests declare `SeleniumTests[AmazonSteps[AmazonConfiguration], AmazonConfiguration]`
   - Ensures type consistency across layers

2. **Base Classes from qa-pytest Libraries**:
   - `SeleniumTests`, `PlaywrightTests`, `RestTests` provide common test setup
   - `SeleniumSteps`, `PlaywrightSteps`, `RestSteps` provide common step operations
   - `SeleniumConfiguration`, `PlaywrightConfiguration`, `RestConfiguration` provide configuration loading

3. **Property Access**:
   - `self.steps` in tests provides access to steps instance
   - `self.configured` in steps provides access to configuration

4. **Dependency Injection**:
   - Configuration instance created by test class
   - Injected into steps by framework base class
   - Driver/session passed from test to steps via initial step method

### Layer Violations

**None detected** - The codebase adheres to strict layering:
- No backward dependencies observed
- No circular imports
- Configuration and models are properly isolated

---

## 6. Data Architecture

### Domain Model Structure

The domain model is organized by Application Under Test (AUT):

```
model/
├── credentials.py                          # Generic credentials dataclass
└── examples/
    ├── swagger_petstore_credentials.py     # API-specific credentials
    ├── swagger_petstore_pet.py             # Pet domain object
    ├── terminalx_credentials.py            # UI-specific credentials
    └── terminalx_user.py                   # User domain object
```

### Entity Relationships

- **Credentials**: Generic authentication data (username + password)
  - Factory method: `from_(colon_separated_string)`
  
- **SwaggerPetstorePet**: API domain object
  - Fields: name, status
  - Factory methods: `random()`, `from_(response)`
  - Immutable (`frozen=True`)

- **No entity relationships** - Domain objects are independent (no foreign keys or references)

### Data Access Patterns

**No traditional data access layer** - This is a test automation framework that interacts with external systems:

- **UI Data Access**: Steps use Selenium/Playwright to read from web pages
- **API Data Access**: Steps use requests library to call REST endpoints
- **Configuration Data Access**: Configurations load from INI files via ConfigParser

### Data Transformation Patterns

1. **Request Serialization**:
   ```python
   def adding(self, pet: SwaggerPetstorePet) -> Self:
       return self.invoking(Request(
           method=HttpMethod.POST,
           url=self.configured.resource_uri(path="pet"),
           json=asdict(pet)  # dataclass → dict → JSON
       ))
   ```

2. **Response Deserialization**:
   ```python
   @staticmethod
   def from_(response: Response) -> Iterator[SwaggerPetstorePet]:
       return (
           SwaggerPetstorePet(name=pet["name"], status=pet["status"])
           for pet in response.json()  # JSON → dict → dataclass
       )
   ```

3. **String Parsing**:
   ```python
   @classmethod
   def from_(cls, colon_separated: str):
       return cls(*colon_separated.split(":"))  # "user:pass" → Credentials
   ```

### Caching Strategies

**No caching implemented** - Each test run starts fresh:
- WebDriver instances created per test method
- requests.Session created per test method
- Configuration loaded once per test class

### Data Validation Patterns

1. **Type Hints**: Python type annotations provide compile-time validation
2. **Dataclass Validation**: `@dataclass` ensures fields are initialized correctly
3. **Hamcrest Matchers**: Runtime assertions validate data shape and values
   ```python
   .then.the_available_pets(yields_item(tracing(is_(random_pet))))
   ```

---

## 7. Cross-Cutting Concerns Implementation

### 7.1 Authentication & Authorization

**Security Model**:
- Credentials stored in INI files (not in code)
- Format: `username:password` strings
- Loaded via `Credentials.from_(config_value)`

**Permission Enforcement**:
- Not enforced in framework - tests interact with AUT as configured user
- Test scenarios validate authentication flows (e.g., `signin_required()`)

**Identity Management**:
- Managed by Applications Under Test
- Tests verify authentication redirects and access controls

**Example**:
```python
# configurations/terminalx_configuration.ini
[users]
checker = Checking2@percepti.co:Checking2@percepti.c
per = Checking@percepti.co:Checking@percepti.c1
```

---

### 7.2 Error Handling & Resilience

**Exception Handling**:
- Relies on pytest and underlying framework error handling
- No custom exception hierarchy
- Framework exceptions (WebDriverException, RequestException) propagate to pytest

**Retry Patterns**:
- Not implemented in current codebase
- Could be added via decorators on step methods

**Resilience Strategies**:
- Selenium/Playwright implicit waits (configured in base classes)
- Explicit waits via framework helper methods

**Error Reporting**:
- pytest captures exceptions and generates reports
- Allure captures screenshots and logs on failure
- Tracing decorator logs method entry/exit

---

### 7.3 Logging & Monitoring

**Instrumentation Pattern**:
- `@Context.traced` decorator on all step methods
- Logs method entry/exit with parameters
- Integrated with Python logging framework

**Configuration**:
```ini
# logging.ini
[logger_root]
level=DEBUG
handlers=console,overwrite_file

[handler_overwrite_file]
class=FileHandler
args=('pytest.log', 'w')
```

**Observability**:
- Console output (real-time)
- File logging (`pytest.log` - overwritten per run)
- Allure attachments (screenshots, HTML, network logs)

**Performance Monitoring**:
- Not explicitly implemented
- Could be added via timing decorators or custom pytest hooks

---

### 7.4 Validation

**Input Validation**:
- Python type hints provide compile-time checks
- Dataclasses ensure required fields
- No runtime validation beyond type checking

**Business Rule Validation**:
- Implemented in test assertions
- Uses Hamcrest matchers for expressive validation:
  ```python
  .then.the_available_pets(yields_item(is_(expected_pet)))
  ```

**Validation Responsibility**:
- Tests validate expected behavior
- Steps validate interaction success (element found, request completed)
- Models validate data structure via dataclass constraints

**Error Reporting**:
- Hamcrest matchers provide descriptive failure messages
- pytest formats assertion errors with context

---

### 7.5 Configuration Management

**Configuration Sources**:
1. INI files in `src/qa_automation_python_demo/configurations/*.ini`
2. Command-line options via pytest (e.g., `--config selenium:browser_type=firefox`)
3. Environment variables (not heavily used)

**Environment-Specific Configuration**:
- Different INI files per AUT
- Potential for environment-specific INI variants (dev/staging/prod)

**Secret Management**:
- Credentials in INI files (should be externalized for production)
- Not using environment variables or secret stores currently

**Feature Flags**:
- Not implemented
- Could be added via configuration parser

---

## 8. Service Communication Patterns

### Service Boundaries

The framework interacts with external services:
- **UI Services**: Web applications via Selenium/Playwright
- **REST Services**: APIs via requests library

### Communication Protocols

1. **Selenium WebDriver**:
   - Protocol: JSON Wire Protocol / W3C WebDriver
   - Format: JSON
   - Communication: Synchronous HTTP requests to WebDriver server

2. **Playwright**:
   - Protocol: Chrome DevTools Protocol (CDP)
   - Format: JSON
   - Communication: WebSocket to browser

3. **REST APIs**:
   - Protocol: HTTP/HTTPS
   - Format: JSON (typically)
   - Communication: Synchronous requests via requests library

### Synchronous vs Asynchronous

**All communication is synchronous**:
- Test execution waits for step completion
- Steps wait for WebDriver/API responses
- No async/await patterns used

### API Versioning

**REST Steps**:
- Base URL includes version: `https://petstore.swagger.io/v2/`
- No explicit version negotiation
- Changes would require new Configuration/Steps classes

### Service Discovery

- **Hardcoded endpoints** in INI files
- No dynamic service discovery
- Configuration determines target environment

### Resilience Patterns

1. **Implicit Waits**: Selenium/Playwright wait for elements
2. **No Circuit Breakers**: Failures propagate immediately
3. **No Fallbacks**: Test fails if service unavailable

---

## 9. Python Architectural Patterns

### Application Bootstrap

**Test Discovery**:
```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
python_files = "*.py"
python_classes = "*Tests"
python_functions = "should_*"
```

**Entry Point**:
- pytest discovers test classes
- Test classes instantiated by pytest
- `setup_method()` called before each test
- `teardown_method()` called after each test (inherited from base)

### Dependency Injection

**Manual Constructor Injection**:
```python
class AmazonTests(SeleniumTests[AmazonSteps[AmazonConfiguration], AmazonConfiguration]):
    _steps_type = AmazonSteps  # Class reference
    _configuration = AmazonConfiguration()  # Instance
```

**Framework-Provided Injection**:
- Base test class instantiates steps with configuration
- Steps receive configuration via constructor (in base class)
- Driver/session passed to first step method by test

### Module Organization

**Package Structure**:
```
src/qa_automation_python_demo/
├── __init__.py
├── amazon_configuration.py
├── amazon_steps.py
├── pw_terminalx_configuration.py
├── pw_terminalx_steps.py
├── swagger_petstore_configuration.py
├── swagger_petstore_steps.py
├── terminalx_configuration.py
├── terminalx_steps.py
├── configurations/
│   ├── amazon_configuration.ini
│   ├── pw_terminalx_configuration.ini
│   ├── swagger_petstore_configuration.ini
│   └── terminalx_configuration.ini
└── model/
    ├── credentials.py
    └── examples/
        ├── swagger_petstore_credentials.py
        ├── swagger_petstore_pet.py
        ├── terminalx_credentials.py
        └── terminalx_user.py
```

**Naming Convention**:
- Configuration + Steps pairs share prefix (e.g., `amazon_*`)
- Suffixes indicate component type (`_configuration.py`, `_steps.py`, `_tests.py`)

### OOP vs Functional

**Primarily Object-Oriented**:
- Tests, Steps, Configurations are classes
- Inheritance from framework base classes
- Generic type parameters for type safety

**Functional Elements**:
- Dataclasses (data-oriented, no behavior)
- Static methods for factories
- Generator expressions for data transformation

### Asynchronous Programming

**Not Used**:
- All operations are synchronous
- No `async`/`await` keywords
- Threading/multiprocessing not used

---

## 10. Implementation Patterns

### 10.1 Interface Design Patterns

**Base Class Abstraction**:
- Framework provides base classes (SeleniumSteps, RestSteps, etc.)
- Concrete implementations extend with AUT-specific methods
- Minimal interface - extend as needed

**Generic Interfaces**:
```python
class AmazonSteps[TConfiguration: AmazonConfiguration](SeleniumSteps[TConfiguration]):
    # TConfiguration ensures type consistency
```

**Method Chaining Interface**:
- All step methods return `Self`
- Enables fluent `.given.when.then.and_` chaining
- Base classes provide `given`, `when`, `then`, `and_` properties (all return `self`)

---

### 10.2 Service Implementation Patterns

**Service Lifetime**:
- Steps instance: Created per test method (via `self.steps` property)
- Configuration instance: Created once per test class (class attribute)
- Driver/Session: Created per test method in `setup_method()`

**Service Composition**:
- Tests compose steps via method chaining
- Steps compose base class helper methods
- No service-to-service calls

**Operation Implementation Template**:
```python
@Context.traced
def action_name(self, param: Type) -> Self:
    # 1. Perform action via framework
    # 2. Optionally chain more actions
    # 3. Return self for chaining
    return self.helper_method(locator, value).and_.another_method()
```

**Error Handling**:
- Framework exceptions propagate to pytest
- No try/catch in step methods
- `@Context.traced` logs exceptions

---

### 10.3 Repository Implementation Patterns

**Not Applicable** - No data persistence layer in this test automation framework.

Alternative interpretation (Configuration as "repository" for settings):

**Configuration Loading Pattern**:
```python
class SwaggerPetstoreConfiguration(RestConfiguration):
    pass  # Inherits parser logic from base class
```

**Data Access**:
```python
# In base class (inherited)
@property
def entry_point(self) -> str:
    return self.parser["ui"]["entry_point"]
```

---

### 10.4 Controller/API Implementation Patterns

**Step Methods as "Controllers"**:
```python
@Context.traced
def searching_for(self, text: str) -> Self:
    # Request validation: parameter type hints
    # Action execution: interact with UI/API
    # Response formatting: return Self for chaining
    return (self.typing(By.id("twotabsearchtextbox"), text)
            .and_.clicking(By.id("nav-search-submit-button")))
```

**Parameter Validation**:
- Type hints (enforced by IDE/linters, not runtime)
- No explicit validation in step methods

**Response Formatting**:
- UI actions: Return self (implicit success)
- REST actions: Response validated via matchers in assertion step

---

### 10.5 Domain Model Implementation

**Entity Pattern** (Immutable):
```python
@dataclass(eq=True, frozen=True)
@to_string()
class SwaggerPetstorePet:
    name: str
    status: str
```

**Value Object Pattern**:
```python
@dataclass
class Credentials:
    username: str
    password: str
```

**Domain Event Pattern**:
- Not implemented (no event-driven architecture)

**Business Rule Enforcement**:
- Enforced in tests via assertions
- Models are passive data structures

---

## 11. Testing Architecture

### Testing Strategy

**Test Types**:
1. **UI Functional Tests** - Selenium/Playwright testing web applications
2. **API Functional Tests** - REST endpoint validation
3. **No Unit Tests** - Framework focused on integration/functional testing

### Test Boundaries

**Integration Test Boundary**:
- Tests interact with real applications (Amazon, TerminalX, Swagger Petstore)
- No mocking of external services
- Tests validate end-to-end flows

**Unit Test Boundary**:
- Not applicable - no isolated unit tests
- Could unit test Steps methods independently (not currently done)

### Test Doubles and Mocking

**No Test Doubles Used**:
- Tests interact with real UIs and APIs
- No mocks, stubs, or fakes
- Could use mocking for offline development (not currently implemented)

### Test Data Strategy

**Hardcoded Test Data**:
- Credentials in INI files
- Search terms and expected values in test code

**Generated Test Data**:
```python
random_pet = SwaggerPetstorePet.random()  # UUID-based name
```

**Test Data Management**:
- No test data cleanup
- Assumes idempotent test execution or fresh environment

### Testing Tools Integration

**pytest Integration**:
- Test discovery via `pyproject.toml` configuration
- Custom base classes integrate with pytest fixtures and lifecycle

**Reporting Integration**:
- `pytest-html`: HTML report generation
- `allure-pytest`: Allure framework integration
- Both configured via pytest `addopts`

**Framework Integration**:
- Selenium: WebDriver instantiation in `setup_method()`
- Playwright: Managed by qa-pytest-playwright base classes
- requests: Session created in base RestTests class

---

## 12. Deployment Architecture

### Deployment Topology

**Local Development**:
- Tests run on developer machine
- WebDriver connects to local browser instances
- APIs accessed over internet

**CI/CD Environments**:
- Containerized test execution (likely)
- Headless browser mode for UI tests
- Allure report generation and publishing

### Environment-Specific Adaptations

**Configuration-Driven**:
- INI files contain environment-specific URLs
- Command-line options override configuration:
  ```bash
  pytest --config selenium:browser_type=firefox tests/amazon_tests.py
  ```

**Browser Selection**:
```python
if self._configuration.parser.has_option("selenium", "browser_type") \
        and self._configuration.parser["selenium"]["browser_type"] == "firefox":
    self._web_driver = Firefox(options=options, service=service)
else:
    super().setup_method()  # Default Chrome
```

### Runtime Dependency Resolution

**PDM-Based**:
```bash
pdm install  # Resolves and installs dependencies
```

**Playwright Browser Installation**:
```bash
pdm run playwright-install  # Downloads browser binaries
```

### Configuration Management

**Configuration Hierarchy**:
1. INI file defaults
2. Command-line overrides (`--config`)
3. Code-level overrides (in `setup_method()`)

### Containerization

**Not Explicitly Defined** - But likely uses:
- Docker containers for consistent test environment
- Selenium Grid or Playwright Grid for parallel execution

### Cloud Service Integration

**None in Current Implementation** - But extensible to:
- BrowserStack / Sauce Labs for cloud browsers
- CI/CD platforms (GitHub Actions, GitLab CI, Jenkins)
- Allure TestOps or similar for report hosting

---

## 13. Extension and Evolution Patterns

### Feature Addition Patterns

**Adding a New Test Scenario** (to existing AUT):
1. Open existing `tests/*_tests.py`
2. Add new `should_*` method
3. Compose step chain using existing steps
4. Add new step methods to `*_steps.py` if needed
5. Add new model objects to `model/examples/` if needed

**Example**:
```python
# tests/amazon_tests.py
def should_search_and_filter(self):
    (self.steps
     .given.amazon(self.ui_context)
     .when.searching_for("laptop")
     .and_.applying_price_filter("$500-$1000")  # New step
     .then.results_contain("laptop"))  # New assertion step
```

### Adding a New Application Under Test

**Complete Checklist**:
1. Create configuration: `src/qa_automation_python_demo/new_app_configuration.py`
   ```python
   class NewAppConfiguration(SeleniumConfiguration):  # or RestConfiguration
       pass
   ```

2. Create INI file: `src/qa_automation_python_demo/configurations/new_app_configuration.ini`
   ```ini
   [ui]
   entry_point = https://newapp.com
   ```

3. Create steps: `src/qa_automation_python_demo/new_app_steps.py`
   ```python
   class NewAppSteps[TConfiguration: NewAppConfiguration](SeleniumSteps[TConfiguration]):
       @Context.traced
       def new_app(self, driver: UiContext[UiElement]) -> Self:
           return self.ui_context(driver).at(self.configured.entry_point)
       
       @Context.traced
       def some_action(self) -> Self:
           return self.clicking(By.id("button-id"))
   ```

4. Create tests: `tests/new_app_tests.py`
   ```python
   class NewAppTests(SeleniumTests[NewAppSteps[NewAppConfiguration], NewAppConfiguration]):
       _steps_type = NewAppSteps
       _configuration = NewAppConfiguration()
       
       def should_do_something(self):
           (self.steps
            .given.new_app(self.ui_context)
            .when.some_action()
            .then.verify_result())
   ```

5. Add models if needed: `src/qa_automation_python_demo/model/examples/new_app_*.py`

### Modification Patterns

**Extending Existing Steps**:
- Add new methods to Steps class
- Maintain `@Context.traced` decorator
- Follow `snake_case` naming
- Return `Self` for chaining

**Modifying Step Behavior**:
- Update step method implementation
- Ensure backward compatibility if step is used by multiple tests
- Add optional parameters with defaults rather than changing signature

**Deprecation Pattern** (Not Formally Defined):
- Could mark methods with deprecation warnings
- Provide migration path in docstring
- Remove after migration period

### Integration Patterns

**Adding External System Integration**:
1. Choose appropriate base class (SeleniumTests, PlaywrightTests, RestTests)
2. Create Configuration + Steps + Tests as described above
3. For new integration types, create custom base classes (e.g., `GrpcSteps`)

**Adapter Implementation**:
```python
# If integrating new protocol (e.g., gRPC)
class GrpcSteps[TConfiguration]:
    def __init__(self, configuration: TConfiguration):
        self._configuration = configuration
        self._client = None  # gRPC client
    
    @property
    def given(self) -> Self:
        return self
    
    # ... implement when, then, and_ similarly
```

**Anti-Corruption Layer**:
- Steps act as anti-corruption layer
- Isolate framework-specific code in Steps
- Tests remain framework-agnostic (mostly)

---

## 14. Architectural Pattern Examples

### Layer Separation Example

**Interface Definition and Implementation**:
```python
# Base interface (from qa-pytest-webdriver)
class SeleniumSteps[TConfiguration]:
    def typing(self, locator: By, text: str) -> Self:
        """Framework-provided helper method."""
        ...

# Implementation
class AmazonSteps[TConfiguration: AmazonConfiguration](SeleniumSteps[TConfiguration]):
    @Context.traced
    def searching_for(self, text: str) -> Self:
        # Uses base class helper, returns Self for chaining
        return (self.typing(By.id("twotabsearchtextbox"), text)
                .and_.clicking(By.id("nav-search-submit-button")))
```

**Cross-Layer Communication**:
```python
# Test layer calls Steps layer
class AmazonTests(SeleniumTests[AmazonSteps[AmazonConfiguration], AmazonConfiguration]):
    def should_checkout(self):
        # Test composes step chain, doesn't implement actions
        (self.steps
         .given.amazon(self.ui_context)  # Steps accesses Configuration
         .when.searching_for("mobile phone")
         .then.signin_required())
```

**Dependency Injection**:
```python
# Test declares dependencies
class AmazonTests(SeleniumTests[...]):
    _steps_type = AmazonSteps  # DI: Steps class
    _configuration = AmazonConfiguration()  # DI: Configuration instance

# Base class handles injection (simplified)
@property
def steps(self) -> TSteps:
    if not self._steps_instance:
        self._steps_instance = self._steps_type(self._configuration)
    return self._steps_instance
```

---

### Component Communication Example

**Service Invocation Pattern**:
```python
# REST API invocation
@Context.traced
def adding(self, pet: SwaggerPetstorePet) -> Self:
    return self.invoking(Request(
        method=HttpMethod.POST,
        url=self.configured.resource_uri(path="pet"),
        json=asdict(pet)  # Model → dict → JSON
    ))
```

**Event Publication and Handling** (Not Used):
- No event-driven patterns in current architecture
- Could be added for complex async workflows

**Message Passing Implementation** (Not Used):
- No message queues or pub/sub
- Synchronous method calls only

---

### Extension Point Example

**Configuration-Driven Extension**:
```python
# Override default browser via configuration
@override
def setup_method(self) -> None:
    if self._configuration.parser.has_option("selenium", "browser_type") \
            and self._configuration.parser["selenium"]["browser_type"] == "firefox":
        # Extension point: custom browser setup
        options = FirefoxOptions()
        service = FirefoxService(GeckoDriverManager().install())
        self._web_driver = Firefox(options=options, service=service)
    else:
        # Default behavior
        super().setup_method()
```

**Plugin Registration** (Not Implemented):
- No formal plugin system
- Could implement via Python entry points or dynamic imports

---

## 15. Architectural Decision Records

### ADR-001: Layered Architecture with BDD-Style Steps

**Context**:
- Test automation requires clear separation between test scenarios, actions, and configuration
- Tests should be readable by non-technical stakeholders
- Framework code should be reusable across multiple Applications Under Test

**Decision**:
Implement layered architecture with:
- Tests layer (scenario definitions)
- Steps layer (action encapsulation)
- Configuration layer (environment settings)
- Model layer (domain objects)

**Alternatives Considered**:
- Page Object Model (POM) - Rejected as too UI-focused, doesn't fit API testing
- Keyword-Driven Testing - Rejected as less type-safe and harder to navigate
- Flat test structure - Rejected due to code duplication and poor maintainability

**Consequences**:
- ✅ Clear separation of concerns
- ✅ High reusability of step methods
- ✅ Type-safe method chaining
- ❌ Steeper learning curve for new developers
- ❌ More boilerplate (3 files per AUT minimum)

---

### ADR-002: BDD-Style Fluent Interface

**Context**:
- Test readability is critical for documentation and collaboration
- Traditional assertion syntax (assert, assertEqual) is verbose
- Hamcrest matchers provide expressive assertions

**Decision**:
Adopt BDD-style Given/When/Then/And method chaining:
```python
(self.steps
 .given.amazon(self.ui_context)
 .when.searching_for("text")
 .then.signin_required())
```

**Alternatives Considered**:
- Traditional pytest assertions - Less fluent, harder to chain
- Gherkin/Cucumber - Rejected as too heavyweight, requires separate feature files

**Consequences**:
- ✅ Highly readable test scenarios
- ✅ Self-documenting test flows
- ✅ Easy to compose complex scenarios
- ❌ Requires `Self` return type on all step methods
- ❌ Less familiar to developers from non-BDD backgrounds

---

### ADR-003: Generic Type Parameters for Type Safety

**Context**:
- Python's dynamic typing can lead to runtime errors
- IDE autocomplete and type checking improve developer experience
- Framework needs to support multiple AUT-specific implementations

**Decision**:
Use generic type parameters throughout:
```python
class AmazonSteps[TConfiguration: AmazonConfiguration](SeleniumSteps[TConfiguration]):
    ...
```

**Alternatives Considered**:
- No generics - Rejected due to loss of type safety
- Duck typing - Rejected due to poor IDE support
- Protocol types - Considered but generics more explicit

**Consequences**:
- ✅ Strong type checking at development time
- ✅ Excellent IDE autocomplete support
- ✅ Catches configuration mismatches early
- ❌ More complex type signatures
- ❌ Requires Python 3.12+ for full generic syntax

---

### ADR-004: Configuration via INI Files

**Context**:
- Tests need to run against different environments (dev/staging/prod)
- Configuration should be external to code
- Non-developers should be able to update settings

**Decision**:
Use INI files for configuration, loaded via ConfigParser:
```ini
[ui]
entry_point = https://terminalx.com

[users]
checker = user@example.com:password
```

**Alternatives Considered**:
- JSON/YAML - Rejected as less human-friendly for simple key-value pairs
- Environment variables - Rejected as harder to organize hierarchically
- Python config files - Rejected due to security concerns (arbitrary code execution)

**Consequences**:
- ✅ Simple, readable configuration format
- ✅ No code deployment for config changes
- ✅ Built-in Python support (ConfigParser)
- ❌ Less structured than JSON/YAML
- ❌ Credentials in plain text (security concern)

---

### ADR-005: Framework Base Classes from External Libraries

**Context**:
- Common test automation patterns should be reusable
- Selenium/Playwright setup is repetitive boilerplate
- Maintenance burden of custom framework code

**Decision**:
Use external qa-pytest-* libraries for base classes:
- qa-pytest-webdriver (SeleniumTests, SeleniumSteps)
- qa-pytest-playwright (PlaywrightTests, PlaywrightSteps)
- qa-pytest-rest (RestTests, RestSteps)
- qa-pytest-commons (UiContext, By)

**Alternatives Considered**:
- Custom framework from scratch - Rejected due to maintenance burden
- Popular frameworks (Robot Framework, etc.) - Rejected as too opinionated

**Consequences**:
- ✅ Reduced boilerplate in project code
- ✅ Framework updates via dependency version bumps
- ✅ Shared patterns across projects
- ❌ External dependency on qa-pytest libraries
- ❌ Limited control over base class behavior

---

### ADR-006: Dataclasses for Domain Models

**Context**:
- Need lightweight data structures for credentials, users, API payloads
- Serialization/deserialization required for API testing
- Immutability desirable for test data

**Decision**:
Use Python dataclasses with decorators:
```python
@dataclass(eq=True, frozen=True)
@to_string()
class SwaggerPetstorePet:
    name: str
    status: str
```

**Alternatives Considered**:
- Plain classes - Rejected due to boilerplate (__init__, __repr__, etc.)
- Named tuples - Rejected as less flexible
- Pydantic models - Rejected as overkill for simple use cases

**Consequences**:
- ✅ Minimal boilerplate code
- ✅ Built-in equality and hashing (frozen=True)
- ✅ Easy serialization via asdict()
- ✅ Type hints for validation
- ❌ Limited validation capabilities
- ❌ Immutable models less flexible for mutation scenarios

---

## 16. Architecture Governance

### Maintaining Architectural Consistency

**Code Review Practices** (Inferred):
- New AUT implementations follow existing patterns
- Naming conventions consistently applied
- Layer boundaries respected in imports

**Architectural Patterns Enforcement**:
1. **File Naming**: `*_configuration.py`, `*_steps.py`, `*_tests.py`
2. **Class Naming**: `*Configuration`, `*Steps`, `*Tests`
3. **Method Naming**: `should_*` for tests, `snake_case` for steps
4. **Decorators**: `@Context.traced` on all step methods

### Automated Checks

**Linting and Formatting**:
```toml
# pyproject.toml
[tool.autopep8]
max_line_length = 80

[tool.isort]
profile = "black"
line_length = 80
```

**Type Checking** (Not Configured):
- Could add mypy or pyright
- IDE provides type checking via language server

**Architecture Tests** (Not Implemented):
- Could use pytest to validate layer dependencies
- Could check for forbidden imports

### Architectural Review Process

**Evidence in Codebase**:
- Consistent patterns across multiple AUTs (Amazon, TerminalX, Swagger Petstore)
- Suggests architectural review or strong conventions
- No documented review process found

### Documentation Practices

**Current Documentation**:
- README.md - Project overview and setup
- SKILL.md - Brownfield developer reference
- references/*.md - Architecture, tech stack, conventions

**Code Documentation**:
- SPDX license headers
- Docstrings on classes and key methods
- Type hints as inline documentation

---

## 17. Blueprint for New Development

### Development Workflow

#### For Adding a New UI Test Scenario (Selenium)

1. **Identify Application Under Test (AUT)**
   - Is there existing `*_configuration.py` and `*_steps.py`? Use them.
   - If new AUT, follow "Adding a New AUT" workflow below.

2. **Add Test Method**
   ```python
   # tests/terminalx_tests.py
   def should_perform_new_scenario(self):
       (self.steps
        .given.terminalx(self.ui_context)
        .when.new_action()
        .then.new_assertion())
   ```

3. **Add Step Methods** (if needed)
   ```python
   # src/qa_automation_python_demo/terminalx_steps.py
   @Context.traced
   def new_action(self) -> Self:
       return self.clicking(By.id("element-id"))
   
   @Context.traced
   def new_assertion(self) -> Self:
       return self.the_element(
           By.id("result"),
           adapted_object(lambda e: e.text, is_("expected")))
   ```

4. **Run Test**
   ```bash
   pdm run test-all
   # Or specific test:
   pytest tests/terminalx_tests.py::TerminalXTests::should_perform_new_scenario
   ```

5. **Review Results**
   - Check console output
   - Review `report.html`
   - Generate Allure report: `pdm run allure-generate`

---

#### For Adding a New REST API Test

1. **Add Model Objects** (if needed)
   ```python
   # src/qa_automation_python_demo/model/examples/my_api_object.py
   @dataclass(eq=True, frozen=True)
   @to_string()
   class MyApiObject:
       field1: str
       field2: int
       
       @staticmethod
       def random() -> MyApiObject:
           return MyApiObject(field1=str(uuid4()), field2=42)
   ```

2. **Add Step Methods**
   ```python
   # src/qa_automation_python_demo/my_api_steps.py
   @Context.traced
   def creating_object(self, obj: MyApiObject) -> Self:
       return self.invoking(Request(
           method=HttpMethod.POST,
           url=self.configured.resource_uri(path="objects"),
           json=asdict(obj)))
   
   @Context.traced
   def the_objects(self, matcher: Matcher[...]) -> Self:
       return self.the_invocation(
           Request(method=HttpMethod.GET, url=self.configured.resource_uri(path="objects")),
           adapted_object(lambda r: MyApiObject.from_(r), matcher))
   ```

3. **Add Test**
   ```python
   # tests/my_api_tests.py
   def should_create_object(self):
       obj = MyApiObject.random()
       (self.steps
        .given.my_api(self._rest_session)
        .when.creating_object(obj)
        .then.the_objects(yields_item(is_(obj))))
   ```

---

#### For Adding a New Application Under Test

1. **Create Configuration Class**
   ```python
   # src/qa_automation_python_demo/newapp_configuration.py
   from qa_pytest_webdriver.selenium_configuration import SeleniumConfiguration
   # OR: from qa_pytest_rest import RestConfiguration
   
   class NewAppConfiguration(SeleniumConfiguration):
       pass
   ```

2. **Create Configuration INI**
   ```ini
   ; src/qa_automation_python_demo/configurations/newapp_configuration.ini
   [ui]
   entry_point = https://newapp.com
   
   [users]
   test_user = user@example.com:password123
   ```

3. **Create Steps Class**
   ```python
   # src/qa_automation_python_demo/newapp_steps.py
   from typing import Self
   from qa_pytest_webdriver.selenium_steps import SeleniumSteps
   from qa_pytest_commons import By, UiContext, UiElement
   from qa_testing_utils.logger import Context
   from qa_automation_python_demo.newapp_configuration import NewAppConfiguration
   
   class NewAppSteps[TConfiguration: NewAppConfiguration](SeleniumSteps[TConfiguration]):
       @Context.traced
       def newapp(self, driver: UiContext[UiElement]) -> Self:
           return self.ui_context(driver).at(self.configured.entry_point)
       
       @Context.traced
       def login(self, username: str, password: str) -> Self:
           return (self.typing(By.id("username"), username)
                   .and_.typing(By.id("password"), password)
                   .and_.clicking(By.id("login-button")))
   ```

4. **Create Test Class**
   ```python
   # tests/newapp_tests.py
   from qa_pytest_webdriver.selenium_tests import SeleniumTests
   from qa_automation_python_demo.newapp_configuration import NewAppConfiguration
   from qa_automation_python_demo.newapp_steps import NewAppSteps
   
   class NewAppTests(SeleniumTests[NewAppSteps[NewAppConfiguration], NewAppConfiguration]):
       _steps_type = NewAppSteps
       _configuration = NewAppConfiguration()
       
       def should_login(self):
           (self.steps
            .given.newapp(self.ui_context)
            .when.login("user@example.com", "password123")
            .then.dashboard_visible())
   ```

5. **Add Models if Needed**
   - Follow dataclass pattern
   - Place in `src/qa_automation_python_demo/model/examples/`

6. **Run and Iterate**
   ```bash
   pdm run test-all
   ```

---

### Implementation Templates

#### Step Method Template (UI)
```python
@Context.traced
def action_name(self, param: str) -> Self:
    """
    Brief description of what this step does.
    
    Args:
        param: Description of parameter.
    
    Returns:
        Self: For method chaining.
    """
    return self.clicking(By.id("element-id"))
```

#### Step Method Template (REST)
```python
@Context.traced
def creating_resource(self, data: ModelClass) -> Self:
    """Create a new resource via POST."""
    return self.invoking(Request(
        method=HttpMethod.POST,
        url=self.configured.resource_uri(path="resource"),
        json=asdict(data)
    ))
```

#### Assertion Step Template
```python
@Context.traced
def element_has_text(self, expected: str) -> Self:
    """Assert element contains expected text."""
    return self.the_element(
        By.id("element-id"),
        adapted_object(
            lambda element: element.text,
            contains_string_ignoring_case(expected)
        )
    )
```

#### Model Class Template
```python
from dataclasses import dataclass
from qa_testing_utils.string_utils import to_string

@dataclass(eq=True, frozen=True)
@to_string()
class MyModel:
    field1: str
    field2: int
    
    @staticmethod
    def random() -> 'MyModel':
        """Create instance with random data."""
        return MyModel(field1=str(uuid4()), field2=42)
```

---

### Common Pitfalls

#### Architecture Violations to Avoid

1. **❌ Implementing Actions in Tests**
   ```python
   # WRONG
   def should_login(self):
       driver.find_element(By.ID, "username").send_keys("user")
   
   # CORRECT
   def should_login(self):
       self.steps.given.app(self.ui_context).when.login("user", "pass")
   ```

2. **❌ Steps Importing Tests**
   ```python
   # WRONG - circular dependency
   from tests.amazon_tests import AmazonTests
   ```

3. **❌ Hardcoding Configuration in Code**
   ```python
   # WRONG
   url = "https://terminalx.com"
   
   # CORRECT
   url = self.configured.entry_point
   ```

4. **❌ Forgetting to Return Self**
   ```python
   # WRONG - breaks chaining
   def action(self) -> Self:
       self.clicking(By.ID, "btn")
       # Missing return!
   
   # CORRECT
   def action(self) -> Self:
       return self.clicking(By.ID, "btn")
   ```

---

#### Common Mistakes

1. **Incorrect Generic Type Parameters**
   ```python
   # WRONG - type parameter mismatch
   class MySteps[T](SeleniumSteps[MyConfiguration]):
       pass
   
   # CORRECT
   class MySteps[TConfiguration: MyConfiguration](SeleniumSteps[TConfiguration]):
       pass
   ```

2. **Missing @Context.traced Decorator**
   ```python
   # WRONG - no tracing
   def action(self) -> Self:
       return self.clicking(...)
   
   # CORRECT
   @Context.traced
   def action(self) -> Self:
       return self.clicking(...)
   ```

3. **Incorrect pytest Discovery Pattern**
   ```python
   # WRONG - pytest won't find this
   def test_login(self):
       pass
   
   # CORRECT (per pyproject.toml)
   def should_login(self):
       pass
   ```

---

#### Performance Considerations

1. **Avoid Unnecessary Waits**
   - Use implicit waits (configured in base classes)
   - Don't add `time.sleep()` - use explicit waits if needed

2. **Reuse Sessions/Drivers**
   - Already handled by framework in `setup_method()`
   - Don't create new drivers in step methods

3. **Parallelize Tests**
   ```bash
   pytest -n auto  # Requires pytest-xdist
   ```

---

#### Testing Blind Spots

1. **No Negative Tests** - Framework supports positive flow testing well; add explicit negative scenario tests

2. **Error Recovery Not Tested** - Tests fail fast; consider adding error recovery scenarios

3. **Cross-Browser Coverage** - Default Chrome; add Firefox/Safari configurations

4. **API Error Responses** - Add tests for 4xx/5xx responses

5. **Accessibility** - No accessibility testing; could add axe-core integration

---

### Keeping This Blueprint Updated

**When to Update**:
- New architectural patterns introduced
- New base classes or frameworks adopted
- Major refactoring of layer structure
- New cross-cutting concerns added

**How to Update**:
1. Review changes in architecture references (.github/skills/*/references/)
2. Update relevant sections in this blueprint
3. Add new examples if new patterns introduced
4. Update decision records for significant changes

**Recommended Frequency**:
- After major feature additions
- Quarterly architecture reviews
- Before onboarding new team members

---

## Appendix: Key Files Reference

| File | Purpose | Layer |
|------|---------|-------|
| [pyproject.toml](pyproject.toml) | Project metadata, dependencies, pytest config | Infrastructure |
| [logging.ini](logging.ini) | Logging configuration | Cross-Cutting |
| [tests/amazon_tests.py](tests/amazon_tests.py) | Amazon UI test scenarios | Tests |
| [src/qa_automation_python_demo/amazon_steps.py](src/qa_automation_python_demo/amazon_steps.py) | Amazon UI action steps | Steps |
| [src/qa_automation_python_demo/amazon_configuration.py](src/qa_automation_python_demo/amazon_configuration.py) | Amazon configuration class | Configuration |
| [src/qa_automation_python_demo/configurations/amazon_configuration.ini](src/qa_automation_python_demo/configurations/amazon_configuration.ini) | Amazon configuration values | Configuration |
| [tests/swagger_petstore_tests.py](tests/swagger_petstore_tests.py) | REST API test scenarios | Tests |
| [src/qa_automation_python_demo/swagger_petstore_steps.py](src/qa_automation_python_demo/swagger_petstore_steps.py) | REST API action steps | Steps |
| [src/qa_automation_python_demo/model/examples/swagger_petstore_pet.py](src/qa_automation_python_demo/model/examples/swagger_petstore_pet.py) | Pet domain model | Model |
| [src/qa_automation_python_demo/model/credentials.py](src/qa_automation_python_demo/model/credentials.py) | Generic credentials model | Model |

---

**Blueprint Version**: 1.0  
**Last Updated**: February 23, 2026  
**Maintainer**: Architecture review process (see Section 16)
