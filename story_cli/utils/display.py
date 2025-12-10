"""Rich formatting helpers for Story CLI.

Provides consistent terminal UI components using Rich library.
"""

from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

# Custom theme for Story CLI
STORY_THEME = Theme(
    {
        "info": "cyan",
        "success": "green",
        "warning": "yellow",
        "error": "red bold",
        "highlight": "magenta",
        "dim": "dim white",
        "character_name": "bold cyan",
        "role": "green",
        "phase": "yellow bold",
    }
)

# Global console instance with custom theme
console = Console(theme=STORY_THEME)


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[success]✓[/success] {message}")


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[error]✗[/error] {message}")


def print_warning(message: str) -> None:
    """Print a warning message."""
    console.print(f"[warning]⚠[/warning] {message}")


def print_info(message: str) -> None:
    """Print an info message."""
    console.print(f"[info]ℹ[/info] {message}")


def print_panel(content: str, title: str, style: str = "cyan") -> None:
    """Print content in a styled panel.

    Args:
        content: The content to display
        title: Panel title
        style: Border style color
    """
    console.print(Panel(content, title=title, border_style=style))


def create_table(title: str, columns: list[tuple[str, str]]) -> Table:
    """Create a styled table.

    Args:
        title: Table title
        columns: List of (name, style) tuples for columns

    Returns:
        Configured Rich Table instance
    """
    table = Table(title=title, show_header=True, header_style="bold")
    for name, style in columns:
        table.add_column(name, style=style)
    return table


def create_progress() -> Progress:
    """Create a styled progress indicator.

    Returns:
        Configured Rich Progress instance
    """
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    )


def format_character_summary(character: dict[str, Any]) -> str:
    """Format a character summary for display.

    Args:
        character: Character data dictionary

    Returns:
        Formatted string for display
    """
    basics = character.get("basics", {})
    name = basics.get("name", "Unknown")
    role = basics.get("role", "unknown")
    age = basics.get("age")

    lines = [
        f"[character_name]{name}[/character_name]",
        f"  Role: [role]{role}[/role]",
    ]
    if age:
        lines.append(f"  Age: {age}")

    return "\n".join(lines)


def format_project_summary(
    name: str,
    genre: str,
    character_count: int,
    last_modified: str,
) -> Panel:
    """Format a project summary panel.

    Args:
        name: Project name
        genre: Project genre
        character_count: Number of characters
        last_modified: Last modified timestamp

    Returns:
        Formatted Rich Panel
    """
    content = Text()
    content.append("Genre: ", style="dim")
    content.append(f"{genre}\n", style="highlight")
    content.append("Characters: ", style="dim")
    content.append(f"{character_count}\n", style="info")
    content.append("Last modified: ", style="dim")
    content.append(last_modified, style="dim")

    return Panel(content, title=f"[bold]{name}[/bold]", border_style="cyan")


def wizard_phase_header(phase_name: str, current: int, total: int) -> None:
    """Display a wizard phase header with progress.

    Args:
        phase_name: Name of the current phase
        current: Current phase number (1-indexed)
        total: Total number of phases
    """
    progress_bar = "●" * current + "○" * (total - current)
    console.print()
    console.print(f"[phase]Phase {current}/{total}: {phase_name}[/phase]")
    console.print(f"[dim]{progress_bar}[/dim]")
    console.print()


def confirm_action(message: str) -> bool:
    """Prompt user for confirmation.

    Args:
        message: Confirmation message to display

    Returns:
        True if confirmed, False otherwise
    """
    from rich.prompt import Confirm

    return Confirm.ask(message)


def prompt_input(message: str, default: str | None = None) -> str:
    """Prompt user for text input.

    Args:
        message: Prompt message
        default: Default value if user presses Enter

    Returns:
        User input string
    """
    from rich.prompt import Prompt

    return Prompt.ask(message, default=default or "")


def prompt_choice(message: str, choices: list[str], default: str | None = None) -> str:
    """Prompt user to select from choices.

    Args:
        message: Prompt message
        choices: List of valid choices
        default: Default choice

    Returns:
        Selected choice
    """
    from rich.prompt import Prompt

    return Prompt.ask(message, choices=choices, default=default)
