# Tasks: Story CLI - Core Foundation & Character Creation

**Input**: Design documents from `/specs/001-story-cli-core/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Not explicitly requested in spec. Tests can be added later.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

Based on plan.md structure:
- Source: `story_cli/` (Python package)
- Tests: `tests/` (pytest)
- Config: `pyproject.toml` at repository root

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Create Python package structure and configure dependencies

- [x] T001 Create pyproject.toml with dependencies: typer, rich, langgraph, langchain-ollama, pydantic
- [x] T002 Create story_cli/__init__.py with version and package metadata
- [x] T003 Create story_cli/__main__.py as entry point for `python -m story_cli`
- [x] T004 [P] Create story_cli/cli/__init__.py module initialization
- [x] T005 [P] Create story_cli/models/__init__.py module initialization
- [x] T006 [P] Create story_cli/services/__init__.py module initialization
- [x] T007 [P] Create story_cli/workflows/__init__.py module initialization
- [x] T008 [P] Create story_cli/prompts/__init__.py module initialization
- [x] T009 [P] Create story_cli/utils/__init__.py module initialization
- [x] T010 [P] Create tests/conftest.py with shared pytest fixtures
- [x] T011 Configure pytest in pyproject.toml

**Checkpoint**: Package installs with `pip install -e .` and `story --help` shows CLI

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T012 [P] Create story_cli/utils/config.py with environment variable handling (STORY_OLLAMA_HOST, STORY_MODEL)
- [x] T013 [P] Create story_cli/utils/validation.py with input validation helpers (name validation, filesystem-safe checks)
- [x] T014 [P] Create story_cli/utils/display.py with Rich formatting helpers (panels, tables, progress bars)
- [x] T015 [P] Create story_cli/models/enums.py with CharacterRole and RelationshipType enums
- [x] T016 [P] Create story_cli/models/exceptions.py with custom exceptions (StoryCliError, ProjectNotFoundError, etc.)
- [x] T017 Create story_cli/cli/main.py with Typer app and command group registration
- [x] T018 Create story_cli/services/llm_service.py with Ollama client, availability check, and streaming support

**Checkpoint**: Foundation ready - `story --help` shows all command groups, LLM connection testable

---

## Phase 3: User Story 1 - Project Initialization (Priority: P1) 🎯 MVP

**Goal**: Enable writers to create new story projects with proper folder structure and metadata

**Independent Test**: Run `story init my-project`, verify `my-project/story.json` and `my-project/story_data/characters/` exist

### Implementation for User Story 1

- [x] T019 [P] [US1] Create Project Pydantic model in story_cli/models/project.py
- [x] T020 [US1] Implement ProjectService.create_project() in story_cli/services/project_service.py
- [x] T021 [US1] Implement ProjectService.validate_project() in story_cli/services/project_service.py
- [x] T022 [US1] Implement story init command in story_cli/cli/init_cmd.py with prompts for name, genre, synopsis
- [x] T023 [US1] Add name validation and duplicate project handling to init command
- [x] T024 [US1] Add Rich formatting for project creation success/error messages

**Checkpoint**: `story init <name>` creates valid project structure with prompted metadata

---

## Phase 4: User Story 2 - Open Existing Project (Priority: P1)

**Goal**: Enable writers to open and validate existing projects

**Independent Test**: Create a project, then run `story open` or `story open <path>`, verify summary is displayed

### Implementation for User Story 2

- [x] T025 [US2] Implement ProjectService.open_project() in story_cli/services/project_service.py
- [x] T026 [US2] Implement ProjectService.get_project_summary() in story_cli/services/project_service.py
- [x] T027 [US2] Implement story open command in story_cli/cli/open_cmd.py with path argument
- [x] T028 [US2] Add validation error display and project summary formatting with Rich
- [x] T029 [US2] Add project context management (store currently open project path)

**Checkpoint**: `story open` loads project and displays character count, last modified

---

## Phase 5: User Story 3 - Character Management (Priority: P1)

**Goal**: Complete character lifecycle: create wizard, edit, list, delete

**Independent Test**: Run wizard to create character, then list/edit/delete it

### US-3.1 through US-3.7: Character Models & Service (Foundation)

- [x] T030 [P] [US3] Create CharacterBasics model in story_cli/models/character.py
- [x] T031 [P] [US3] Create HairDescription, EyeDescription models in story_cli/models/character.py
- [x] T032 [P] [US3] Create CharacterAppearance model in story_cli/models/character.py
- [x] T033 [P] [US3] Create CharacterPersonality model in story_cli/models/character.py
- [x] T034 [P] [US3] Create CharacterBackstory model in story_cli/models/character.py
- [x] T035 [P] [US3] Create Relationship model in story_cli/models/relationship.py
- [x] T036 [US3] Create complete Character model with lora_trigger generation in story_cli/models/character.py
- [x] T037 [US3] Create CharacterIndex and CharacterIndexEntry models in story_cli/models/character.py
- [x] T038 [US3] Implement CharacterService.create_character() in story_cli/services/character_service.py
- [x] T039 [US3] Implement CharacterService.get_character() in story_cli/services/character_service.py
- [x] T040 [US3] Implement CharacterService.update_character() in story_cli/services/character_service.py
- [x] T041 [US3] Implement CharacterService.rebuild_index() in story_cli/services/character_service.py

### US-3.1 through US-3.7: LLM Prompts & AI Features

- [x] T042 [P] [US3] Create name suggestion prompt in story_cli/prompts/character_prompts.py
- [x] T043 [P] [US3] Create appearance expansion prompt in story_cli/prompts/character_prompts.py
- [x] T044 [P] [US3] Create trait suggestion prompt in story_cli/prompts/character_prompts.py
- [x] T045 [P] [US3] Create backstory expansion prompt in story_cli/prompts/character_prompts.py
- [x] T046 [P] [US3] Create backstory questions prompt in story_cli/prompts/character_prompts.py
- [x] T047 [US3] Implement LLMService.suggest_names() in story_cli/services/llm_service.py
- [x] T048 [US3] Implement LLMService.expand_appearance() in story_cli/services/llm_service.py
- [x] T049 [US3] Implement LLMService.suggest_traits() in story_cli/services/llm_service.py
- [x] T050 [US3] Implement LLMService.expand_backstory() in story_cli/services/llm_service.py
- [x] T051 [US3] Implement LLMService.generate_backstory_questions() in story_cli/services/llm_service.py
- [x] T052 [US3] Implement LLMService.check_trait_contradictions() in story_cli/services/llm_service.py

### US-3.1 through US-3.7: Character Wizard (LangGraph)

- [x] T053 [US3] Define CharacterWizardState TypedDict in story_cli/workflows/character_wizard.py (implemented inline in character_cmd.py)
- [x] T054 [US3] Implement basics_node() wizard phase in story_cli/workflows/character_wizard.py (implemented as _wizard_basics)
- [x] T055 [US3] Implement appearance_node() wizard phase in story_cli/workflows/character_wizard.py (implemented as _wizard_appearance)
- [x] T056 [US3] Implement personality_node() wizard phase in story_cli/workflows/character_wizard.py (implemented as _wizard_personality)
- [x] T057 [US3] Implement backstory_node() wizard phase in story_cli/workflows/character_wizard.py (implemented as _wizard_backstory)
- [x] T058 [US3] Implement relationships_node() wizard phase in story_cli/workflows/character_wizard.py (implemented as _wizard_relationships_info)
- [x] T059 [US3] Implement review_node() wizard phase in story_cli/workflows/character_wizard.py (implemented as _display_character_review)
- [x] T060 [US3] Implement save_node() wizard phase in story_cli/workflows/character_wizard.py (implemented in new_character)
- [x] T061 [US3] Create StateGraph with conditional edges and routing functions (simplified implementation)
- [ ] T062 [US3] Add partial save functionality when user quits mid-wizard
- [x] T063 [US3] Implement story new character command in story_cli/cli/character_cmd.py

### US-3.8: Edit Existing Character

- [x] T064 [US3] Implement story edit character command in story_cli/cli/character_cmd.py
- [x] T065 [US3] Add --phase flag support to open specific wizard phase
- [ ] T066 [US3] Add diff display before saving changes

### US-3.9: List Characters

- [x] T067 [US3] Implement CharacterService.list_characters() with role_filter in story_cli/services/character_service.py
- [x] T068 [US3] Implement story list characters command in story_cli/cli/character_cmd.py
- [x] T069 [US3] Add --detailed, --json, --role flags for list command

### Character Deletion (FR-019, FR-022)

- [x] T070 [US3] Implement CharacterService.delete_character() with dependency check in story_cli/services/character_service.py
- [x] T071 [US3] Implement CharacterService.get_relationship_dependencies() in story_cli/services/character_service.py
- [x] T072 [US3] Implement story delete character command in story_cli/cli/character_cmd.py
- [x] T073 [US3] Add --force flag and dependency warning display

**Checkpoint**: Complete character lifecycle works: create via wizard, list, edit, delete with dependency warnings

---

## Phase 6: User Story 4 - Interactive Chat Session (Priority: P2)

**Goal**: Freeform LLM conversation for brainstorming

**Independent Test**: Run `story chat`, send message, receive streaming response, exit gracefully

### Implementation for User Story 4

- [x] T074 [US4] Implement LLMService.chat_stream() with streaming in story_cli/services/llm_service.py
- [x] T075 [US4] Implement story chat command in story_cli/cli/chat_cmd.py
- [x] T076 [US4] Add chat loop with Rich Live display for streaming responses
- [x] T077 [US4] Add graceful exit handling (exit command, Ctrl+C)
- [x] T078 [US4] Add LLM unavailable error handling with clear message

**Checkpoint**: `story chat` starts session, streams responses, exits cleanly

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements affecting multiple user stories

- [x] T079 [P] Add README.md with installation and usage instructions
- [x] T080 [P] Add --help text improvements to all commands
- [ ] T081 Validate all JSON serialization/deserialization roundtrips
- [x] T082 Add consistent error handling and Rich formatting across all commands
- [ ] T083 Run quickstart.md validation (all documented commands work)
- [x] T084 Verify offline mode works (all non-LLM features work without Ollama)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - MVP target
- **User Story 2 (Phase 4)**: Depends on Foundational - Can parallel with US1
- **User Story 3 (Phase 5)**: Depends on Foundational + US1 (needs project) - Core feature
- **User Story 4 (Phase 6)**: Depends on Foundational + US2 (needs open project)
- **Polish (Phase 7)**: Depends on all user stories complete

### User Story Dependencies

```
Phase 1: Setup
    │
    ▼
