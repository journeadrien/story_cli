"""Character commands for Story CLI.

Implements character CRUD operations: new, edit, list, delete.
"""

import asyncio
from pathlib import Path
from typing import Optional

import typer
from rich.prompt import Confirm, Prompt
from rich.table import Table

from story_cli.models.character import (
    Character,
    CharacterAppearance,
    CharacterBackstory,
    CharacterBasics,
    CharacterPersonality,
    EyeDescription,
    HairDescription,
)
from story_cli.models.enums import CharacterRole
from story_cli.models.exceptions import (
    CharacterExistsError,
    CharacterNotFoundError,
    ProjectNotFoundError,
    RelationshipDependencyError,
)
from story_cli.services.character_service import get_character_service
from story_cli.services.llm_service import get_llm_service
from story_cli.services.project_service import get_project_service
from story_cli.utils.display import (
    console,
    print_error,
    print_info,
    print_success,
    print_warning,
    wizard_phase_header,
)


def _get_project_path() -> Path:
    """Get and validate the current project path."""
    # Try current directory
    project_path = Path.cwd()
    project_service = get_project_service()

    is_valid, _ = project_service.validate_project(project_path)
    if not is_valid:
        print_error("No valid project found in current directory.")
        print_info("Use 'story init <name>' to create a new project,")
        print_info("or 'cd' into an existing project directory.")
        raise typer.Exit(1)

    return project_path


def _get_genre() -> str:
    """Get the project genre from story.json."""
    try:
        project_service = get_project_service()
        project = project_service.open_project(Path.cwd())
        return project.genre
    except Exception:
        return "general"


def new_character(
    name: Optional[str] = typer.Option(
        None,
        "--name",
        "-n",
        help="Pre-fill character name",
    ),
) -> None:
    """Create a new character through guided wizard.

    Walks through 5 phases: basics, appearance, personality, backstory, relationships.
    AI suggestions available when LLM is connected.
    """
    project_path = _get_project_path()
    char_service = get_character_service(project_path)
    genre = _get_genre()

    console.print("\n[bold]Character Creation Wizard[/bold]\n")
    console.print("[dim]Press Ctrl+C at any time to save partial progress and exit.[/dim]\n")

    try:
        # Phase 1: Basics
        basics = _wizard_basics(name, genre)

        # Check if character exists
        if char_service.character_exists(basics.name):
            print_error(f"Character '{basics.name}' already exists.")
            print_info("Use 'story edit character' to modify existing characters.")
            raise typer.Exit(1)

        # Phase 2: Appearance
        appearance = _wizard_appearance(basics.name, genre)

        # Phase 3: Personality
        personality = _wizard_personality(basics.name, basics.role.value, genre)

        # Phase 4: Backstory
        backstory = _wizard_backstory(basics.name, basics.role.value, genre)

        # Phase 5: Relationships (simplified - just show existing chars)
        _wizard_relationships_info(char_service)

        # Review and save
        character = Character(
            basics=basics,
            appearance=appearance,
            personality=personality,
            backstory=backstory,
            relationships=[],
        )

        _display_character_review(character)

        if Confirm.ask("\n[cyan]Save this character?[/cyan]", default=True):
            char_service.create_character(character)
            print_success(f"Character '{basics.name}' created successfully!")
        else:
            print_warning("Character creation cancelled.")

    except KeyboardInterrupt:
        console.print("\n")
        print_warning("Character creation interrupted.")
        raise typer.Exit(0)


def _wizard_basics(prefill_name: str | None, genre: str) -> CharacterBasics:
    """Phase 1: Collect basic character information."""
    wizard_phase_header("Basics", 1, 5)

    llm_service = get_llm_service()

    # Name
    if prefill_name:
        name = prefill_name
        console.print(f"[dim]Character name:[/dim] {name}")
    else:
        # Offer AI name suggestions
        console.print("[dim]Enter a name, or press Enter for AI suggestions[/dim]")
        name = Prompt.ask("[cyan]Character name[/cyan]", default="")

        if not name:
            console.print("[dim]Getting AI suggestions...[/dim]")
            suggestions = asyncio.run(
                llm_service.suggest_names(genre, "protagonist", 5)
            )
            if suggestions:
                console.print("\n[dim]Suggestions:[/dim]")
                for i, s in enumerate(suggestions, 1):
                    console.print(f"  {i}. {s}")
                console.print()
            name = Prompt.ask("[cyan]Character name[/cyan]")

    # Age
    age_str = Prompt.ask("[cyan]Age[/cyan] [dim](optional, press Enter to skip)[/dim]", default="")
    age = int(age_str) if age_str.isdigit() else None

    # Gender
    gender = Prompt.ask("[cyan]Gender[/cyan] [dim](optional)[/dim]", default="")
    gender = gender if gender else None

    # Role
    console.print("\n[dim]Available roles:[/dim]")
    roles = list(CharacterRole)
    for i, role in enumerate(roles, 1):
        console.print(f"  {i}. {role.value}")

    role_choice = Prompt.ask(
        "[cyan]Role[/cyan]",
        choices=[str(i) for i in range(1, len(roles) + 1)] + [r.value for r in roles],
        default="4",  # supporting
    )

    if role_choice.isdigit():
        role = roles[int(role_choice) - 1]
    else:
        role = CharacterRole(role_choice)

    return CharacterBasics(name=name, age=age, gender=gender, role=role)


