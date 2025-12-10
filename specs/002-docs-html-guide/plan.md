# Implementation Plan: Story CLI Markdown Guide

**Branch**: `002-docs-html-guide` | **Date**: 2025-12-10 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-docs-html-guide/spec.md`

## Summary

Create comprehensive user documentation as plain Markdown files in a `docs/` folder. Documentation covers installation, LLM setup (Ollama), story project management, and character management with clear AI feature callouts (🤖). Files render natively on GitHub and are readable locally—no build step required.

## Technical Context

**Language/Version**: Markdown (CommonMark/GFM compatible)
**Primary Dependencies**: None (plain text files)
**Storage**: `docs/` folder at repository root
**Testing**: Manual verification of links and rendering on GitHub
**Target Platform**: GitHub web UI, local text editors, Markdown viewers
**Project Type**: Documentation only (no code)
**Performance Goals**: N/A
**Constraints**: Must render correctly on GitHub without preprocessing
**Scale/Scope**: 5 documentation files (~500-1000 lines total)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Writer-First Design | ✅ PASS | Documentation helps writers understand and use the tool |
| II. Structured Creativity | ✅ PASS | Organized guides follow logical learning progression |
| III. Local-First, Privacy-Respecting | ✅ PASS | Markdown files stored locally, no cloud dependencies |
| IV. Iterative Refinement | ✅ PASS | Documentation can be updated with new features |
| V. Interoperability | ✅ PASS | Standard Markdown readable by any tool |

**Technical Constraints Compliance:**
- ✅ No code changes, only documentation
- ✅ Documents existing Python/Typer/Rich/LangGraph implementation
- ✅ Explains Ollama integration without requiring internet
- ✅ No external dependencies introduced

**GATE RESULT: PASS** — No violations. Proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/002-docs-html-guide/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output (minimal for docs)
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (created by /speckit.tasks)
```

### Source Code (repository root)

```text
docs/                    # NEW: Documentation folder
├── README.md            # Index with links to all guides
├── installation.md      # Prerequisites, pip install, verification
├── llm-setup.md         # Ollama installation and configuration
├── story-guide.md       # Project creation, opening, chat
└── character-guide.md   # Wizard phases, CRUD, AI features
```

**Structure Decision**: Documentation-only feature. No changes to existing `story_cli/` source structure. Creates new `docs/` folder at repository root containing 5 Markdown files.

## Complexity Tracking

> No violations to justify. This is a straightforward documentation feature.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| (none) | — | — |
