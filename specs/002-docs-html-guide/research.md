# Research: Story CLI Markdown Guide

**Feature**: 002-docs-html-guide
**Date**: 2025-12-10

## Research Questions

### 1. GitHub-Flavored Markdown (GFM) Best Practices

**Decision**: Use GitHub-Flavored Markdown with fenced code blocks, tables, and emoji

**Rationale**: GFM is the de-facto standard for README and documentation files on GitHub. It supports:
- Fenced code blocks with syntax highlighting (```python)
- Tables for structured information
- Task lists for checklists
- Emoji shortcodes and Unicode emoji
- Relative links between files

**Alternatives Considered**:
- CommonMark only: Rejected (loses table support and syntax highlighting)
- reStructuredText: Rejected (less readable in raw form, overkill for user guides)

### 2. Documentation File Organization

**Decision**: Flat structure with 5 files in `docs/` folder

**Rationale**:
- Simple navigation (all files visible in one directory listing)
- No nested folders = shorter relative links
- Matches user mental model of "guides" vs "API reference"
- GitHub renders `docs/README.md` when navigating to folder

**Alternatives Considered**:
- Nested folders (docs/guides/, docs/reference/): Rejected (over-engineering for 5 files)
- Single file: Rejected (too long, harder to navigate)
- Root-level files: Rejected (clutters repository root)

### 3. AI Feature Callout Convention

**Decision**: Use 🤖 emoji prefix in blockquotes for AI feature callouts

**Rationale**:
- Visually distinctive and scannable
- Works in both GitHub rendered view and raw Markdown
- Consistent with modern documentation patterns
- Unicode emoji supported across all target platforms

**Format**:
```markdown
> 🤖 **AI Feature**: Description of what the AI does here.
```

**Alternatives Considered**:
- Custom badges/shields: Rejected (requires image hosting or external service)
- Plain text markers: Rejected (less visually distinctive)
- Admonition syntax: Rejected (requires MkDocs or similar processor)

### 4. Code Example Format

**Decision**: Fenced code blocks with shell/output separation

**Rationale**:
- Clear distinction between commands and output
- Syntax highlighting for shell commands
- Copy-paste friendly (exclude output from command blocks)

**Format**:
```markdown
```bash
story init my-novel
```

Output:
```text
✨ Created new story project: my-novel
```
```

**Alternatives Considered**:
- Single block with $ prefix: Rejected (harder to copy-paste)
- Inline code only: Rejected (multiline commands need blocks)

### 5. Internal Link Strategy

**Decision**: Use relative paths with .md extension

**Rationale**:
- Works both on GitHub and locally
- GitHub automatically handles navigation
- No broken links when repository is cloned

**Format**:
```markdown
See the [Installation Guide](./installation.md) for setup instructions.
```

**Alternatives Considered**:
- Absolute URLs: Rejected (breaks local viewing, depends on hosting URL)
- Anchor links only: Rejected (can't link between files)

### 6. Command Documentation Completeness

**Decision**: Document all user-facing commands with examples

**Commands to Document**:
| Command | Guide | AI Features |
|---------|-------|-------------|
| `story init <name>` | story-guide.md | No |
| `story open [path]` | story-guide.md | No |
| `story chat` | story-guide.md | Yes (LLM chat) |
| `story new character` | character-guide.md | Yes (name, appearance, traits, backstory) |
| `story edit character <name>` | character-guide.md | Yes (same as create) |
| `story list characters` | character-guide.md | No |
| `story delete character <name>` | character-guide.md | No |

**Rationale**: SC-003 requires 100% command coverage. Each command needs:
- Syntax with all options/flags
- One or more examples
- Expected output
- AI feature callouts where applicable

### 7. Environment Variable Documentation

**Decision**: Dedicate a section in llm-setup.md for environment variables

**Variables to Document**:
| Variable | Purpose | Default |
|----------|---------|---------|
| `STORY_OLLAMA_HOST` | Ollama server URL | `http://localhost:11434` |
| `STORY_MODEL` | LLM model name | `qwen3:32b` |

**Rationale**: FR-010 requires environment variable documentation. Users may need to:
- Connect to remote Ollama instance
- Use different model (smaller for low-memory systems)

## Implementation Implications

1. **File Creation Order**: Create docs/README.md first (serves as index), then guides in dependency order (installation → llm-setup → story-guide → character-guide)

2. **Content Reuse**: Avoid duplicating command syntax across guides. Reference other guides for prerequisites.

3. **Testing Strategy**: Manual verification on GitHub after push. Check:
   - All relative links work
   - Code blocks render with highlighting
   - Tables display correctly
   - Emoji render properly

4. **Maintenance**: Document update requirements in README.md footer. When new commands are added, character-guide.md or story-guide.md must be updated.
