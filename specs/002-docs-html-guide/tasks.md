# Tasks: Story CLI Markdown Guide

**Input**: Design documents from `/specs/002-docs-html-guide/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Not required - documentation-only feature. Validation is manual (links, rendering).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each documentation section.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

Based on plan.md structure:
- Documentation: `docs/` at repository root
- All files are Markdown (`.md`)

---

## Phase 1: Setup (Documentation Structure)

**Purpose**: Create documentation folder and index file

- [x] T001 Create docs/ directory at repository root
- [x] T002 Create docs/README.md with title, overview, and table of contents structure per data-model.md

**Checkpoint**: `docs/` folder exists with README.md skeleton

---

## Phase 2: Foundational (Index & Navigation)

**Purpose**: Complete the index file that all user stories link back to

**⚠️ CRITICAL**: Index must be complete before individual guides, as all guides link back to it

- [x] T003 Add Quick Links table to docs/README.md with links to all 4 guides
- [x] T004 Add Prerequisites section to docs/README.md linking to installation guide
- [x] T005 Add Getting Started section to docs/README.md with learning path

**Checkpoint**: docs/README.md is a complete navigation hub for all documentation

---

## Phase 3: User Story 1 - View Installation Guide (Priority: P1) 🎯 MVP

**Goal**: Enable new users to install Story CLI by following clear instructions

**Independent Test**: Follow installation.md on a fresh system, verify `story --version` works

### Implementation for User Story 1

- [x] T006 [US1] Create docs/installation.md with title and introduction
- [x] T007 [US1] Add Prerequisites section to docs/installation.md (Python 3.11+, pip)
- [x] T008 [US1] Add Installation section to docs/installation.md with pip install command and code block
- [x] T009 [US1] Add Verification section to docs/installation.md with `story --version` and `story --help` examples
- [x] T010 [US1] Add Troubleshooting section to docs/installation.md (common issues)
- [x] T011 [US1] Add Next Steps section to docs/installation.md linking to llm-setup.md
- [x] T012 [US1] Add navigation footer to docs/installation.md linking back to README.md

**Checkpoint**: A user can follow docs/installation.md and successfully run `story --help`

---

## Phase 4: User Story 2 - Set Up Local LLM Server (Priority: P1)

**Goal**: Enable users to configure Ollama for AI-assisted features

**Independent Test**: Follow llm-setup.md, verify `ollama list` works and `story chat` responds

### Implementation for User Story 2

- [x] T013 [US2] Create docs/llm-setup.md with title and introduction explaining Ollama
- [x] T014 [US2] Add What is Ollama section to docs/llm-setup.md explaining local LLM concept
- [x] T015 [US2] Add Installation section to docs/llm-setup.md with platform-specific commands (macOS, Linux, Windows)
- [x] T016 [US2] Add Model Download section to docs/llm-setup.md with `ollama pull` command
- [x] T017 [US2] Add Configuration section to docs/llm-setup.md with environment variables table (STORY_OLLAMA_HOST, STORY_MODEL)
- [x] T018 [US2] Add Verification section to docs/llm-setup.md with `ollama list` and `story chat` test
- [x] T019 [US2] Add Offline Mode section to docs/llm-setup.md explaining which features work without LLM
- [x] T020 [US2] Add Troubleshooting section to docs/llm-setup.md (connection issues, model not found)
- [x] T021 [US2] Add navigation footer to docs/llm-setup.md linking to README.md and story-guide.md

**Checkpoint**: A user can follow docs/llm-setup.md and have working AI features in Story CLI

---

## Phase 5: User Story 3 - Learn Story Project Management (Priority: P2)

**Goal**: Enable users to create and manage story projects

**Independent Test**: Follow story-guide.md to create project with `story init` and open with `story open`

### Implementation for User Story 3

- [x] T022 [US3] Create docs/story-guide.md with title and introduction
- [x] T023 [US3] Add Creating a Project section to docs/story-guide.md with `story init` command and example
- [x] T024 [US3] Add Project Structure section to docs/story-guide.md explaining folder layout (story.json, story_data/)
- [x] T025 [US3] Add Opening a Project section to docs/story-guide.md with `story open` command and example
- [x] T026 [US3] Add AI Chat section to docs/story-guide.md with `story chat` command and 🤖 AI Feature callout
- [x] T027 [US3] Add Next Steps section to docs/story-guide.md linking to character-guide.md
- [x] T028 [US3] Add navigation footer to docs/story-guide.md linking to README.md

**Checkpoint**: A user can follow docs/story-guide.md to create and open a story project

---

## Phase 6: User Story 4 - Learn Character Management (Priority: P2)

**Goal**: Enable users to create and manage characters with AI assistance

**Independent Test**: Follow character-guide.md to create, list, edit, and delete a character

### Implementation for User Story 4

- [x] T029 [US4] Create docs/character-guide.md with title and introduction
- [x] T030 [US4] Add Overview section to docs/character-guide.md explaining character system
- [x] T031 [US4] Add Creating a Character section header with `story new character` command
- [x] T032 [US4] Add Phase 1: Basics subsection to docs/character-guide.md with 🤖 AI Feature callout for name suggestions
- [x] T033 [US4] Add Phase 2: Appearance subsection to docs/character-guide.md with 🤖 AI Feature callout for appearance expansion
- [x] T034 [US4] Add Phase 3: Personality subsection to docs/character-guide.md with 🤖 AI Feature callout for trait suggestions
- [x] T035 [US4] Add Phase 4: Backstory subsection to docs/character-guide.md with 🤖 AI Feature callout for backstory questions
- [x] T036 [US4] Add Phase 5: Relationships subsection to docs/character-guide.md
- [x] T037 [US4] Add Editing Characters section to docs/character-guide.md with `story edit character` command and --phase flag
- [x] T038 [US4] Add Listing Characters section to docs/character-guide.md with `story list characters` and flags (--detailed, --json, --role)
- [x] T039 [US4] Add Deleting Characters section to docs/character-guide.md with `story delete character` and dependency warnings
- [x] T040 [US4] Add navigation footer to docs/character-guide.md linking to README.md

**Checkpoint**: A user can follow docs/character-guide.md for complete character CRUD operations

---

## Phase 7: User Story 5 - Navigate Documentation (Priority: P3)

**Goal**: Enable users to easily find information across all documentation

**Independent Test**: Verify all links in docs/README.md work, all guides link back to index

### Implementation for User Story 5

- [x] T041 [US5] Review and verify all internal links in docs/README.md work correctly
- [x] T042 [US5] Review and verify navigation footers in all guide files link correctly
- [x] T043 [US5] Add consistent "Back to Documentation Index" link at bottom of each guide
- [x] T044 [US5] Verify table of contents in README.md matches actual guide titles

**Checkpoint**: All documentation navigation works both on GitHub and locally

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final quality checks and consistency

- [x] T045 [P] Verify all code blocks have language specifiers (bash, text, etc.)
- [x] T046 [P] Verify all 🤖 AI Feature callouts use consistent format per research.md
- [x] T047 [P] Verify command examples match actual CLI (run `story --help` to confirm)
- [x] T048 Run quickstart.md validation scenarios
- [ ] T049 Test documentation renders correctly on GitHub (push and view)
- [x] T050 Verify all files are readable in a plain text editor

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - MVP target
- **User Story 2 (Phase 4)**: Depends on Foundational - Can parallel with US1
- **User Story 3 (Phase 5)**: Depends on Foundational - Can parallel with US1/US2
- **User Story 4 (Phase 6)**: Depends on Foundational - Can parallel with US1/US2/US3
- **User Story 5 (Phase 7)**: Depends on ALL guides being complete (US1-US4)
- **Polish (Phase 8)**: Depends on all user stories complete

### User Story Dependencies

```
Phase 1: Setup
    │
    ▼