def _wizard_appearance(char_name: str, genre: str) -> CharacterAppearance | None:
    """Phase 2: Collect character appearance."""
    wizard_phase_header("Appearance", 2, 5)

    console.print("[dim]Describe the character's appearance, or skip for now.[/dim]")
    console.print("[dim]You can enter a brief description for AI expansion.[/dim]\n")

    brief = Prompt.ask(
        "[cyan]Brief appearance description[/cyan] [dim](or Enter to skip)[/dim]",
        default="",
    )

    if not brief:
        return None

    # Try AI expansion
    llm_service = get_llm_service()
    console.print("[dim]Expanding description...[/dim]")

    try:
        expanded = asyncio.run(llm_service.expand_appearance(brief, genre))
        if expanded:
            console.print("\n[dim]AI expanded appearance:[/dim]")

            hair = None
            if expanded.get("hair"):
                h = expanded["hair"]
                hair = HairDescription(
                    color=h.get("color"),
                    style=h.get("style"),
                    length=h.get("length"),
                )
                console.print(f"  Hair: {h.get('color', '')} {h.get('style', '')} {h.get('length', '')}")

            eyes = None
            if expanded.get("eyes"):
                e = expanded["eyes"]
                eyes = EyeDescription(color=e.get("color"), shape=e.get("shape"))
                console.print(f"  Eyes: {e.get('color', '')} {e.get('shape', '')}")

            console.print(f"  Skin: {expanded.get('skin_tone', 'N/A')}")
            console.print(f"  Height: {expanded.get('height', 'N/A')}")
            console.print(f"  Build: {expanded.get('build', 'N/A')}")

            if Confirm.ask("\n[cyan]Use this appearance?[/cyan]", default=True):
                return CharacterAppearance(
                    hair=hair,
                    eyes=eyes,
                    skin_tone=expanded.get("skin_tone"),
                    height=expanded.get("height"),
                    build=expanded.get("build"),
                    distinctive_features=expanded.get("distinctive_features", []),
                    clothing_style=expanded.get("clothing_style"),
                    accessories=expanded.get("accessories", []),
                )
    except Exception:
        pass

    # Manual entry fallback
    console.print("\n[dim]Manual entry:[/dim]")
    hair_color = Prompt.ask("[cyan]Hair color[/cyan]", default="")
    eye_color = Prompt.ask("[cyan]Eye color[/cyan]", default="")

    return CharacterAppearance(
        hair=HairDescription(color=hair_color) if hair_color else None,
        eyes=EyeDescription(color=eye_color) if eye_color else None,
    )


def _wizard_personality(char_name: str, role: str, genre: str) -> CharacterPersonality | None:
    """Phase 3: Collect personality traits."""
    wizard_phase_header("Personality", 3, 5)

    console.print("[dim]Define personality traits (3-5 recommended).[/dim]\n")

    llm_service = get_llm_service()

    # Get AI suggestions
    console.print("[dim]Getting trait suggestions...[/dim]")
    suggestions = asyncio.run(llm_service.suggest_traits(role, [], genre, 5))

    if suggestions:
        console.print("\n[dim]Suggested traits:[/dim]")
        for i, s in enumerate(suggestions, 1):
            console.print(f"  {i}. {s}")
        console.print()

    traits_input = Prompt.ask(
        "[cyan]Primary traits[/cyan] [dim](comma-separated, or Enter to skip)[/dim]",
        default="",
    )

    if not traits_input:
        return None

    primary_traits = [t.strip() for t in traits_input.split(",") if t.strip()]

    flaws_input = Prompt.ask(
        "[cyan]Character flaws[/cyan] [dim](comma-separated, or Enter to skip)[/dim]",
        default="",
    )
    flaws = [f.strip() for f in flaws_input.split(",") if f.strip()]

    speaking_style = Prompt.ask(
        "[cyan]Speaking style[/cyan] [dim](e.g., formal, casual, sarcastic)[/dim]",
        default="",
    )

    return CharacterPersonality(
        primary_traits=primary_traits[:5],
        flaws=flaws[:3],
        speaking_style=speaking_style if speaking_style else None,
    )


