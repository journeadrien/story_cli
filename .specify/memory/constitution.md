<!--
Sync Impact Report
==================
Version change: 0.0.0 → 1.0.0 (MAJOR - initial ratification)
Added sections: Project Identity, Guiding Principles, Technical Constraints, Scope Boundaries, Governance
Removed sections: All template placeholders
Templates requiring updates:
  - .specify/templates/plan-template.md: ✅ no changes needed (Constitution Check section is generic)
  - .specify/templates/spec-template.md: ✅ no changes needed
  - .specify/templates/tasks-template.md: ✅ no changes needed
Follow-up TODOs: None
-->

# Story CLI Constitution

## Project Identity

**Story CLI** — AI-Powered Visual Novel Story Builder

A terminal-based creative writing assistant that helps authors develop visual novel stories through structured wizards and iterative planning workflows, powered by local LLMs.

**Core Purpose**: Enable writers to create rich, consistent visual novel narratives by guiding character creation, facilitating scene planning with AI assistance, maintaining story coherence through a searchable JSON database, and generating AI image prompts.

## Guiding Principles

### I. Writer-First Design

The tool serves the writer's creative vision. AI suggests, human decides—every generated content requires explicit approval. Minimize friction between idea and documented story element.

### II. Structured Creativity

Use phase-based wizards to ensure completeness without overwhelming. Allow non-linear navigation (go back, skip, edit later). Enforce minimum viable data before proceeding via validation gates.

### III. Local-First, Privacy-Respecting

All data stored locally in JSON files. LLM runs locally via Ollama with no cloud dependencies. No telemetry, no external API calls for core functionality.

### IV. Iterative Refinement

Never finalize on first draft—always offer "regenerate" or "refine" options. Track version history for major story elements. Support "what-if" branches for exploration.

### V. Interoperability

Output clean JSON consumable by other tools. Generate prompts compatible with multiple image generation systems. Structure data for eventual Ren'Py export (handled by renpy-cli).

## Technical Constraints

### MUST Use

- **Python 3.11+** with full type hints
- **Typer** for CLI framework
- **Rich** for terminal UI (panels, tables, progress)
- **LangGraph** for workflow state machines
- **langchain-ollama** for LLM integration
- **Pydantic** for data models and validation
- **JSON** for all persistent storage

### MUST Support

- **Ollama** as LLM backend (Qwen3-32B primary, smaller models as fallback)
- Linux, macOS, Windows terminals
- Unicode/emoji in terminal output

### MUST NOT

- Require internet connection for core functionality
- Store data outside project directory
- Make irreversible changes without confirmation
- Generate Ren'Py code (that's renpy-cli's responsibility)

## Scope Boundaries

### In Scope

Character creation wizard, scene planning workflow, location creation, relationship mapping, story timeline management, AI prompt generation for images, JSON data management, chat interface for story queries, search across story elements.

### Out of Scope

Ren'Py script generation, image generation, video generation, LoRA training, game testing/preview, asset management, multi-project support, collaboration features, cloud sync, GUI version, plugin system.

## Governance

This constitution supersedes all other project documentation when conflicts arise.

**Amendment Process**:
1. Propose change with rationale
2. Verify change doesn't conflict with existing principles
3. Update constitution with new version number
4. Propagate changes to dependent templates if needed

**Versioning**: MAJOR.MINOR.PATCH
- MAJOR: Principle removal or fundamental redefinition
- MINOR: New principle or section added
- PATCH: Clarifications and wording improvements

**Compliance**: All PRs and code reviews MUST verify alignment with these principles. Deviations require explicit justification documented in the relevant spec or plan.

**Version**: 1.0.0 | **Ratified**: 2025-12-09 | **Last Amended**: 2025-12-09
