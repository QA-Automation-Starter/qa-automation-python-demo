# Brownfield Skills

> **VS Code + GitHub Copilot Skills** for brownfield (existing) project development.

## Overview

This directory contains skills that enable AI coding agents to work effectively with existing (brownfield) projects. These skills are independent of the spec-kit extension and can be used standalone.

## Available Skills

| Skill | Description |
|-------|-------------|
| `brownfield-skills` | Generate senior developer expertise for any existing project |
| `brownfield-ears` | Convert natural language requirements to EARS format |

## Installation

### For VS Code + GitHub Copilot

Keep the skills in your repository under `.github/skills/` (no extra install needed). Add a Copilot instructions file that points Copilot to these references:

```bash
mkdir -p .github/skills
cp -r brownfield-skills .github/skills/
cp -r brownfield-ears .github/skills/
```

### Verification

```bash
ls .github/skills/*/SKILL.md
```

Should show:
- `.github/skills/brownfield-skills/SKILL.md`
- `.github/skills/brownfield-ears/SKILL.md`

## Skill Details

### brownfield-skills

Analyzes an existing project and generates structured Skills that enable AI to:

1. **Master the project** - Deep understanding of tech stack, architecture, and code style
2. **Follow conventions** - Work according to existing coding patterns
3. **Ensure compatibility** - Maintain backward compatibility when extending
4. **Reuse code first** - Prioritize existing implementations over new code

**Generated Output Structure:**
```
.github/skills/brownfield-developer-[project-name]/
├── SKILL.md                    # Entry point with project overview
└── references/
    ├── architecture.md         # Architecture and layering
    ├── tech-stack.md           # Tech stack and versions
    ├── coding-conventions.md   # Coding standards
    ├── module-structure.md     # Module responsibilities
    └── development-patterns.md # Development patterns
```

### brownfield-ears

Converts natural language requirements into [EARS (Easy Approach to Requirements Syntax)](https://alistairmavin.com/ears/) format for better requirement clarity.

**EARS Patterns:**
- Ubiquitous: `The system shall <function>`
- Event-Driven: `When <trigger>, the system shall <response>`
- State-Driven: `If <state>, then the system shall <behavior>`
- Optional: `Where <condition>, the user can <operation>`
- Complex: `When <trigger>, and <state>, the system shall <response>`

## Integration with Extension

These skills complement the `brownfield-bootstrap` extension:

1. Use `/speckit.brownfield-bootstrap.init` to bootstrap SDD workflow
2. Use `brownfield-skills` to generate developer expertise
3. Use `brownfield-ears` to improve requirement clarity

## Language Support

Both skills support English and Chinese:
- `templates.md` - English templates
- `templates-cn.md` - Chinese templates (中文模板)

## Related

- **Extension**: See `extension/` directory for spec-kit commands
- **Main README**: See the repository root for complete documentation

## License

MIT License
