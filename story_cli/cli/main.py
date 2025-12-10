"""Main CLI application for Story CLI.

Defines the Typer app and registers all command groups.
"""

import typer

from story_cli import __version__
from story_cli.utils.display import console, print_info

# Main application
app = typer.Typer(
    name="story",
    help="Story CLI - AI-Powered Visual Novel Story Builder",
    no_args_is_help=True,
    rich_markup_mode="rich",
)

# Subcommand groups
new_app = typer.Typer(help="Create new entities")
edit_app = typer.Typer(help="Edit existing entities")
list_app = typer.Typer(help="List entities")
delete_app = typer.Typer(help="Delete entities")

app.add_typer(new_app, name="new")
app.add_typer(edit_app, name="edit")
app.add_typer(list_app, name="list")
app.add_typer(delete_app, name="delete")


def version_callback(value: bool) -> None:
    """Display version and exit."""
    if value:
        print_info(f"Story CLI version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit.",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """Story CLI - AI-Powered Visual Novel Story Builder.

    A terminal-based creative writing assistant that helps authors develop
    visual novel stories through structured wizards and iterative planning
    workflows, powered by local LLMs.
    """
    pass


# Import and register command modules
def register_commands() -> None:
    """Register all CLI commands and command groups."""
    # Import here to avoid circular imports
    try:
        from story_cli.cli import init_cmd

        app.command(name="init")(init_cmd.init_project)
    except ImportError:
        pass

    try:
        from story_cli.cli import open_cmd

        app.command(name="open")(open_cmd.open_project)
    except ImportError:
        pass

    try:
        from story_cli.cli import chat_cmd

        app.command(name="chat")(chat_cmd.chat)
    except ImportError:
        pass

    try:
        from story_cli.cli import character_cmd

        # Register character subcommands under their respective groups
        new_app.command(name="character")(character_cmd.new_character)
        edit_app.command(name="character")(character_cmd.edit_character)
        list_app.command(name="characters")(character_cmd.list_characters)
        delete_app.command(name="character")(character_cmd.delete_character)
    except ImportError:
        pass


# Register commands when module is loaded
register_commands()


# Placeholder commands for development
@app.command(name="status", hidden=True)
def status() -> None:
    """Show current project status (development helper)."""
    console.print("[dim]No project currently open.[/dim]")
    console.print("[dim]Use 'story init <name>' to create a new project.[/dim]")
    console.print("[dim]Use 'story open [path]' to open an existing project.[/dim]")


if __name__ == "__main__":
    app()
