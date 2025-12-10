"""Init command for Story CLI.

Implements the 'story init' command for creating new projects.
"""

from pathlib import Path
from typing import Optional

import typer
from pydantic import ValidationError

from story_cli.models.exceptions import ProjectExistsError
from story_cli.services.project_service import get_project_service
from story_cli.utils.display import (
    console,
    print_error,
    print_success,
    print_panel,
    prompt_input,
)
from story_cli.utils.validation import is_valid_project_name


def init_project(
    name: Optional[str] = typer.Argument(
        None,
        help="Project name (will prompt if not provided)",
    ),
    genre: Optional[str] = typer.Option(
        None,
        "--genre",
        "-g",
        help="Story genre (e.g., romance, mystery, fantasy)",
    ),
    synopsis: Optional[str] = typer.Option(
        None,
        "--synopsis",
        "-s",
        help="Brief story synopsis",
    ),
    path: Optional[Path] = typer.Option(
        None,
        "--path",
        "-p",
        help="Parent directory for project (default: current directory)",
    ),
) -> None:
    """Initialize a new story project.

    Creates a project directory with the following structure:
        <name>/
        ├── story.json
        └── story_data/
            ├── characters_index.json
            └── characters/

    If name, genre, or synopsis are not provided, you will be prompted.
    """
    # Get project name
    if not name:
        console.print("\n[bold]Create New Story Project[/bold]\n")
        name = _prompt_project_name()

    # Validate name if provided directly
    if not is_valid_project_name(name):
        print_error(
            "Invalid project name. Use only letters, numbers, spaces, "
            "hyphens, and underscores."
        )
        raise typer.Exit(1)

    # Check for duplicate before prompting for more info
    project_service = get_project_service()
    parent_dir = path or Path.cwd()

    from story_cli.utils.validation import sanitize_for_filesystem
    project_path = parent_dir / sanitize_for_filesystem(name)

    if project_path.exists():
        print_error(f"Project already exists: {project_path}")
        raise typer.Exit(1)

    # Get genre
    if not genre:
        genre = _prompt_genre()

    # Get synopsis
    if not synopsis:
        synopsis = _prompt_synopsis()

    # Create the project
    try:
        created_path = project_service.create_project(
            name=name,
            genre=genre,
            synopsis=synopsis,
            parent_dir=parent_dir,
        )

        # Show success message
        _display_success(name, genre, synopsis, created_path)

    except ProjectExistsError as e:
        print_error(str(e))
        raise typer.Exit(1)
    except ValidationError as e:
        print_error("Invalid project data:")
        for error in e.errors():
            field = ".".join(str(loc) for loc in error["loc"])
            print_error(f"  {field}: {error['msg']}")
        raise typer.Exit(1)
    except Exception as e:
        print_error(f"Failed to create project: {e}")
        raise typer.Exit(1)


def _prompt_project_name() -> str:
    """Prompt for and validate project name."""
    while True:
        name = prompt_input("[cyan]Project name[/cyan]")
        if not name.strip():
            print_error("Project name cannot be empty")
            continue
        if is_valid_project_name(name):
            return name.strip()
        print_error(
            "Invalid name. Use only letters, numbers, spaces, "
            "hyphens, and underscores."
        )


def _prompt_genre() -> str:
    """Prompt for story genre."""
    console.print("\n[dim]Examples: romance, mystery, fantasy, sci-fi, horror, drama[/dim]")
    while True:
        genre = prompt_input("[cyan]Genre[/cyan]")
        if genre.strip():
            return genre.strip()
        print_error("Genre cannot be empty")


def _prompt_synopsis() -> str:
    """Prompt for story synopsis."""
    console.print("\n[dim]Briefly describe your story (1-3 sentences)[/dim]")
    while True:
        synopsis = prompt_input("[cyan]Synopsis[/cyan]")
        if synopsis.strip():
            return synopsis.strip()
        print_error("Synopsis cannot be empty")


def _display_success(name: str, genre: str, synopsis: str, path: Path) -> None:
    """Display project creation success message."""
    console.print()
    print_success(f"Created project: [bold]{name}[/bold]")
    console.print()

    # Show project summary in a panel
    summary = f"""[dim]Genre:[/dim] {genre}
[dim]Synopsis:[/dim] {synopsis}
[dim]Location:[/dim] {path}"""

    print_panel(summary, f"Project: {name}", style="green")

    console.print()
    console.print("[dim]Next steps:[/dim]")
    console.print(f"  [cyan]cd {path.name}[/cyan]")
    console.print("  [cyan]story new character[/cyan]  - Create your first character")
    console.print("  [cyan]story chat[/cyan]          - Brainstorm with AI")
    console.print()
