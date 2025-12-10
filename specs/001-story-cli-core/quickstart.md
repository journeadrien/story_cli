# Quickstart: Story CLI Core

**Feature**: 001-story-cli-core
**Date**: 2025-12-10

## Prerequisites

- Python 3.11+
- Ollama installed and running (for AI features)
- Qwen3-32B model pulled in Ollama (or configure alternative)

## Installation

```bash
# From source (development)
git clone https://github.com/your-org/story-cli.git
cd story-cli
pip install -e ".[dev]"

# Verify installation
story --help
```

## Environment Configuration

```bash
# Optional: Configure Ollama endpoint (default: localhost:11434)
export STORY_OLLAMA_HOST="http://localhost:11434"

# Optional: Configure model (default: qwen3:32b)
export STORY_MODEL="qwen3:32b"
```

## Quick Start

### 1. Create a New Project

```bash
# Initialize a new project
story init my-visual-novel

# You'll be prompted for:
# - Genre (e.g., romance, mystery, fantasy)
# - Synopsis (brief story description)

cd my-visual-novel
```

### 2. Create Your First Character

```bash
# Start the character creation wizard
story new character

# Or pre-fill the name
story new character --name "Alex Chen"
```

The wizard guides you through:
1. **Basics**: Name, age, gender, role
2. **Appearance**: Hair, eyes, build, distinctive features
3. **Personality**: Traits, flaws, speaking style
4. **Backstory**: Summary, key events, secrets
5. **Relationships**: Connections to other characters

### 3. View Your Characters

```bash
# List all characters
story list characters

# Filter by role
story list characters --role protagonist

# Show detailed info
story list characters --detailed

# Export as JSON
story list characters --json
```

### 4. Edit a Character

```bash
# Open character for editing
story edit character "Alex Chen"

# Jump to a specific phase
story edit character "Alex Chen" --phase appearance
```

### 5. Delete a Character

```bash
# Delete (will warn if other characters have relationships)
story delete character "Alex Chen"

# Force delete including relationship cleanup
story delete character "Alex Chen" --force
```

### 6. Interactive Chat

```bash
# Start chat session for brainstorming
story chat

# Type messages to discuss your story
# Type "exit" or press Ctrl+C to end
```

## Project Structure

After creating a project and some characters:

```
my-visual-novel/
├── story.json                    # Project metadata
└── story_data/
    ├── characters_index.json     # Quick lookup index
    └── characters/
        ├── alex_chen/
        │   └── description.json  # Full character data
        └── sarah_miller/
            └── description.json
```

## Working Without LLM

Story CLI works without an LLM running - AI features will be disabled but all core functionality remains:

```bash
# These work without LLM:
story init my-project
story new character          # Manual input only
story edit character "Name"
story list characters
story delete character "Name"

# These require LLM:
# - Name suggestions
# - Appearance expansion from brief description
# - Trait suggestions
# - Backstory expansion
# - Chat functionality
```

## Command Reference

| Command | Description |
|---------|-------------|
| `story init <name>` | Create new project |
| `story open [path]` | Open existing project |
| `story new character` | Create character via wizard |
| `story edit character <name>` | Edit existing character |
| `story list characters` | List all characters |
| `story delete character <name>` | Delete a character |
| `story chat` | Interactive LLM chat |
| `story --help` | Show help |

## Tips

1. **Genre matters**: The genre you choose affects AI suggestions (tone, naming conventions, tropes)

2. **Build relationships incrementally**: Create characters first, then define relationships between them

3. **Use partial saves**: If you quit mid-wizard, you can save partial progress

4. **LoRA triggers**: Character appearance data auto-generates LoRA trigger strings for image generation

5. **JSON export**: Use `--json` flag for scripting and integration with other tools

## Troubleshooting

### "LLM unavailable" message

1. Check Ollama is running: `ollama list`
2. Verify the model is pulled: `ollama pull qwen3:32b`
3. Check STORY_OLLAMA_HOST is correct

### "Project not found" error

1. Make sure you're in a project directory
2. Or specify the path: `story open /path/to/project`

### Character name validation error

Names can only contain:
- Letters (a-z, A-Z)
- Numbers (0-9)
- Spaces, hyphens, underscores, apostrophes

## Next Steps

After creating your characters:

1. Define relationships between them
2. Use `story chat` to brainstorm scenes
3. Export character data for downstream tools

Future versions will add:
- Scene creation and planning
- Location management
- Ren'Py export integration
