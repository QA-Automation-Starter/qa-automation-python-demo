---
name: brownfield-developer-qa-automation-python-demo
description: >-
  Senior developer expertise for qa-automation-python-demo. Provides deep understanding of 
  tech stack, architecture, coding conventions, and development patterns. 
  Use when working on qa-automation-python-demo to ensure code consistency and quality.
---

# qa-automation-python-demo Developer Skills

## Skill Overview

This skill empowers GitHub Copilot in VS Code as a **senior development engineer** for **qa-automation-python-demo**.

## Key Skills

### 1. Tech Stack Mastery
- **Primary Language**: Python $\ge 3.13$
- **Core Frameworks**: pytest, Selenium WebDriver, Playwright, requests, Hamcrest
- **Details**: See [references/tech-stack.md](references/tech-stack.md)

### 2. Architecture Understanding
- **Style**: Layered, test-driven (Tests → Steps → Configurations/Models)
- **Layering**: BDD-style step chains with framework-provided base classes
- **Details**: See [references/architecture.md](references/architecture.md)

### 3. Coding Conventions
- **Naming**: snake_case files/functions, PascalCase classes, *Tests test classes
- **Style**: autopep8 and isort with line length 80
- **Details**: See [references/coding-conventions.md](references/coding-conventions.md)

### 4. Module Structure
- **Type**: Monolith (single Python package)
- **Count**: 2 primary modules (src package + tests)
- **Details**: See [references/module-structure.md](references/module-structure.md)

### 5. Development Patterns
- **Patterns**: BDD Given/When/Then step chaining, configuration-driven tests
- **Practices**: Dataclass models, Hamcrest matchers, tracing decorators
- **Details**: See [references/development-patterns.md](references/development-patterns.md)

## Brownfield Principles

1. **Respect existing architecture** - Follow, don't "improve"
2. **Code reuse first** - Search before creating
3. **Forward compatibility** - Don't break existing
4. **Refactor on-demand** - Only when necessary
5. **Style consistency** - Match existing code

## Reference Files

| File | Description |
|------|-------------|
| [architecture.md](references/architecture.md) | Architecture and layering |
| [tech-stack.md](references/tech-stack.md) | Tech stack and constraints |
| [coding-conventions.md](references/coding-conventions.md) | Coding standards |
| [module-structure.md](references/module-structure.md) | Module responsibilities |
| [development-patterns.md](references/development-patterns.md) | Development patterns |
