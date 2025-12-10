"""Open command for Story CLI.

Implements the 'story open' command for opening existing projects.
"""

from pathlib import Path
from typing import Optional

import typer

from story_cli.models.exceptions import ProjectNotFoundError, ProjectValidationError
from story_cli.services.project_service import get_project_service
from story_cli.utils.display import (
    console,
    format_project_summary,
    print_error,
    print_success,
    print_warning,
)


# Simple context manager for tracking current project
_current_project_path: Path | None = None


def get_current_project() -> Path | None:
    """Get the currently open project path."""
    return _current_project_path


def set_current_project(path: Path | None) -> None:
    """Set the currently open project path."""
    global _current_project_path
    _current_project_path = path


def open_project(
    path: Optional[Path] = typer.Argument(
        None,
        help="Path to project directory (default: current directory)",
        exists=False,  # We handle existence check ourselves for better error messages
    ),
) -> None:
    """Open an existing story project.

    Validates the project structure and displays a summary including:
    - Project name and genre
    - Number of characters
    - Last modified timestamp

    If no path is provided, opens the project in the current directory.
    """
    project_service = get_project_service()

    # Use provided path or current directory
    project_path = path or Path.cwd()

    # Resolve to absolute path
    project_path = project_path.resolve()

    # Try to open the project
    try:
        # Validate and load
        is_valid, errors = project_service.validate_project(project_path)

        if not is_valid:
            _display_validation_errors(project_path, errors)
            raise typer.Exit(1)

        # Get project summary
        summary = project_service.get_project_summary(project_path)

        # Set as current project
        set_current_project(project_path)

        # Display success
        _display_project_summary(summary, project_path)

    except typer.Exit:
        # Re-raise Exit exceptions without wrapping
        raise
    except ProjectNotFoundError as e:
        print_error(str(e))
        console.print("\n[dim]To create a new project, use:[/dim]")
        console.print("  [cyan]story init <name>[/cyan]")
        raise typer.Exit(1)
    except ProjectValidationError as e:
        _display_validation_errors(project_path, e.errors)
        raise typer.Exit(1)
    except Exception as e:
        print_error(f"Failed to open project: {e}")
        raise typer.Exit(1)


def _display_validation_errors(path: Path, errors: list[str]) -> None:
    """Display validation errors in a formatted way."""
    print_error(f"Invalid project at: {path}")
    console.print()
    console.print("[dim]Validation errors:[/dim]")
    for error in errors:
        console.print(f"  [error]•[/error] {error}")
    console.print()
    print_warning("The project structure may be corrupted or incomplete.")


def _display_project_summary(summary: dict, path: Path) -> None:
    """Display project summary in a nice format."""
    print_success(f"Opened project: [bold]{summary['name']}[/bold]")
    console.print()

    # Format last modified
    last_modified_str = summary["last_modified"].strftime("%Y-%m-%d %H:%M")

    # Display the summary panel
    panel = format_project_summary(
        name=summary["name"],
        genre=summary["genre"],
        character_count=summary["character_count"],
        last_modified=last_modified_str,
    )
    console.print(panel)

    # Show synopsis
    if summary.get("synopsis"):
        console.print()
        console.print("[dim]Synopsis:[/dim]")
        console.print(f"  {summary['synopsis']}")

    console.print()
    console.print("[dim]Available commands:[/dim]")
    console.print("  [cyan]story list characters[/cyan]  - List all characters")
    console.print("  [cyan]story new character[/cyan]    - Create a new character")
    console.print("  [cyan]story chat[/cyan]             - Brainstorm with AI")
    console.print()
