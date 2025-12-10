# Data Model: Story CLI Markdown Guide

**Feature**: 002-docs-html-guide
**Date**: 2025-12-10

## Overview

This feature creates documentation files only—no runtime data models. This document describes the **content structure** of each documentation file for implementation guidance.

## Documentation Entities

### Guide (Markdown File)

A single `.md` file in the `docs/` folder covering one topic.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| Title | H1 heading | Yes | Document title (e.g., "# Installation Guide") |
| Introduction | Paragraph | Yes | 2-3 sentences explaining purpose |
| Sections | H2 headings | Yes | Logical breakdown of content |
| Navigation | Links | Yes | Link to index and related guides |
| Examples | Code blocks | Per topic | Fenced code with syntax highlighting |
| AI Callouts | Blockquotes | Per topic | 🤖 prefix for AI features |

### Index (docs/README.md)

The entry point for documentation navigation.

| Section | Required | Content |
|---------|----------|---------|
| Title | Yes | "# Story CLI Documentation" |
| Overview | Yes | Brief project description |
| Quick Links | Yes | Table of guides with descriptions |
| Prerequisites | Yes | Link to installation guide |
| Getting Help | Optional | Links to issues/discussions |

### Code Example

Structured command demonstration within guides.

| Component | Format | Description |
|-----------|--------|-------------|
| Command | ```bash block | The command to run |
| Output | ```text block | Expected terminal output |
| Explanation | Paragraph | What the command does |

### AI Callout

Visual marker for AI-assisted features.

| Format | Rendering |
|--------|-----------|
| `> 🤖 **AI Feature**: Description` | Blockquote with robot emoji |

## File Specifications

### docs/README.md (Index)

```
# Story CLI Documentation

## Overview
[2-3 sentence project description]

## Guides

| Guide | Description |
|-------|-------------|
| [Installation](./installation.md) | ... |
| [LLM Setup](./llm-setup.md) | ... |
| [Story Management](./story-guide.md) | ... |
| [Character Management](./character-guide.md) | ... |

## Prerequisites
[Link to installation]
```

### docs/installation.md

```
# Installation Guide

## Prerequisites
- Python 3.11+
- pip

## Installation
[pip install command]

## Verification
[story --version command]

## Troubleshooting
[Common issues]

## Next Steps
[Link to LLM setup]
```

### docs/llm-setup.md

```
# LLM Setup Guide

## What is Ollama?
[Explanation]

## Installation
[Platform-specific instructions]

## Configuration
[Environment variables: STORY_OLLAMA_HOST, STORY_MODEL]

## Verification
[ollama list, story chat test]

## Offline Mode
[What works without LLM]

## Troubleshooting
[Connection issues]
```

### docs/story-guide.md

```
# Story Management Guide

## Creating a Project
[story init command with example]

## Opening a Project
[story open command]

## Project Structure
[Folder layout explanation]

## AI Chat
[story chat with AI callout]

## Next Steps
[Link to character guide]
```

### docs/character-guide.md

```
# Character Management Guide

## Overview
[Character system intro]

## Creating a Character (Wizard)
### Phase 1: Basics
[🤖 AI Feature: name suggestions]

### Phase 2: Appearance
[🤖 AI Feature: appearance expansion]

### Phase 3: Personality
[🤖 AI Feature: trait suggestions]

### Phase 4: Backstory
[🤖 AI Feature: backstory questions]

### Phase 5: Relationships
[Relationship definition]

## Editing Characters
[story edit character command]

## Listing Characters
[story list characters with flags]

## Deleting Characters
[story delete character with warnings]
```

## Relationships

```
docs/README.md
    │
    ├── docs/installation.md
    │       │
    │       └── docs/llm-setup.md
    │               │
    │               └── docs/story-guide.md
    │                       │
    │                       └── docs/character-guide.md
```

Navigation flow: Index → Installation → LLM Setup → Story Guide → Character Guide

Each guide links back to the index and to the next logical guide.

## Validation Rules

1. **All relative links must work on GitHub** — Test by clicking links in GitHub web UI
2. **All code blocks must specify language** — Enables syntax highlighting
3. **AI callouts must use consistent format** — `> 🤖 **AI Feature**:` prefix
4. **No external image dependencies** — Text and emoji only
5. **Commands must match actual CLI** — Verify with `story --help`
