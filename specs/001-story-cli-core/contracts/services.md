# Service Contracts: Story CLI Core

**Feature**: 001-story-cli-core
**Date**: 2025-12-10

## Overview

This document defines the internal service contracts for Story CLI. Since this is a CLI application (not a web API), contracts are defined as Python service interfaces.

---

## ProjectService

Handles project lifecycle operations.

### Interface

```python
from pathlib import Path
from typing import Optional
from story_cli.models.project import Project

class ProjectService:
    """Service for project management operations."""

    def create_project(
        self,
        name: str,
        genre: str,
        synopsis: str,
        parent_dir: Optional[Path] = None,
    ) -> Path:
        """
        Create a new project with the given metadata.

        Args:
            name: Project name (used as directory name)
            genre: Story genre
            synopsis: Brief story synopsis
            parent_dir: Parent directory for project (defaults to cwd)

        Returns:
            Path to created project directory

        Raises:
            ValueError: If name contains invalid characters
            FileExistsError: If project directory already exists
        """
        ...

    def open_project(self, path: Optional[Path] = None) -> Project:
        """
        Open and validate an existing project.

        Args:
            path: Path to project directory (defaults to cwd)

        Returns:
            Loaded Project model

        Raises:
            FileNotFoundError: If project directory doesn't exist
            ValidationError: If project structure is invalid
        """
        ...

    def validate_project(self, path: Path) -> tuple[bool, list[str]]:
        """
        Validate project structure without loading.

        Args:
            path: Path to project directory

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        ...

    def get_project_summary(self, path: Path) -> dict:
        """
        Get project summary for display.

        Args:
            path: Path to project directory

        Returns:
            Dictionary with:
                - name: str
                - genre: str
                - character_count: int
                - last_modified: datetime
        """
        ...
```

---

## CharacterService

Handles character CRUD operations and index management.

### Interface

```python
from pathlib import Path
from typing import Optional
from story_cli.models.character import Character, CharacterBasics

class CharacterService:
    """Service for character management operations."""

    def __init__(self, project_path: Path):
        """Initialize service with project path."""
        self.project_path = project_path

    def create_character(self, character: Character) -> Path:
        """
        Create a new character.

        Args:
            character: Character model to save

        Returns:
            Path to character directory

        Raises:
            ValueError: If character name already exists
            ValidationError: If character data is invalid
        """
        ...

    def get_character(self, name: str) -> Character:
        """
        Load a character by name.

        Args:
            name: Character name (case-insensitive)

        Returns:
            Loaded Character model

        Raises:
            FileNotFoundError: If character doesn't exist
        """
        ...

    def update_character(self, character: Character) -> None:
        """
        Update an existing character.

        Args:
            character: Updated Character model

        Raises:
            FileNotFoundError: If character doesn't exist
            ValidationError: If character data is invalid
        """
        ...

    def delete_character(self, name: str, force: bool = False) -> list[str]:
        """
        Delete a character.

        Args:
            name: Character name to delete
            force: If True, also remove relationship references

        Returns:
            List of affected characters (those with relationships to deleted)

        Raises:
            FileNotFoundError: If character doesn't exist
            ValueError: If character has relationships and force=False
        """
        ...

    def list_characters(
        self,
        role_filter: Optional[str] = None,
    ) -> list[dict]:
        """
        List all characters with optional filtering.

        Args:
            role_filter: Filter by role (protagonist, antagonist, etc.)

        Returns:
            List of character summary dicts with:
                - name: str
                - role: str
                - age: int | None
                - completion: int (percentage)
        """
        ...

    def character_exists(self, name: str) -> bool:
        """Check if a character exists."""
        ...

    def get_relationship_dependencies(self, name: str) -> list[str]:
        """
        Get names of characters that have relationships to this character.

        Args:
            name: Character name to check

        Returns:
            List of character names with relationships to the given character
        """
        ...

    def rebuild_index(self) -> None:
        """Rebuild the characters_index.json file."""
        ...
```

---

## LLMService

Handles LLM interactions with Ollama.

### Interface

