# Story Management Guide

This guide covers creating and managing story projects in Story CLI.

## Creating a Project

Use `story init` to create a new story project:

```bash
story init my-visual-novel
```

The wizard will prompt you for:

1. **Project name**: A name for your story (used for the folder)
2. **Genre**: The genre of your visual novel (e.g., romance, mystery, fantasy)
3. **Synopsis**: A brief description of your story

Example session:

```text
$ story init my-visual-novel

✨ Creating new story project: my-visual-novel

Project name: my-visual-novel
Genre: Romance
Synopsis: A story about two childhood friends who reunite after years apart.

✨ Created new story project: my-visual-novel
   Location: /Users/you/projects/my-visual-novel
```

## Project Structure

After initialization, your project folder contains:

```text
my-visual-novel/
├── story.json           # Project metadata (name, genre, synopsis)
└── story_data/
    └── characters/      # Character JSON files
        └── index.json   # Character index for quick lookup
```

### story.json

The main project file contains your story's metadata:

```json
{
  "name": "my-visual-novel",
  "genre": "Romance",
  "synopsis": "A story about two childhood friends who reunite after years apart.",
  "created_at": "2025-01-15T10:30:00",
  "updated_at": "2025-01-15T10:30:00"
}
```

## Opening a Project

Use `story open` to open an existing project:

```bash
# Open project in current directory
cd my-visual-novel
story open

# Or specify a path
story open /path/to/my-visual-novel
```

This displays a project summary:

```text
📖 Story Project: my-visual-novel

Genre: Romance
Synopsis: A story about two childhood friends who reunite after years apart.

📊 Statistics:
   Characters: 3
   Last modified: 2025-01-15 14:30

Use 'story list characters' to see all characters.
```

## AI Chat

> 🤖 **AI Feature**: The chat command provides interactive brainstorming with the LLM.

Use `story chat` to start a conversation with the AI assistant:

```bash
story chat
```

The AI can help you:

- Brainstorm plot ideas
- Develop character concepts
- Explore story themes
- Work through writer's block
- Generate scene descriptions

Example session:

```text
$ story chat

Story Chat
Interactive AI assistant for story development

Project context detected and loaded.
Commands: 'exit' or 'quit' to leave, 'clear' to reset

You: I need ideas for a plot twist in my romance story
Assistant: Here are some plot twist ideas for your romance story...
```

**Note**: `story chat` requires Ollama to be running. See [LLM Setup](./llm-setup.md) if you haven't configured it yet.

## Next Steps

Now that you have a project set up:

1. **[Create characters](./character-guide.md)** using the AI-powered wizard
2. Use `story chat` to brainstorm ideas for your story

---

[Back to Documentation Index](./README.md)