Phase 2: Foundational (docs/README.md complete)
    │
    ├────────────┬────────────┬────────────┐
    │            │            │            │
    ▼            ▼            ▼            ▼
Phase 3:     Phase 4:     Phase 5:     Phase 6:
US1          US2          US3          US4
(install)    (llm-setup)  (story)      (character)
    │            │            │            │
    └────────────┴────────────┴────────────┘
                       │
                       ▼
                 Phase 7: US5 (navigation verification)
                       │
                       ▼
                 Phase 8: Polish
```

### Within Each User Story

1. Create file with title/intro first
2. Add content sections in order
3. Add navigation footer last
4. All tasks within a guide are sequential (same file)

### Parallel Opportunities

**Phase 3-6 can all run in parallel** since each creates a different file:
- docs/installation.md (US1)
- docs/llm-setup.md (US2)
- docs/story-guide.md (US3)
- docs/character-guide.md (US4)

**Phase 8 polish tasks marked [P] can run in parallel**

---

## Parallel Example: All Guides

```bash
# After Foundational phase, launch all guide creation in parallel:
Task: "Create docs/installation.md with title and introduction" [US1]
Task: "Create docs/llm-setup.md with title and introduction" [US2]
Task: "Create docs/story-guide.md with title and introduction" [US3]
Task: "Create docs/character-guide.md with title and introduction" [US4]
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2)

1. Complete Phase 1: Setup (1 task)
2. Complete Phase 2: Foundational (3 tasks)
3. Complete Phase 3: User Story 1 - Installation Guide (7 tasks)
4. Complete Phase 4: User Story 2 - LLM Setup Guide (9 tasks)
5. **STOP and VALIDATE**: New user can install and configure Story CLI
6. Deploy/push if ready

### Incremental Delivery

Each phase adds independently valuable documentation:
- After Phase 3: Users can install Story CLI
- After Phase 4: Users can set up AI features
- After Phase 5: Users can manage projects
- After Phase 6: Users can create characters
- After Phase 7: Navigation fully validated
- After Phase 8: Production-ready documentation

---

## Summary

| Phase | User Story | Tasks | Parallel |
|-------|------------|-------|----------|
| 1. Setup | - | 2 | 0 |
| 2. Foundational | - | 3 | 0 |
| 3. US1 - Installation | P1 | 7 | 0 |
| 4. US2 - LLM Setup | P1 | 9 | 0 |
| 5. US3 - Story Guide | P2 | 7 | 0 |
| 6. US4 - Character Guide | P2 | 12 | 0 |
| 7. US5 - Navigation | P3 | 4 | 0 |
| 8. Polish | - | 6 | 3 |
| **Total** | | **50** | **3** |

**MVP Scope**: Phases 1-4 (21 tasks) - Installation and LLM setup documentation
**Full Implementation**: All phases (50 tasks)

---

## Notes

- All guide tasks within a story are sequential (same file)
- Different guides (US1-US4) can be written in parallel by different authors
- [P] tasks in Polish phase can run in parallel
- Verify all commands against actual CLI before finalizing
- Push to GitHub to test rendering after each guide is complete
- 🤖 callouts appear in: story-guide.md (chat), character-guide.md (4 wizard phases)
