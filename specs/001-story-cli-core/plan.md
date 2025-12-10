# Implementation Plan: Story CLI - Core Foundation & Character Creation

**Branch**: `001-story-cli-core` | **Date**: 2025-12-10 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-story-cli-core/spec.md`

## Summary

Build the foundational Python CLI package for Story CLI, a terminal-based creative writing assistant for visual novel authors. This version establishes:
1. **CLI Framework**: Python package with `story` command entry point using Typer
2. **Project Management**: `story init` and `story open` commands for project lifecycle
3. **Character Creation Wizard**: 5-phase guided wizard (basics, appearance, personality, backstory, relationships) with LLM assistance
4. **LLM Integration**: Ollama integration with Qwen3-32B using LangGraph for agentic tool-calling patterns
5. **Interactive Chat**: `story chat` command for freeform LLM interaction

## Technical Context

**Language/Version**: Python 3.11+ with full type hints (per constitution)
**Primary Dependencies**: Typer (CLI), Rich (terminal UI), LangGraph (workflows), langchain-ollama (LLM), Pydantic (data models)
**Storage**: JSON files in project directory (`story_data/`)
**Testing**: pytest with contract, integration, and unit test structure
**Target Platform**: Linux, macOS, Windows terminals (cross-platform)
**Project Type**: Single Python package (CLI application)
**Performance Goals**: 10-second LLM connection timeout, streaming responses for real-time feedback
**Constraints**: Offline-capable (local LLM only), <100MB memory for CLI, no cloud dependencies
**Scale/Scope**: Single-user, up to 50 characters per project

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Guiding Principles Alignment

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Writer-First Design | ✅ PASS | All AI suggestions require user approval; wizard allows editing/regeneration |
| II. Structured Creativity | ✅ PASS | 5-phase wizard with validation gates; non-linear navigation supported |
| III. Local-First, Privacy-Respecting | ✅ PASS | JSON storage in project dir; Ollama LLM; no cloud/telemetry |
| IV. Iterative Refinement | ✅ PASS | Regenerate option in wizard; edit existing characters |
| V. Interoperability | ✅ PASS | Clean JSON output; LoRA trigger generation for image tools |

### Technical Constraints Alignment

| Constraint | Status | Evidence |
|------------|--------|----------|
| Python 3.11+ with type hints | ✅ PASS | Specified in assumptions |
| Typer for CLI | ✅ PASS | Will use for all commands |
| Rich for terminal UI | ✅ PASS | Will use for panels, tables, progress |
| LangGraph for workflows | ✅ PASS | Character wizard state machine |
| langchain-ollama for LLM | ✅ PASS | Ollama integration specified |
| Pydantic for data models | ✅ PASS | Character, Project entities |
| JSON for storage | ✅ PASS | All data persisted as JSON |
| Ollama backend support | ✅ PASS | Primary LLM integration |
| Cross-platform terminals | ✅ PASS | Target platform specified |
| No internet for core | ✅ PASS | Local-only operation |
| No data outside project | ✅ PASS | All in `story_data/` |
| No irreversible changes without confirm | ✅ PASS | Delete warns about dependencies |
| No Ren'Py code generation | ✅ PASS | Explicitly out of scope |

### MUST NOT Violations

None identified. All constraints satisfied.

## Project Structure

### Documentation (this feature)

```text
specs/001-story-cli-core/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (internal APIs)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
story_cli/
├── __init__.py          # Package init with version
├── __main__.py          # Entry point for `python -m story_cli`
├── cli/
│   ├── __init__.py
│   ├── main.py          # Typer app, command registration
│   ├── init_cmd.py      # story init command
│   ├── open_cmd.py      # story open command
│   ├── character_cmd.py # story new/edit/list/delete character
│   └── chat_cmd.py      # story chat command
├── models/
│   ├── __init__.py
│   ├── project.py       # Project Pydantic model
│   ├── character.py     # Character Pydantic model
│   └── relationship.py  # Relationship Pydantic model
├── services/
│   ├── __init__.py
│   ├── project_service.py    # Project CRUD operations
│   ├── character_service.py  # Character CRUD, index management
│   └── llm_service.py        # Ollama client, streaming
├── workflows/
│   ├── __init__.py
│   └── character_wizard.py   # LangGraph state machine
├── prompts/
│   ├── __init__.py
│   └── character_prompts.py  # LLM prompt templates
└── utils/
    ├── __init__.py
    ├── config.py         # Environment variable handling
    ├── validation.py     # Input validation helpers
    └── display.py        # Rich formatting helpers

tests/
├── conftest.py           # Shared fixtures
├── contract/
│   └── test_models.py    # Pydantic model validation
├── integration/
│   ├── test_cli.py       # CLI command tests
│   └── test_llm.py       # LLM integration tests (requires Ollama)
└── unit/
    ├── test_services.py  # Service unit tests
    └── test_workflows.py # Workflow state tests

pyproject.toml            # Package configuration, dependencies
README.md                 # Project documentation
```

**Structure Decision**: Single Python package structure selected. CLI application with clear separation between:
- `cli/` - Command handlers (Typer)
- `models/` - Data models (Pydantic)
- `services/` - Business logic
- `workflows/` - LangGraph state machines
- `prompts/` - LLM prompt templates
- `utils/` - Shared utilities

## Complexity Tracking

No violations requiring justification. Implementation follows constitution constraints.
