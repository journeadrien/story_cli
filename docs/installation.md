# Installation Guide

This guide walks you through installing Story CLI on your system.

## Prerequisites

Before installing Story CLI, ensure you have:

- **Python 3.11 or higher**
  - Check your version: `python --version` or `python3 --version`
  - [Download Python](https://www.python.org/downloads/) if needed

- **pip** (Python package manager)
  - Usually included with Python
  - Check with: `pip --version` or `pip3 --version`

## Installation

Install Story CLI using pip:

```bash
pip install story-cli
```

Or install from source (for development):

```bash
git clone https://github.com/anthropics/story-cli.git
cd story-cli
pip install -e .
```

### Virtual Environment (Recommended)

Using a virtual environment keeps Story CLI isolated from other Python projects:

```bash
# Create virtual environment
python -m venv story-env

# Activate it
# On macOS/Linux:
source story-env/bin/activate
# On Windows:
story-env\Scripts\activate

# Install Story CLI
pip install story-cli
```

## Verification

After installation, verify Story CLI is working:

```bash
story --version
```

Expected output:
```text
Story CLI version 0.1.0
```

Check available commands:

```bash
story --help
```

Expected output:
```text
Usage: story [OPTIONS] COMMAND [ARGS]...

  Story CLI - AI-Powered Visual Novel Story Builder.

Options:
  -v, --version  Show version and exit.
  --help         Show this message and exit.

Commands:
  chat    Start an interactive chat session with the LLM.
  delete  Delete entities
  edit    Edit existing entities
  init    Initialize a new story project.
  list    List entities
  new     Create new entities
  open    Open an existing story project.
```

## Troubleshooting

### Command not found: story

If you see "command not found" after installation:

1. **Check PATH**: Ensure pip's installation directory is in your PATH
   ```bash
   python -m story_cli --help
   ```

2. **Reinstall with user flag**:
   ```bash
   pip install --user story-cli
   ```

3. **Use full path**: Find where pip installed it
   ```bash
   pip show story-cli | grep Location
   ```

### Python version too old

Story CLI requires Python 3.11+. If your system Python is older:

1. Install Python 3.11+ from [python.org](https://www.python.org/downloads/)
2. Use `python3.11` explicitly:
   ```bash
   python3.11 -m pip install story-cli
   ```

### Permission denied errors

Try installing with the `--user` flag:

```bash
pip install --user story-cli
```

Or use a virtual environment (recommended).

## Next Steps

Once Story CLI is installed:

1. **[Set up Ollama](./llm-setup.md)** for AI-powered features (recommended)
2. **[Create your first project](./story-guide.md)** to start building your story

---

[Back to Documentation Index](./README.md)