def _wizard_backstory(char_name: str, role: str, genre: str) -> CharacterBackstory | None:
    """Phase 4: Collect character backstory."""
    wizard_phase_header("Backstory", 4, 5)

    console.print("[dim]Provide a brief backstory summary.[/dim]\n")

    llm_service = get_llm_service()

    # Get guiding questions
    console.print("[dim]Getting guiding questions...[/dim]")
    questions = asyncio.run(
        llm_service.generate_backstory_questions(char_name, role, genre, 3)
    )

    if questions:
        console.print("\n[dim]Consider these questions:[/dim]")
        for q in questions:
            console.print(f"  • {q}")
        console.print()

    summary = Prompt.ask(
        "[cyan]Backstory summary[/cyan] [dim](or Enter to skip)[/dim]",
        default="",
    )

    if not summary:
        return None

    # Offer AI expansion
    if Confirm.ask("\n[cyan]Would you like AI to expand this backstory?[/cyan]", default=False):
        console.print("[dim]Expanding backstory...[/dim]")
        try:
            expanded = asyncio.run(
                llm_service.expand_backstory(summary, char_name, genre)
            )
            console.print(f"\n[dim]Expanded backstory:[/dim]\n{expanded}\n")

            if Confirm.ask("[cyan]Use expanded version?[/cyan]", default=True):
                return CharacterBackstory(summary=summary, full=expanded)
        except Exception:
            pass

    return CharacterBackstory(summary=summary)


def _wizard_relationships_info(char_service) -> None:
    """Phase 5: Show relationship options."""
    wizard_phase_header("Relationships", 5, 5)

    characters = char_service.list_characters()

    if characters:
        console.print("[dim]Existing characters you could relate to:[/dim]")
        for c in characters:
            console.print(f"  • {c['name']} ({c['role']})")
        console.print()
        console.print("[dim]Relationships can be added later with 'story edit character'.[/dim]")
    else:
        console.print("[dim]No other characters exist yet.[/dim]")
        console.print("[dim]Relationships can be added later.[/dim]")

    console.print()


def _display_character_review(character: Character) -> None:
    """Display character summary for review."""
    console.print("\n[bold]Character Review[/bold]\n")

    table = Table(show_header=False, box=None)
    table.add_column("Field", style="dim")
    table.add_column("Value")

    # Basics
    table.add_row("Name", character.basics.name)
    table.add_row("Role", character.basics.role.value)
    if character.basics.age:
        table.add_row("Age", str(character.basics.age))
    if character.basics.gender:
        table.add_row("Gender", character.basics.gender)

    # Appearance
    if character.appearance:
        if character.appearance.hair and character.appearance.hair.color:
            table.add_row("Hair", character.appearance.hair.color)
        if character.appearance.eyes and character.appearance.eyes.color:
            table.add_row("Eyes", character.appearance.eyes.color)

    # Personality
    if character.personality:
        if character.personality.primary_traits:
            table.add_row("Traits", ", ".join(character.personality.primary_traits))
        if character.personality.flaws:
            table.add_row("Flaws", ", ".join(character.personality.flaws))

    # Backstory
    if character.backstory:
        summary = character.backstory.summary
        if len(summary) > 50:
            summary = summary[:50] + "..."
        table.add_row("Backstory", summary)

    console.print(table)

    # Show completion
    completion = character.get_completion_percentage()
    console.print(f"\n[dim]Profile completion: {completion}%[/dim]")