```python
from typing import AsyncIterator, Optional
from story_cli.models.character import CharacterAppearance, CharacterPersonality

class LLMService:
    """Service for LLM-powered content generation."""

    async def is_available(self) -> bool:
        """
        Check if LLM is available.

        Returns:
            True if LLM responds within timeout, False otherwise
        """
        ...

    async def suggest_names(
        self,
        genre: str,
        role: str,
        count: int = 5,
    ) -> list[str]:
        """
        Generate name suggestions based on genre and role.

        Args:
            genre: Story genre
            role: Character role
            count: Number of suggestions

        Returns:
            List of suggested names (empty if LLM unavailable)
        """
        ...

    async def expand_appearance(
        self,
        brief_description: str,
        genre: str,
    ) -> CharacterAppearance:
        """
        Expand a brief description into structured appearance.

        Args:
            brief_description: User's brief description
            genre: Story genre for context

        Returns:
            Structured CharacterAppearance

        Raises:
            LLMUnavailableError: If LLM is not available
        """
        ...

    async def suggest_traits(
        self,
        role: str,
        existing_traits: list[str],
        genre: str,
    ) -> list[str]:
        """
        Suggest personality traits based on role.

        Args:
            role: Character role
            existing_traits: Already chosen traits
            genre: Story genre

        Returns:
            List of suggested traits (empty if LLM unavailable)
        """
        ...

    async def expand_backstory(
        self,
        notes: str,
        character_name: str,
        genre: str,
    ) -> str:
        """
        Expand brief notes into full backstory.

        Args:
            notes: User's brief notes
            character_name: Character's name
            genre: Story genre

        Returns:
            Expanded backstory text

        Raises:
            LLMUnavailableError: If LLM is not available
        """
        ...

    async def generate_backstory_questions(
        self,
        character_name: str,
        role: str,
        genre: str,
    ) -> list[str]:
        """
        Generate questions to help flesh out backstory.

        Args:
            character_name: Character's name
            role: Character role
            genre: Story genre

        Returns:
            List of questions (empty if LLM unavailable)
        """
        ...

    async def check_trait_contradictions(
        self,
        traits: list[str],
    ) -> list[tuple[str, str]]:
        """
        Check for contradictory traits.

        Args:
            traits: List of trait strings

        Returns:
            List of (trait1, trait2) tuples that contradict
        """
        ...

    async def chat_stream(
        self,
        message: str,
        context: Optional[str] = None,
    ) -> AsyncIterator[str]:
        """
        Stream a chat response.

        Args:
            message: User message
            context: Optional project context

        Yields:
            Text chunks as they arrive

        Raises:
            LLMUnavailableError: If LLM is not available
        """
        ...
```

---

## CharacterWizardWorkflow

LangGraph workflow for character creation wizard.

### State Definition

```python
from typing import TypedDict, Literal, Optional
from story_cli.models.character import Character

class CharacterWizardState(TypedDict):
    """State for character creation wizard."""

    # Current phase
    phase: Literal["basics", "appearance", "personality", "backstory", "relationships", "review"]

    # Character data being built
    character: Optional[Character]

    # Project context
    project_path: str
    genre: str

    # Navigation
    previous_phase: Optional[str]
    skip_to_phase: Optional[str]

    # Completion tracking
    phases_completed: list[str]

    # User interaction
    last_user_input: Optional[str]
    ai_suggestions: list[str]

    # Exit state
    should_exit: bool
    save_partial: bool
```

### Workflow Nodes

```python
from langgraph.graph import StateGraph

def create_character_wizard() -> StateGraph:
    """Create the character wizard workflow graph."""

    workflow = StateGraph(CharacterWizardState)

    # Add nodes for each phase
    workflow.add_node("basics", basics_node)
    workflow.add_node("appearance", appearance_node)
    workflow.add_node("personality", personality_node)
    workflow.add_node("backstory", backstory_node)
    workflow.add_node("relationships", relationships_node)
    workflow.add_node("review", review_node)
    workflow.add_node("save", save_node)

    # Add edges
    workflow.add_conditional_edges("basics", route_after_basics)
    workflow.add_conditional_edges("appearance", route_after_appearance)
    workflow.add_conditional_edges("personality", route_after_personality)
    workflow.add_conditional_edges("backstory", route_after_backstory)
    workflow.add_conditional_edges("relationships", route_after_relationships)
    workflow.add_conditional_edges("review", route_after_review)

    workflow.set_entry_point("basics")
    workflow.set_finish_point("save")

    return workflow.compile()
```

### Node Signatures

