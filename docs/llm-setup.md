# LLM Setup Guide

This guide helps you set up Ollama to enable AI-powered features in Story CLI.

## What is Ollama?

[Ollama](https://ollama.ai) is a tool that runs large language models (LLMs) locally on your computer. Story CLI uses Ollama to provide AI assistance for:

- Generating character name suggestions
- Expanding appearance descriptions
- Suggesting personality traits
- Developing backstory through guided questions
- Interactive brainstorming via chat

**Why local?** Your story data stays on your machine. No cloud services, no API keys, no usage fees.

## Installation

### macOS

```bash
# Using Homebrew
brew install ollama

# Or download from ollama.ai
curl -fsSL https://ollama.ai/install.sh | sh
```

### Linux

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Windows

Download the installer from [ollama.ai/download](https://ollama.ai/download) and run it.

## Model Download

After installing Ollama, download a language model. Story CLI works best with **Qwen3** (recommended) or similar models:

```bash
# Start Ollama service (if not already running)
ollama serve

# In another terminal, pull the recommended model
ollama pull qwen3:32b
```

For systems with limited memory, use a smaller model:

```bash
# 8GB RAM systems
ollama pull qwen3:8b

# 4GB RAM systems
ollama pull qwen3:4b
```

## Configuration

Story CLI uses environment variables for LLM configuration:

| Variable | Description | Default |
|----------|-------------|---------|
| `STORY_OLLAMA_HOST` | Ollama server URL | `http://localhost:11434` |
| `STORY_MODEL` | Model to use for AI features | `qwen3:32b` |

### Setting Environment Variables

**macOS/Linux** (add to `~/.bashrc` or `~/.zshrc`):

```bash
export STORY_OLLAMA_HOST="http://localhost:11434"
export STORY_MODEL="qwen3:32b"
```

**Windows** (PowerShell):

```powershell
$env:STORY_OLLAMA_HOST = "http://localhost:11434"
$env:STORY_MODEL = "qwen3:32b"
```

### Remote Ollama Server

If Ollama runs on a different machine:

```bash
export STORY_OLLAMA_HOST="http://192.168.1.100:11434"
```

## Verification

1. **Check Ollama is running**:

```bash
ollama list
```

Expected output:
```text
NAME           SIZE     MODIFIED
qwen3:32b      18 GB    2 minutes ago
```

2. **Test Story CLI AI features**:

```bash
story chat
```

Type a message and verify you get an AI response:

```text
You: Hello, can you help me brainstorm a story?
Assistant: Of course! I'd love to help you brainstorm...
```

Type `exit` to leave the chat.

## Offline Mode

Story CLI works without Ollama, but AI features will be unavailable:

| Feature | Without Ollama |
|---------|---------------|
| `story init` | Works |
| `story open` | Works |
| `story new character` | Works (no AI suggestions) |
| `story edit character` | Works (no AI suggestions) |
| `story list characters` | Works |
| `story delete character` | Works |
| `story chat` | Does not work |

When Ollama is unavailable, you'll see a message like:

```text
LLM is not available.
Make sure Ollama is running at: http://localhost:11434
Start Ollama with: ollama serve
```

You can still create characters manually—the wizard will skip AI suggestion steps.

## Troubleshooting

### "Connection refused" error

Ollama isn't running. Start it:

```bash
ollama serve
```

### "Model not found" error

The model hasn't been downloaded:

```bash
ollama pull qwen3:32b
```

Or check which models are installed:

```bash
ollama list
```

### Slow responses

Large models require significant RAM. Try a smaller model:

```bash
export STORY_MODEL="qwen3:8b"
```

### Wrong model being used

Check your environment variable:

```bash
echo $STORY_MODEL
```

Set it to your preferred model:

```bash
export STORY_MODEL="qwen3:32b"
```

## Next Steps

With Ollama configured, you're ready to:

1. **[Create a story project](./story-guide.md)** and start brainstorming
2. **[Create characters](./character-guide.md)** with AI-powered suggestions

---

[Back to Documentation Index](./README.md)