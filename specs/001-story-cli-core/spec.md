# Feature Specification: Story CLI - Core Foundation & Character Creation

**Feature Branch**: `001-story-cli-core`
**Created**: 2025-12-10
**Updated**: 2025-12-10 (scope narrowed to foundation + character creation)
**Status**: Draft
**Input**: User description: "Story CLI core foundation - a terminal-based creative writing assistant for visual novel authors. This version establishes the CLI command line, full integrated Python package using local LLM (Ollama/Qwen3-32B), and the first feature: character creation using LLM and agentic tools."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Project Initialization (Priority: P1)

A visual novel writer wants to initialize a new story project so they have a clean workspace with proper folder structure.

**Why this priority**: Without a project, no other features can be used. This is the entry point for all workflows.

**Independent Test**: Can be fully tested by running `story init <project-name>` and verifying the project structure exists with correct metadata.

**Acceptance Scenarios**:

1. **Given** the CLI is installed, **When** the writer runs `story init <project-name>`, **Then** a project directory is created with the specified name
2. **Given** a project is being initialized, **When** the command completes, **Then** a `story_data/` subdirectory is created with `characters/` folder
3. **Given** a project is being initialized, **When** the command completes, **Then** a `story.json` config file is created with project metadata
4. **Given** the writer runs `story init`, **When** prompted, **Then** they enter project name, genre, and brief synopsis
5. **Given** a project name contains special characters, **When** the writer attempts creation, **Then** the system rejects it with a validation error
6. **Given** a project with the same name exists, **When** the writer attempts creation, **Then** the system warns and offers options (overwrite, rename, cancel)

---

### User Story 2 - Open Existing Project (Priority: P1)

A writer wants to open an existing project so they can continue working on their story.

**Why this priority**: Opening projects is essential for any multi-session workflow. Writers need to resume work on existing stories.

**Independent Test**: Can be fully tested by creating a project, closing the CLI, then reopening the project and verifying all data is accessible.

**Acceptance Scenarios**:

1. **Given** the CLI is in a project directory, **When** the writer runs `story open`, **Then** the project is loaded from the current directory
2. **Given** a valid project path, **When** the writer runs `story open <path>`, **Then** the project is loaded from the specified path
3. **Given** a project is being opened, **When** the structure is validated, **Then** the system shows a project summary (character count, last modified date)
4. **Given** an invalid or corrupted project, **When** the writer attempts to open it, **Then** the system displays a clear error indicating what's wrong

---

### User Story 3 - Character Management (Priority: P1)

Characters are the foundation of visual novels. This story covers the complete character lifecycle.

**Why this priority**: Writers need to create detailed, consistent characters before writing scenes.

#### US-3.1: Start Character Wizard

A writer wants to create a new character through a guided wizard to capture all necessary details systematically.

**Acceptance Scenarios**:
1. **Given** a project is open, **When** the writer runs `story new character`, **Then** the wizard starts
2. **Given** the writer runs `story new character --name "Alex"`, **When** the wizard starts, **Then** the name is pre-filled
3. **Given** the wizard is running, **When** viewing any phase, **Then** a progress indicator shows current phase
4. **Given** the wizard is running, **When** the writer quits, **Then** they are offered a partial save option

#### US-3.2: Character Basics Phase

A writer wants to define basic character information to establish the character's identity.

**Acceptance Scenarios**:
1. **Given** the basics phase, **When** completing it, **Then** name (required), age, gender, and role are collected
2. **Given** role selection, **When** choosing, **Then** options are: protagonist, love_interest, antagonist, supporting, background
3. **Given** the writer requests suggestions, **When** AI responds, **Then** name ideas based on genre are provided
4. **Given** a name is entered, **When** validating, **Then** uniqueness within project is enforced

#### US-3.3: Character Appearance Phase

A writer wants to describe character appearance in detail for consistent AI image generation.

**Acceptance Scenarios**:
1. **Given** the appearance phase, **When** completing it, **Then** hair (color, style, length), eyes (color, shape), skin_tone, height, build are collected
2. **Given** the appearance phase, **When** completing it, **Then** distinctive_features (list), clothing_style, accessories are collected
3. **Given** a brief description like "tall blonde athletic type", **When** AI processes it, **Then** structured appearance details are generated
4. **Given** appearance is complete, **When** previewing, **Then** a structured summary is displayed
5. **Given** appearance is complete, **When** saving, **Then** a lora_trigger string is generated for image generation

