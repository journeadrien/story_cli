"""Chat command for Story CLI.

Implements the 'story chat' command for interactive LLM conversations.
"""

import asyncio
from pathlib import Path

import typer
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel

from story_cli.models.exceptions import LLMUnavailableError
from story_cli.services.llm_service import get_llm_service
from story_cli.services.project_service import get_project_service
from story_cli.utils.display import (
    console,
    print_error,
    print_info,
    print_warning,
)


def _get_project_context() -> str | None:
    """Get project context if in a valid project directory."""
    try:
        project_service = get_project_service()
        project_path = Path.cwd()

        is_valid, _ = project_service.validate_project(project_path)
        if not is_valid:
            return None

        project = project_service.open_project(project_path)
        return f"Project: {project.name}\nGenre: {project.genre}\nSynopsis: {project.synopsis}"
    except Exception:
        return None


async def _chat_loop(context: str | None) -> None:
    """Run the interactive chat loop."""
    llm_service = get_llm_service()

    # Check LLM availability
    console.print("[dim]Checking LLM connection...[/dim]")
    if not await llm_service.is_available():
        print_error("LLM is not available.")
        print_info(f"Make sure Ollama is running at: {llm_service.config.host}")
        print_info("Start Ollama with: ollama serve")
        raise typer.Exit(1)

    console.print("[green]Connected to LLM[/green]\n")

    if context:
        console.print("[dim]Project context loaded.[/dim]")

    console.print("[dim]Commands: 'exit' or 'quit' to leave, 'clear' to reset[/dim]")
    console.print()

    while True:
        try:
            # Get user input
            user_input = console.input("[bold cyan]You:[/bold cyan] ").strip()

            if not user_input:
                continue

            # Check for commands
            if user_input.lower() in ("exit", "quit", "q"):
                console.print("\n[dim]Goodbye![/dim]")
                break

            if user_input.lower() == "clear":
                console.clear()
                console.print("[dim]Chat cleared. Context retained.[/dim]\n")
                continue

            # Stream response
            console.print()
            response_text = ""

            with Live(console=console, refresh_per_second=10) as live:
                try:
                    async for chunk in llm_service.chat_stream(user_input, context):
                        response_text += chunk
                        # Render as markdown for nice formatting
                        live.update(
                            Panel(
                                Markdown(response_text),
                                title="[bold green]Assistant[/bold green]",
                                border_style="green",
                            )
                        )
                except LLMUnavailableError:
                    print_error("Lost connection to LLM.")
                    print_info("Attempting to reconnect...")
                    llm_service.reset_availability_cache()
                    if not await llm_service.is_available():
                        print_error("Could not reconnect. Exiting chat.")
                        break
                    continue

            console.print()

        except KeyboardInterrupt:
            console.print("\n\n[dim]Use 'exit' to quit, or continue chatting.[/dim]\n")
            continue
        except EOFError:
            console.print("\n[dim]Goodbye![/dim]")
            break


def chat() -> None:
    """Start an interactive chat session with the LLM.

    Chat with the AI assistant for brainstorming story ideas,
    character development, plot suggestions, and more.

    If run from within a project directory, the project context
    (name, genre, synopsis) will be included automatically.

    Commands during chat:
    - exit/quit: End the chat session
    - clear: Clear the screen (keeps context)
    """
    console.print("\n[bold]Story Chat[/bold]")
    console.print("[dim]Interactive AI assistant for story development[/dim]\n")

    # Get project context if available
    context = _get_project_context()

    if context:
        print_info("Project context detected and loaded.")
    else:
        print_warning("No project context (not in a project directory).")
        print_info("Chat will work, but without project-specific context.")

    console.print()

    # Run the async chat loop
    try:
        asyncio.run(_chat_loop(context))
    except typer.Exit:
        raise
    except Exception as e:
        print_error(f"Chat error: {e}")
        raise typer.Exit(1)