Phase 2: Foundational ──────────────────────────────────────┐
    │                                                       │
    ├───────────────────────┬───────────────────────────────┤
    │                       │                               │
    ▼                       ▼                               │
Phase 3: US1           Phase 4: US2                         │
(story init)           (story open)                         │
    │                       │                               │
    └───────┬───────────────┘                               │
            │                                               │
            ▼                                               │
       Phase 5: US3                                         │
       (character                                           │
        management)                                         │
            │                                               │
            ├───────────────────────────────────────────────┤
            │                                               │
            ▼                                               ▼
       Phase 6: US4                              (can also start
       (story chat)                               from Phase 2)
            │
            ▼
       Phase 7: Polish
```

### Within Each User Story

1. Models before services
2. Services before CLI commands
3. Core implementation before optional features
4. All [P] tasks in a story can run in parallel

### Parallel Opportunities

**Phase 1 - All [P] tasks can run in parallel:**
- T004, T005, T006, T007, T008, T009, T010

**Phase 2 - All [P] tasks can run in parallel:**
- T012, T013, T014, T015, T016

**Phase 5 (US3) - Model creation can run in parallel:**
- T030, T031, T032, T033, T034, T035

**Phase 5 (US3) - Prompt creation can run in parallel:**
- T042, T043, T044, T045, T046

---

## Parallel Example: User Story 3 Models

```bash
# Launch all character models in parallel:
Task: "Create CharacterBasics model in story_cli/models/character.py"
Task: "Create HairDescription, EyeDescription models in story_cli/models/character.py"
Task: "Create CharacterAppearance model in story_cli/models/character.py"
Task: "Create CharacterPersonality model in story_cli/models/character.py"
Task: "Create CharacterBackstory model in story_cli/models/character.py"
Task: "Create Relationship model in story_cli/models/relationship.py"
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (story init)
4. Complete Phase 4: User Story 2 (story open)
5. **STOP and VALIDATE**: Can create and open projects
6. Deploy/demo if ready