def edit_character(
    name: str = typer.Argument(..., help="Character name to edit"),
    phase: Optional[str] = typer.Option(
        None,
        "--phase",
        "-p",
        help="Go directly to phase (basics, appearance, personality, backstory)",
    ),
) -> None:
    """Edit an existing character.

    Opens the character in the wizard for modifications.
    Use --phase to jump directly to a specific section.
    """
    project_path = _get_project_path()
    char_service = get_character_service(project_path)

    try:
        character = char_service.get_character(name)
    except CharacterNotFoundError:
        print_error(f"Character '{name}' not found.")
        raise typer.Exit(1)

    console.print(f"\n[bold]Editing: {character.basics.name}[/bold]\n")
    _display_character_review(character)

    # Simple edit menu
    console.print("\n[dim]Edit options:[/dim]")
    console.print("  1. Basics (name, age, gender, role)")
    console.print("  2. Appearance")
    console.print("  3. Personality")
    console.print("  4. Backstory")
    console.print("  5. Save and exit")
    console.print("  6. Cancel")

    choice = Prompt.ask("[cyan]Choose option[/cyan]", choices=["1", "2", "3", "4", "5", "6"], default="5")

    if choice == "6":
        print_warning("Edit cancelled.")
        return

    if choice == "5":
        print_info("No changes made.")
        return

    genre = _get_genre()

    if choice == "1":
        character.basics = _wizard_basics(character.basics.name, genre)
    elif choice == "2":
        character.appearance = _wizard_appearance(character.basics.name, genre)
    elif choice == "3":
        character.personality = _wizard_personality(
            character.basics.name, character.basics.role.value, genre
        )
    elif choice == "4":
        character.backstory = _wizard_backstory(
            character.basics.name, character.basics.role.value, genre
        )

    char_service.update_character(character)
    print_success(f"Character '{character.basics.name}' updated!")


def list_characters(
    role: Optional[str] = typer.Option(
        None,
        "--role",
        "-r",
        help="Filter by role (protagonist, antagonist, etc.)",
    ),
    detailed: bool = typer.Option(
        False,
        "--detailed",
        "-d",
        help="Show full details",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON",
    ),
) -> None:
    """List all characters in the project.

    Shows character name, role, and completion percentage.
    """
    project_path = _get_project_path()
    char_service = get_character_service(project_path)

    characters = char_service.list_characters(role_filter=role)

    if not characters:
        print_info("No characters found.")
        if role:
            print_info(f"No characters with role '{role}'.")
        print_info("Use 'story new character' to create one.")
        return

    if json_output:
        import json
        console.print(json.dumps(characters, indent=2))
        return

    # Table output
    table = Table(title="Characters")
    table.add_column("Name", style="cyan")
    table.add_column("Role", style="green")
    table.add_column("Age")
    table.add_column("Completion", justify="right")

    for char in characters:
        age_str = str(char["age"]) if char["age"] else "-"
        table.add_row(
            char["name"],
            char["role"],
            age_str,
            f"{char['completion']}%",
        )

    console.print(table)

    if detailed:
        console.print("\n[dim]Use 'story edit character <name>' for full details.[/dim]")


def delete_character(
    name: str = typer.Argument(..., help="Character name to delete"),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Force delete even with relationships",
    ),
) -> None:
    """Delete a character from the project.

    Requires confirmation. Use --force to delete even if other
    characters have relationships to this one.
    """
    project_path = _get_project_path()
    char_service = get_character_service(project_path)

    # Check if character exists
    try:
        character = char_service.get_character(name)
    except CharacterNotFoundError:
        print_error(f"Character '{name}' not found.")
        raise typer.Exit(1)

    # Check dependencies
    dependencies = char_service.get_relationship_dependencies(name)

    if dependencies and not force:
        print_warning(f"Character '{name}' is referenced by other characters:")
        for dep in dependencies:
            console.print(f"  • {dep}")
        console.print()
        print_info("Use --force to delete anyway (will remove relationships).")
        raise typer.Exit(1)

    # Confirm deletion
    console.print(f"\n[bold]Delete character: {character.basics.name}[/bold]")
    console.print(f"  Role: {character.basics.role.value}")
    console.print(f"  Completion: {character.get_completion_percentage()}%")

    if dependencies:
        print_warning(f"This will remove relationships from: {', '.join(dependencies)}")

    if not Confirm.ask("\n[red]Are you sure you want to delete this character?[/red]", default=False):
        print_info("Deletion cancelled.")
        return

    try:
        affected = char_service.delete_character(name, force=force)
        print_success(f"Character '{name}' deleted.")
        if affected:
            print_info(f"Removed relationships from: {', '.join(affected)}")
    except RelationshipDependencyError as e:
        print_error(str(e))
        raise typer.Exit(1)