#### US-3.4: Character Personality Phase

A writer wants to define character personality traits for consistent dialogue and actions.

**Acceptance Scenarios**:
1. **Given** the personality phase, **When** completing it, **Then** primary_traits (3-5), secondary_traits (2-3), flaws (1-3) are collected
2. **Given** the personality phase, **When** completing it, **Then** speaking_style (formal, casual, slang, etc.) and speech_quirks are collected
3. **Given** the personality phase, **When** completing it, **Then** motivations (list), fears (list), secrets (list) are collected
4. **Given** the writer requests suggestions, **When** AI responds, **Then** traits based on role and archetype are suggested
5. **Given** traits are entered, **When** validating, **Then** contradictions (e.g., "brave" + "cowardly") are flagged

#### US-3.5: Character Backstory Phase

A writer wants to write character backstory to understand their history and motivations.

**Acceptance Scenarios**:
1. **Given** the backstory phase, **When** completing it, **Then** backstory_summary (short) and backstory_full (detailed, optional) are collected
2. **Given** the backstory phase, **When** completing it, **Then** key_events (list of formative moments) are collected
3. **Given** the backstory phase, **When** completing it, **Then** secrets (things other characters don't know) are collected
4. **Given** brief notes, **When** AI expands them, **Then** a full backstory is generated
5. **Given** the writer requests help, **When** AI responds, **Then** questions to flesh out backstory are generated

#### US-3.6: Character Relationships Phase

A writer wants to define how this character relates to others for consistent interactions.

**Acceptance Scenarios**:
1. **Given** the relationships phase, **When** starting, **Then** a list of existing characters is shown
2. **Given** defining a relationship, **When** completing it, **Then** character, relationship_type, and dynamic description are collected
3. **Given** relationship type selection, **When** choosing, **Then** options are: family, friend, enemy, romantic, professional, acquaintance
4. **Given** defining a relationship, **When** completing it, **Then** initial_feeling, history, tension_points are collected
5. **Given** a relationship is defined, **When** saving, **Then** the system prompts to update the other character's relationship entry (bidirectional)

#### US-3.7: Character Review and Save

A writer wants to review the complete character before saving to catch any issues.

**Acceptance Scenarios**:
1. **Given** all phases complete, **When** reviewing, **Then** the complete character profile is shown in formatted view
2. **Given** the review phase, **When** viewing, **Then** missing recommended fields are highlighted
3. **Given** the review phase, **When** choosing actions, **Then** options are: Save, Edit (go to specific phase), Regenerate (AI rewrites section), Cancel
4. **Given** saving, **When** complete, **Then** character is saved to `story_data/characters/<name>/description.json`
5. **Given** saving, **When** complete, **Then** `characters_index.json` is updated with character reference

#### US-3.8: Edit Existing Character

A writer wants to edit an existing character to refine them as the story evolves.

**Acceptance Scenarios**:
1. **Given** a character exists, **When** running `story edit character <name>`, **Then** the character is opened for editing
2. **Given** editing, **When** running `story edit character alex --phase appearance`, **Then** that specific phase opens directly
3. **Given** changes are made, **When** saving, **Then** a diff is shown before confirming
4. **Given** changes break relationship references, **When** saving, **Then** a warning is displayed

#### US-3.9: List Characters

A writer wants to see all characters in the project to navigate their cast.

**Acceptance Scenarios**:
1. **Given** a project has characters, **When** running `story list characters`, **Then** a character table is displayed
2. **Given** the list view, **When** viewing, **Then** columns show: Name, Role, Age, Completion %
3. **Given** the list view, **When** using `--detailed`, **Then** full info is shown
4. **Given** the list view, **When** using `--json`, **Then** raw JSON output is returned
5. **Given** the list view, **When** using `--role protagonist`, **Then** only protagonists are shown

---

### User Story 4 - Interactive Chat Session (Priority: P2)

A writer wants to have an interactive conversation with the LLM to brainstorm ideas, discuss characters, or get writing assistance.

**Why this priority**: Provides a flexible interface for AI-assisted creative work beyond structured wizards.

**Independent Test**: Can be fully tested by running `story chat` and verifying the interactive session starts and responds to user input.

**Acceptance Scenarios**:

1. **Given** a project is open, **When** the writer runs `story chat`, **Then** an interactive chat session starts
2. **Given** a chat session is active, **When** the writer types a message, **Then** the LLM responds with streaming output
3. **Given** a chat session is active, **When** the writer types "exit" or presses Ctrl+C, **Then** the session ends gracefully
4. **Given** a chat session is active, **When** the LLM is unavailable, **Then** a clear error message is shown

---

### Edge Cases

- What happens when the local LLM is not available or not responding? System should display a clear error message and allow non-AI workflows to continue.
- How does the system handle very long character backstories? Content should be accepted up to reasonable limits with clear feedback if limits are exceeded.
- What happens when a character is deleted but referenced in relationships? System should warn about dependencies and offer options (remove references, cancel).
- How does the system handle concurrent edits if the project is accessed from multiple terminals? The system assumes single-user access; last-write-wins with no locking mechanism.
- What if the LLM generates inappropriate or inconsistent content? Users can regenerate or manually edit any AI-generated content.

## Requirements *(mandatory)*

### Functional Requirements

#### Core CLI & Package Foundation

- **FR-001**: System MUST be installable as a Python package via pip with a `story` command-line entry point
- **FR-002**: System MUST allow users to initialize projects via `story init <project-name>`, prompting for name, genre, and synopsis, creating `story_data/` with `characters/` subdirectory
- **FR-003**: System MUST allow users to open existing projects from current directory (`story open`) or specified path (`story open <path>`)
- **FR-004**: System MUST validate project structure when opening and display a summary (character count, last modified)
- **FR-005**: System MUST persist all data locally in JSON format
- **FR-006**: System MUST function offline, using only local resources
- **FR-007**: System MUST provide clear terminal-based UI with navigable menus and prompts
- **FR-008**: System MUST gracefully handle LLM unavailability and allow non-AI workflows to continue

#### Local LLM Integration

- **FR-009**: System MUST integrate with local LLM (Ollama) for AI-assisted content generation
- **FR-010**: System MUST support configurable LLM model selection (default: Qwen3-32B)
- **FR-011**: System MUST implement agentic tool-calling patterns for structured character generation
- **FR-012**: System MUST provide streaming responses from LLM for real-time feedback during generation
- **FR-012a**: System MUST use 10-second connection timeout for LLM; no timeout once streaming begins

#### Character Creation & Management

- **FR-013**: System MUST provide a guided wizard for character creation with phases: basics, appearance, personality, backstory, and relationships
- **FR-014**: System MUST use LLM to suggest and expand character attributes based on user input
- **FR-015**: System MUST support defining relationships between characters with relationship types (friend, rival, family, romantic, professional, acquaintance)
- **FR-016**: System MUST auto-generate character LoRA trigger keywords from appearance attributes
- **FR-017**: System MUST auto-generate and maintain character index file that rebuilds when characters change
- **FR-018**: System MUST allow editing existing characters via `story edit character <name>` with direct phase access
- **FR-019**: System MUST allow deletion of characters via `story delete character <name>` with dependency warnings
- **FR-020**: System MUST support listing characters via `story list characters` with filtering and output format options
- **FR-021**: System MUST provide interactive chat session via `story chat` command with streaming LLM responses
- **FR-022**: System MUST validate data integrity when deleting characters with relationship references

### Key Entities

- **Project**: Container for all story data; has name, genre (informs AI content generation), synopsis (brief story summary), creation date; stored in `story.json`
- **Character**: Represents a story character stored in `story_data/characters/<name>/description.json`; has:
  - **Basics**: name (required, unique), age, gender, role (protagonist/love_interest/antagonist/supporting/background)
  - **Appearance**: hair (color, style, length), eyes (color, shape), skin_tone, height, build, distinctive_features, clothing_style, accessories, lora_trigger (auto-generated)
  - **Personality**: primary_traits (3-5), secondary_traits (2-3), flaws (1-3), speaking_style, speech_quirks, motivations, fears, secrets
  - **Backstory**: backstory_summary, backstory_full (optional), key_events (list)
  - **Relationships**: list of relationships to other characters with type, dynamic, initial_feeling, history, tension_points
- **Character Index**: Auto-generated lookup index for all characters; rebuilds when characters are added, modified, or deleted; stored in `characters_index.json`
- **Relationship**: Defines a connection between two characters; has type (friend/rival/family/romantic/professional/acquaintance), dynamic description, initial_feeling, history, and tension_points
- **LLM Configuration**: System-level settings via environment variables: `STORY_OLLAMA_HOST` (default: localhost:11434), `STORY_MODEL` (default: qwen3:32b)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can install the package and create a new project within 5 minutes
- **SC-002**: Users can create their first character with AI assistance within 10 minutes of project creation
- **SC-003**: Character creation wizard captures all required attributes (name, appearance, personality, backstory, relationships) in a single guided session
- **SC-004**: AI-assisted character generation produces coherent, usable character profiles 90% of the time
- **SC-005**: Interactive chat session starts and responds to first message within 10 seconds
- **SC-006**: System remains fully functional for core workflows (create, edit, list) when LLM is unavailable
- **SC-007**: All project data persists correctly across CLI sessions with zero data loss
- **SC-008**: LLM integration provides real-time streaming feedback during character generation

## Clarifications

### Session 2025-12-10

- Q: How should character LoRA triggers be used? → A: Store LoRA trigger keywords per character (auto-generated from appearance), for use in future image generation features.
- Q: Should genre be part of project metadata? → A: Yes, genre is part of project metadata and informs AI content generation (tone, tropes, vocabulary appropriate to the genre).
- Q: What project settings should be configurable? → A: None per-project. story.json contains story metadata only (name, genre, synopsis). LLM configuration is system-level.
- Q: How does multi-project support work? → A: Multiple projects supported. `story open` in project directory loads it; `story open <path>` loads from specified path. Validates structure and shows summary.
- Q: What is the exact project initialization command and structure? → A: `story init <project-name>` creates project directory with `story_data/` containing `characters/` subdirectory and `story.json` with name, genre, synopsis.
- Q: How should the character index be managed? → A: Auto-generated index file that rebuilds automatically when characters are added, modified, or deleted.
- Q: How should agentic LLM integration work? → A: LLM uses tool-calling patterns to generate structured character data, with streaming responses for real-time feedback.
- Q: How long should the system wait for LLM responses before timing out? → A: 10-second connection timeout; once streaming begins, generation continues until complete (no timeout on streaming content).
- Q: What is the character deletion command? → A: `story delete character <name>` - follows the established CLI pattern (matches edit/list).
- Q: What command should users run to query characters? → A: `story chat` opens interactive LLM chat session; structured retrieval tools (RAG, semantic search) deferred to future version.
- Q: Where should LLM configuration be stored? → A: Environment variables: `STORY_OLLAMA_HOST` (default: localhost:11434) and `STORY_MODEL` (default: qwen3:32b).

## Out of Scope

The following features are explicitly **NOT** included in this version:

### Deferred to Future Versions

- **Scene Generation**: Scene creation, planning, and AI-assisted scene beats (future feature)
- **Location Creation**: Location/setting management with time-of-day variants (future feature)
- **Ren'Py Export**: JSON export for renpy-cli integration (future feature)
- **Panel/Visual Prompts**: AI-ready image/video prompts for scenes (future feature)
- **Story Timeline**: Auto-computed scene timeline with state tracking (future feature)
- **Character Arcs**: Tracking character emotional states across scenes (future feature - depends on scenes)
- **Retrieval Tools**: RAG, semantic search, and structured query tools for chat (future feature)

### Not Planned

- **Image/Video Generation**: Story CLI generates prompts only; actual generation handled by external tools
- **Audio/Voice**: No voice synthesis, sound effects, or music generation
- **Cloud Sync**: All data is local; no cloud storage, sync, or backup to remote servers
- **Multi-User/Collaboration**: Single-user only; no real-time collaboration, user accounts, or access control
- **GUI/Web Interface**: Terminal-based only; no graphical or web-based interface
- **Version Control**: No built-in project versioning or history; users can use external git if needed
- **Plugin System**: No extensibility via plugins or custom scripts
- **Data Import**: No import from external sources (JSON, markdown, etc.); all content created via wizards

## Assumptions

- Users have Python 3.10+ installed for package installation
- Users have a local LLM (Ollama with Qwen3-32B or similar) installed and running for AI features
- Users are comfortable with terminal-based interfaces and command-line workflows
- Single-user access pattern; no concurrent editing from multiple terminals
- Projects are stored in the local filesystem with standard read/write permissions
- Ollama API is available at localhost:11434 (default) or user-configured endpoint
