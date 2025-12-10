# Quickstart: Story CLI Markdown Guide

**Feature**: 002-docs-html-guide
**Date**: 2025-12-10

## Overview

This quickstart validates the documentation feature by testing user scenarios from the spec.

## Prerequisites

- Story CLI installed (`pip install -e .`)
- Ollama running (for AI feature verification)
- Git repository with docs/ folder created

## Validation Scenarios

### Scenario 1: View Installation Guide (User Story 1)

**Test**: A new user follows the installation guide

```bash
# 1. Navigate to docs folder on GitHub or locally
ls docs/

# Expected output:
# README.md
# installation.md
# llm-setup.md
# story-guide.md
# character-guide.md

# 2. Read installation guide
cat docs/installation.md | head -50

# 3. Follow steps and verify
story --version

# Expected: Story CLI version X.Y.Z
```

**Pass Criteria**:
- [ ] docs/README.md links to installation.md
- [ ] installation.md has clear step-by-step instructions
- [ ] `story --version` works after following guide

---

### Scenario 2: Set Up LLM Server (User Story 2)

**Test**: A user follows the LLM setup guide

```bash
# 1. Read LLM setup guide
cat docs/llm-setup.md | head -80

# 2. Verify Ollama after following guide
ollama list

# 3. Test AI features
story chat
# Type: "Hello" then "exit"
```

**Pass Criteria**:
- [ ] llm-setup.md explains what Ollama is
- [ ] Environment variables documented (STORY_OLLAMA_HOST, STORY_MODEL)
- [ ] Offline mode explained (what works without LLM)
- [ ] `story chat` responds with AI-generated content

---

### Scenario 3: Learn Story Project Management (User Story 3)

**Test**: A user follows the story guide to create and open a project

```bash
# 1. Read story guide
cat docs/story-guide.md | head -60

# 2. Create project following guide
story init test-novel
# Follow prompts: name, genre, synopsis

# 3. Open project following guide
cd test-novel
story open

# Expected: Project summary displayed
```

**Pass Criteria**:
- [ ] story-guide.md shows `story init` command
- [ ] story-guide.md shows `story open` command
- [ ] `story chat` has 🤖 AI Feature callout

---

### Scenario 4: Learn Character Management (User Story 4)

**Test**: A user follows the character guide for full CRUD

```bash
# 1. Read character guide
cat docs/character-guide.md | head -100

# 2. Create character following wizard section
cd test-novel
story new character
# Follow 5-phase wizard

# 3. List characters
story list characters

# 4. Edit character
story edit character "Character Name"

# 5. Delete character
story delete character "Character Name" --force
```

**Pass Criteria**:
- [ ] character-guide.md documents all 5 wizard phases
- [ ] Each AI-assisted phase has 🤖 callout
- [ ] Edit/list/delete commands documented with examples

---

### Scenario 5: Navigate Documentation (User Story 5)

**Test**: A user can navigate between all guides

```bash
# 1. Check index has all links
grep -E "^\|.*\[.*\]\(.*\.md\)" docs/README.md

# 2. Check each guide links back to index
for f in docs/*.md; do
  echo "=== $f ==="
  grep -i "readme\|index\|documentation" "$f" | head -2
done

# 3. Verify no broken links (manual: click all links on GitHub)
```

**Pass Criteria**:
- [ ] docs/README.md has table of contents with all guides
- [ ] Each guide has navigation link back to index
- [ ] All relative links render correctly on GitHub

---

## AI Feature Callout Verification

Check each guide for proper AI callouts:

```bash
# Find all AI callouts
grep -r "🤖" docs/

# Expected callouts:
# - story-guide.md: story chat feature
# - character-guide.md: name suggestions (Phase 1)
# - character-guide.md: appearance expansion (Phase 2)
# - character-guide.md: trait suggestions (Phase 3)
# - character-guide.md: backstory questions (Phase 4)
```

---

## Success Criteria Checklist

From spec.md:

- [ ] **SC-001**: New user can run `story --help` in under 10 minutes following docs
- [ ] **SC-002**: User can set up Ollama and verify AI in under 15 minutes
- [ ] **SC-003**: Documentation covers 100% of Story CLI commands
- [ ] **SC-004**: Each AI-assisted feature has clear 🤖 callout
- [ ] **SC-005**: All Markdown files render correctly on GitHub
- [ ] **SC-006**: All Markdown files readable locally

---

## Cleanup

```bash
# Remove test project
cd ..
rm -rf test-novel
```
