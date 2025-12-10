# Research: Story CLI Core Foundation

**Feature**: 001-story-cli-core
**Date**: 2025-12-10

## Overview

This document captures research findings for implementing Story CLI's core foundation and character creation features. All technical choices align with the project constitution.

---

## 1. Typer CLI Framework

### Decision
Use **Typer** as the CLI framework with command groups for organizing subcommands.

### Rationale
- Constitution mandates Typer for CLI
- Native support for command groups (`story init`, `story new character`, etc.)
- Automatic help generation and shell completion
- Type hints for argument validation
- Integrates seamlessly with Rich for enhanced output

### Implementation Pattern

```python
import typer
from rich.console import Console

app = typer.Typer(help="Story CLI - AI-Powered Visual Novel Story Builder")
character_app = typer.Typer(help="Character management commands")
app.add_typer(character_app, name="character")

# Commands: story init, story open, story chat
# Subcommands: story new character, story edit character, story list characters, story delete character
```

### Alternatives Considered
- **Click**: More verbose, less type-hint integration
- **argparse**: Too low-level, no Rich integration
- **Fire**: Auto-generates CLI but less control over UX

---

## 2. Rich Terminal UI

### Decision
Use **Rich** for all terminal output including panels, tables, progress bars, and syntax highlighting.

### Rationale
- Constitution mandates Rich for terminal UI
- Beautiful output with minimal code
- Progress bars for wizard phases
- Tables for character listings
- Panels for character profiles
- Live updates for streaming LLM responses

### Implementation Pattern

```python
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress
from rich.live import Live

console = Console()

# Character display
console.print(Panel(character_summary, title=f"[bold]{character.name}[/bold]"))

# Character list
table = Table(title="Characters")
table.add_column("Name", style="cyan")
table.add_column("Role", style="green")

# LLM streaming with Live
with Live(console=console) as live:
    for chunk in llm_stream:
        live.update(Text(accumulated_text))
```

### Alternatives Considered
- **Textual**: Overkill for wizard-style CLI; better for full TUI apps
- **Blessed/curses**: Too low-level
- **Plain print**: Doesn't meet UX requirements

---

## 3. LangGraph Workflow State Machine

### Decision
Use **LangGraph** for the character creation wizard as a state machine with defined phases.

### Rationale
- Constitution mandates LangGraph for workflow state machines
- Clear state transitions between wizard phases
- Built-in support for checkpointing (partial saves)
- Conditional edges for skip/back navigation
- Native integration with LangChain for LLM calls

### Implementation Pattern

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal

class CharacterWizardState(TypedDict):
    phase: Literal["basics", "appearance", "personality", "backstory", "relationships", "review"]
    character_data: dict
    is_complete: bool

def basics_node(state: CharacterWizardState) -> CharacterWizardState:
    # Collect basics, return updated state
    ...

workflow = StateGraph(CharacterWizardState)
workflow.add_node("basics", basics_node)
workflow.add_node("appearance", appearance_node)
# ... add other nodes
workflow.add_conditional_edges("basics", route_from_basics)
```

### State Machine Design

```
[START] → basics → appearance → personality → backstory → relationships → review → [END]
                ↑                                                              ↓
                ←←←←←←←←←←←←←←←← (edit specific phase) ←←←←←←←←←←←←←←←←←←←←←←
```

### Alternatives Considered
- **Manual state tracking**: Error-prone, hard to maintain
- **FSM libraries (transitions)**: No LLM integration
- **LangChain Agents**: Too autonomous; wizard needs structured phases

---

## 4. langchain-ollama LLM Integration

### Decision
Use **langchain-ollama** for Ollama integration with streaming support and tool calling.

### Rationale
- Constitution mandates langchain-ollama for LLM integration
- Native streaming support for real-time feedback
- Tool/function calling for structured output
- Automatic retry and error handling
- Works with any Ollama model

### Implementation Pattern

```python
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
import os

def get_llm_client():
    return ChatOllama(
        base_url=os.getenv("STORY_OLLAMA_HOST", "http://localhost:11434"),
        model=os.getenv("STORY_MODEL", "qwen3:32b"),
        timeout=10,  # Connection timeout
        streaming=True,
    )

# Streaming usage
async for chunk in llm.astream([SystemMessage(...), HumanMessage(...)]):
    yield chunk.content

# Tool calling for structured output
from langchain_core.tools import tool

@tool
def generate_character_appearance(brief_description: str) -> dict:
    """Generate structured appearance from brief description."""
    ...
```

### Error Handling

```python
from httpx import ConnectError, ConnectTimeout

try:
    response = await llm.ainvoke(messages)
except (ConnectError, ConnectTimeout):
    console.print("[red]LLM unavailable. Continuing without AI assistance.[/red]")
    # Fall back to manual input
```

### Alternatives Considered
- **Direct Ollama API**: More code, less abstraction
- **LiteLLM**: Extra dependency, Ollama support via langchain is native
- **OpenAI SDK**: Cloud-focused, not local-first

---

## 5. Pydantic Data Models

### Decision
Use **Pydantic v2** for all data models with JSON serialization.

### Rationale
- Constitution mandates Pydantic for data models and validation
- Type-safe data structures
- Automatic JSON serialization/deserialization
- Validation with clear error messages
- IDE support with type hints

### Implementation Pattern

```python
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum

class CharacterRole(str, Enum):
    PROTAGONIST = "protagonist"
    LOVE_INTEREST = "love_interest"
    ANTAGONIST = "antagonist"
    SUPPORTING = "supporting"
    BACKGROUND = "background"