```python
async def basics_node(state: CharacterWizardState) -> CharacterWizardState:
    """
    Collect basic character information.

    Prompts for:
        - name (required)
        - age (optional)
        - gender (optional)
        - role (required, with selection)

    AI Features:
        - Suggest names based on genre

    Returns:
        Updated state with basics populated
    """
    ...

async def appearance_node(state: CharacterWizardState) -> CharacterWizardState:
    """
    Collect character appearance.

    Prompts for:
        - hair (color, style, length)
        - eyes (color, shape)
        - skin_tone
        - height, build
        - distinctive_features
        - clothing_style
        - accessories

    AI Features:
        - Expand brief description to structured data
        - Generate LoRA trigger on completion

    Returns:
        Updated state with appearance populated
    """
    ...

async def personality_node(state: CharacterWizardState) -> CharacterWizardState:
    """
    Collect personality traits.

    Prompts for:
        - primary_traits (3-5)
        - secondary_traits (2-3)
        - flaws (1-3)
        - speaking_style
        - speech_quirks
        - motivations
        - fears
        - secrets

    AI Features:
        - Suggest traits based on role
        - Check for contradictions

    Returns:
        Updated state with personality populated
    """
    ...

async def backstory_node(state: CharacterWizardState) -> CharacterWizardState:
    """
    Collect character backstory.

    Prompts for:
        - backstory_summary (required)
        - backstory_full (optional)
        - key_events
        - secrets

    AI Features:
        - Expand notes to full backstory
        - Generate questions to flesh out history

    Returns:
        Updated state with backstory populated
    """
    ...

async def relationships_node(state: CharacterWizardState) -> CharacterWizardState:
    """
    Define character relationships.

    Shows:
        - List of existing characters

    Prompts for each relationship:
        - target_character
        - type (family, friend, enemy, etc.)
        - dynamic
        - initial_feeling
        - history
        - tension_points

    Features:
        - Prompt to update other character's relationship (bidirectional)

    Returns:
        Updated state with relationships populated
    """
    ...

async def review_node(state: CharacterWizardState) -> CharacterWizardState:
    """
    Review complete character before saving.

    Displays:
        - Formatted character profile
        - Missing recommended fields highlighted

    Options:
        - Save
        - Edit (go to specific phase)
        - Regenerate (AI rewrites section)
        - Cancel

    Returns:
        Updated state with user's choice
    """
    ...

async def save_node(state: CharacterWizardState) -> CharacterWizardState:
    """
    Save character to disk.

    Actions:
        - Write description.json
        - Update characters_index.json
        - Update related characters' relationships if bidirectional

    Returns:
        Final state with save confirmation
    """
    ...
```

---

## Error Types

```python
class StoryCliError(Exception):
    """Base exception for Story CLI."""
    pass

class ProjectNotFoundError(StoryCliError):
    """Project directory or structure not found."""
    pass

class ProjectValidationError(StoryCliError):
    """Project structure is invalid."""
    pass

class CharacterNotFoundError(StoryCliError):
    """Character does not exist."""
    pass

class CharacterExistsError(StoryCliError):
    """Character with this name already exists."""
    pass

class RelationshipDependencyError(StoryCliError):
    """Cannot delete character with existing relationships."""
    pass

class LLMUnavailableError(StoryCliError):
    """LLM service is not available."""
    pass
```

---

## CLI Command Signatures

```python
import typer
from pathlib import Path
from typing import Optional

app = typer.Typer()

@app.command()
def init(
    name: str = typer.Argument(..., help="Project name"),
    genre: Optional[str] = typer.Option(None, help="Story genre"),
    synopsis: Optional[str] = typer.Option(None, help="Brief synopsis"),
) -> None:
    """Initialize a new story project."""
    ...

@app.command()
def open(
    path: Optional[Path] = typer.Argument(None, help="Project path (default: current directory)"),
) -> None:
    """Open an existing project."""
    ...

@app.command()
def chat() -> None:
    """Start interactive chat session with LLM."""
    ...

# Character subcommands
character_app = typer.Typer()
app.add_typer(character_app, name="new")
app.add_typer(character_app, name="edit")
app.add_typer(character_app, name="list")
app.add_typer(character_app, name="delete")

@character_app.command("character")
def new_character(
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Pre-fill character name"),
) -> None:
    """Create a new character through guided wizard."""
    ...

@character_app.command("character")
def edit_character(
    name: str = typer.Argument(..., help="Character name"),
    phase: Optional[str] = typer.Option(None, "--phase", "-p", help="Go directly to phase"),
) -> None:
    """Edit an existing character."""
    ...

@character_app.command("characters")
def list_characters(
    role: Optional[str] = typer.Option(None, "--role", "-r", help="Filter by role"),
    detailed: bool = typer.Option(False, "--detailed", "-d", help="Show full details"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
) -> None:
    """List all characters in the project."""
    ...

@character_app.command("character")
def delete_character(
    name: str = typer.Argument(..., help="Character name"),
    force: bool = typer.Option(False, "--force", "-f", help="Force delete with dependencies"),
) -> None:
    """Delete a character."""
    ...
```
