# Feature Specification: Story CLI Markdown Guide

**Feature Branch**: `002-docs-html-guide`
**Created**: 2025-12-10
**Status**: Draft
**Input**: User description: "High-level documentation/guide as organized Markdown files readable locally and on GitHub - no static site generator, just .md files updated with new features"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View Installation Guide (Priority: P1)

A new user discovers Story CLI and wants to install it. They browse the `docs/` folder on GitHub or locally and follow the installation guide to get started.

**Why this priority**: Installation is the first barrier to adoption. Without clear installation instructions, users cannot use the tool at all.

**Independent Test**: Can be fully tested by following the installation guide on a fresh system and verifying `story --help` works.

**Acceptance Scenarios**:

1. **Given** a user browsing the repository on GitHub, **When** they navigate to `docs/`, **Then** they see a clear README linking to all guides.
2. **Given** a user reading `docs/installation.md`, **When** they follow the steps, **Then** they can run `story --version` successfully.
3. **Given** a user on macOS, Linux, or Windows, **When** they follow the installation guide, **Then** they complete installation without errors.

---

### User Story 2 - Set Up Local LLM Server (Priority: P1)

A user wants to enable AI-assisted features in Story CLI. They read the LLM setup guide to install and configure Ollama.

**Why this priority**: AI assistance is a core value proposition. Users need to understand how to set up the LLM to benefit from AI features.

**Independent Test**: Can be tested by following the LLM setup guide and verifying `story chat` responds with AI-generated content.

**Acceptance Scenarios**:

1. **Given** a user reading `docs/llm-setup.md`, **When** they read the introduction, **Then** they understand what Ollama is and why it's needed.
2. **Given** a user following the Ollama installation steps, **When** they complete setup, **Then** they can verify the LLM is running with `ollama list`.
3. **Given** a user who cannot install Ollama, **When** they read the guide, **Then** they understand which features still work without AI (offline mode).

---

### User Story 3 - Learn Story Project Management (Priority: P2)

A user wants to understand how to create, open, and manage story projects. They read the story guide to learn the workflow.

**Why this priority**: Project management is fundamental to using the tool.

**Independent Test**: Can be tested by following the guide to create a new project and open it.

**Acceptance Scenarios**:

1. **Given** a user reading `docs/story-guide.md`, **When** they follow the "Create Project" section, **Then** they successfully create a new story project.
2. **Given** a user with an existing project, **When** they follow the "Open Project" section, **Then** they can open and view their project summary.
3. **Given** a user reading about AI assistance, **When** they review the guide, **Then** they understand that `story chat` enables AI brainstorming.

---

### User Story 4 - Learn Character Management (Priority: P2)

A user wants to create characters for their visual novel. They read the character guide to understand the wizard and CRUD operations, with emphasis on AI assistance.

**Why this priority**: Character creation is the most feature-rich part of Story CLI with significant AI integration.

**Independent Test**: Can be tested by following the guide to create, edit, list, and delete a character.

**Acceptance Scenarios**:

1. **Given** a user reading `docs/character-guide.md`, **When** they follow the wizard section, **Then** they understand all 5 phases (basics, appearance, personality, backstory, relationships).
2. **Given** a user reading about AI assistance, **When** they review each wizard phase, **Then** they see clear indicators of where AI helps (name suggestions, appearance expansion, trait suggestions, backstory questions).
3. **Given** a user wanting to manage characters, **When** they read the edit/list/delete sections, **Then** they know the commands and options available.

---

### User Story 5 - Navigate Documentation (Priority: P3)

A user wants to quickly find information across the documentation. They use the index/README to navigate between guides.

**Why this priority**: Good navigation improves usability but users can also browse files directly.

**Independent Test**: Can be tested by verifying all links in the docs README work correctly.

**Acceptance Scenarios**:

1. **Given** a user viewing `docs/README.md`, **When** they look for a topic, **Then** they find a clear table of contents with links to all guides.
2. **Given** a user reading any guide, **When** they want to go to another section, **Then** they find navigation links back to the index.

---

### Edge Cases

- What happens when a user tries to use AI features without Ollama running? Documentation should explain graceful degradation and error messages.
- What happens if a user has a different LLM server? Documentation should mention environment variable configuration (`STORY_OLLAMA_HOST`, `STORY_MODEL`).
- What if the user's Python version is incompatible? Documentation should clearly state Python 3.11+ requirement upfront.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Documentation MUST be in a `docs/` folder at the repository root.
- **FR-002**: Documentation MUST consist of plain Markdown files (`.md`) that render correctly on GitHub and locally.
- **FR-003**: Documentation MUST include a `docs/README.md` serving as an index with links to all guides.
- **FR-004**: Documentation MUST include `docs/installation.md` covering prerequisites, pip installation, and verification.
- **FR-005**: Documentation MUST include `docs/llm-setup.md` explaining Ollama installation, model configuration, and offline mode.
- **FR-006**: Documentation MUST include `docs/story-guide.md` covering project creation, opening, and AI-assisted brainstorming.
- **FR-007**: Documentation MUST include `docs/character-guide.md` covering the wizard phases, editing, listing, deletion, and AI assistance details.
- **FR-008**: Each guide MUST clearly indicate where AI assistance is available using a consistent visual marker (e.g., "🤖 AI Feature" callout).
- **FR-009**: Documentation MUST include command examples with copy-pasteable code blocks.
- **FR-010**: Documentation MUST explain environment variable configuration for LLM settings.
- **FR-011**: Documentation MUST be kept up-to-date when new features are added to Story CLI.
- **FR-012**: All internal links between documentation files MUST use relative paths that work on GitHub and locally.

### Key Entities

- **Guide**: A single Markdown file covering one topic (e.g., installation, characters).
- **Index**: The `docs/README.md` file providing navigation to all guides.
- **Code Example**: Fenced code block showing Story CLI command with optional output.
- **AI Callout**: Visual indicator marking features that use AI assistance.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A new user can go from zero to running `story --help` in under 10 minutes following only the documentation.
- **SC-002**: A user can set up Ollama and verify AI features work in under 15 minutes following the documentation.
- **SC-003**: Documentation covers 100% of Story CLI commands (`init`, `open`, `chat`, `new character`, `edit character`, `list characters`, `delete character`).
- **SC-004**: Each AI-assisted feature has a clear callout explaining what the AI does and when it's invoked.
- **SC-005**: All Markdown files render correctly when viewed on GitHub (no broken links, images, or formatting).
- **SC-006**: All Markdown files are readable locally with any text editor or Markdown viewer.

## Assumptions

- Users have basic familiarity with command-line interfaces.
- Users have Python 3.11+ already installed or can install it themselves.
- Users can read Markdown either via GitHub's rendered view or a local Markdown viewer/editor.
- No build step is required - documentation is plain Markdown files.

## Out of Scope

- Static site generators (MkDocs, Sphinx, Jekyll, etc.).
- HTML generation or hosting.
- Custom styling or theming.
- Automated documentation deployment (CI/CD).
- API reference documentation for developers.
- Video tutorials or interactive guides.
- Internationalization/localization.