class CharacterBasics(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=200)
    gender: Optional[str] = None
    role: CharacterRole = CharacterRole.SUPPORTING

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        # No special characters in name for filesystem safety
        if not v.replace(" ", "").replace("-", "").replace("_", "").isalnum():
            raise ValueError("Name can only contain letters, numbers, spaces, hyphens, and underscores")
        return v

class Character(BaseModel):
    basics: CharacterBasics
    appearance: Optional[CharacterAppearance] = None
    personality: Optional[CharacterPersonality] = None
    backstory: Optional[CharacterBackstory] = None
    relationships: list[Relationship] = Field(default_factory=list)
    lora_trigger: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
```

### JSON Storage Pattern

```python
import json
from pathlib import Path

def save_character(character: Character, project_path: Path) -> None:
    char_dir = project_path / "story_data" / "characters" / character.basics.name.lower().replace(" ", "_")
    char_dir.mkdir(parents=True, exist_ok=True)

    with open(char_dir / "description.json", "w") as f:
        f.write(character.model_dump_json(indent=2))
```

### Alternatives Considered
- **dataclasses**: No built-in validation
- **attrs**: Less JSON serialization support
- **TypedDict**: No validation, just type hints

---

## 6. LoRA Trigger Generation

### Decision
Auto-generate LoRA trigger strings from character appearance attributes.

### Rationale
- Spec requires LoRA triggers for future image generation
- Consistent format enables downstream tool compatibility
- Combines key visual identifiers into a single string

### Implementation Pattern

```python
def generate_lora_trigger(appearance: CharacterAppearance, name: str) -> str:
    """Generate a LoRA trigger string from appearance attributes."""
    parts = [name.lower().replace(" ", "_")]

    if appearance.hair:
        parts.append(f"{appearance.hair.color}_{appearance.hair.style}_hair")
    if appearance.eyes:
        parts.append(f"{appearance.eyes.color}_eyes")
    if appearance.distinctive_features:
        parts.extend([f.lower().replace(" ", "_") for f in appearance.distinctive_features[:2]])

    return ", ".join(parts)

# Example output: "alex_chen, blonde_long_hair, blue_eyes, scar_on_cheek"
```

---

## 7. Character Index Management

### Decision
Auto-rebuild `characters_index.json` on any character modification.

### Rationale
- Spec requires auto-maintained index
- Enables fast lookups without reading all character files
- Supports filtering by role, name search

### Implementation Pattern

```python
def rebuild_character_index(project_path: Path) -> None:
    """Rebuild characters_index.json from all character files."""
    characters_dir = project_path / "story_data" / "characters"
    index = []

    for char_dir in characters_dir.iterdir():
        if char_dir.is_dir():
            desc_file = char_dir / "description.json"
            if desc_file.exists():
                char = Character.model_validate_json(desc_file.read_text())
                index.append({
                    "name": char.basics.name,
                    "role": char.basics.role.value,
                    "age": char.basics.age,
                    "path": str(char_dir.relative_to(project_path)),
                    "updated_at": char.updated_at.isoformat(),
                })

    index_path = project_path / "story_data" / "characters_index.json"
    index_path.write_text(json.dumps(index, indent=2))
```

---

## 8. Project Validation

### Decision
Validate project structure on `story open` and report issues clearly.

### Rationale
- Spec requires validation and error reporting
- Prevents cryptic errors from missing/corrupted files
- Provides summary on successful open

### Implementation Pattern

```python
def validate_project(project_path: Path) -> tuple[bool, list[str]]:
    """Validate project structure, return (is_valid, errors)."""
    errors = []

    story_json = project_path / "story.json"
    if not story_json.exists():
        errors.append("Missing story.json")

    story_data = project_path / "story_data"
    if not story_data.exists():
        errors.append("Missing story_data/ directory")

    characters_dir = story_data / "characters"
    if not characters_dir.exists():
        errors.append("Missing story_data/characters/ directory")

    # Validate story.json schema if exists
    if story_json.exists():
        try:
            Project.model_validate_json(story_json.read_text())
        except ValidationError as e:
            errors.append(f"Invalid story.json: {e}")

    return (len(errors) == 0, errors)
```

---

## 9. Graceful LLM Degradation

### Decision
All LLM-dependent features must have non-AI fallbacks.

### Rationale
- Spec requires system to work when LLM unavailable
- Users should be able to create characters manually
- Clear messaging when AI features unavailable

### Implementation Pattern

```python
class LLMService:
    def __init__(self):
        self._client = None
        self._available = None

    async def is_available(self) -> bool:
        if self._available is None:
            try:
                client = get_llm_client()
                await client.ainvoke([HumanMessage(content="ping")])
                self._available = True
            except Exception:
                self._available = False
        return self._available

    async def suggest_names(self, genre: str, role: str) -> list[str]:
        if not await self.is_available():
            return []  # Empty list signals manual input needed
        # ... LLM call
```

---

## Summary

All technical decisions align with the project constitution. No NEEDS CLARIFICATION items remain. Key patterns established:

1. **CLI**: Typer with command groups
2. **UI**: Rich for all terminal output
3. **Workflows**: LangGraph state machines
4. **LLM**: langchain-ollama with streaming
5. **Data**: Pydantic models with JSON persistence
6. **Graceful degradation**: All AI features have fallbacks

Ready for Phase 1: Data Model and Contracts.