### Core Feature Addition (User Story 3)

1. Complete MVP above
2. Complete Phase 5: User Story 3 (character management)
3. **VALIDATE**: Full character lifecycle works
4. This is the main value-add of the CLI

### Full Feature Set (User Story 4)

1. Complete above
2. Complete Phase 6: User Story 4 (chat)
3. Complete Phase 7: Polish
4. **VALIDATE**: All quickstart.md scenarios work

### Incremental Delivery

Each phase adds independently testable value:
- After Phase 3: Writers can create projects
- After Phase 4: Writers can reopen projects
- After Phase 5: Writers can create/manage characters with AI
- After Phase 6: Writers can brainstorm with AI
- After Phase 7: Production-ready polish

---

## Summary

| Phase | User Story | Tasks | Parallel |
|-------|------------|-------|----------|
| 1. Setup | - | 11 | 7 |
| 2. Foundational | - | 7 | 5 |
| 3. US1 - Init | P1 | 6 | 1 |
| 4. US2 - Open | P1 | 5 | 0 |
| 5. US3 - Characters | P1 | 44 | 11 |
| 6. US4 - Chat | P2 | 5 | 0 |
| 7. Polish | - | 6 | 2 |
| **Total** | | **84** | **26** |

**MVP Scope**: Phases 1-4 (29 tasks)
**Core Feature**: Phase 5 (44 tasks)
**Full Implementation**: All phases (84 tasks)

---

## Notes

- [P] tasks = different files, no dependencies within the same batch
- [Story] label maps task to specific user story for traceability
- Each user story is independently testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- LLM features gracefully degrade when Ollama unavailable
