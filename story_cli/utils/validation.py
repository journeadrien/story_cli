"""Input validation helpers for Story CLI.

Provides validation functions for names, paths, and other user input.
"""

import re
from pathlib import Path


def is_valid_project_name(name: str) -> bool:
    """Check if a project name is valid for filesystem use.

    Valid names contain only:
    - Letters (a-z, A-Z)
    - Numbers (0-9)
    - Spaces, hyphens, underscores

    Args:
        name: The project name to validate

    Returns:
        True if valid, False otherwise
    """
    if not name or not name.strip():
        return False
    # Allow alphanumeric, spaces, hyphens, underscores
    pattern = r"^[a-zA-Z0-9][a-zA-Z0-9\s\-_]*$"
    return bool(re.match(pattern, name))


def is_valid_character_name(name: str) -> bool:
    """Check if a character name is valid for filesystem use.

    Valid names contain only:
    - Letters (a-z, A-Z)
    - Numbers (0-9)
    - Spaces, hyphens, underscores, apostrophes

    Args:
        name: The character name to validate

    Returns:
        True if valid, False otherwise
    """
    if not name or not name.strip():
        return False
    # Allow alphanumeric, spaces, hyphens, underscores, apostrophes
    pattern = r"^[a-zA-Z][a-zA-Z0-9\s\-_']*$"
    return bool(re.match(pattern, name))


def sanitize_for_filesystem(name: str) -> str:
    """Convert a name to a filesystem-safe directory name.

    Converts spaces to underscores and lowercases the name.

    Args:
        name: The name to sanitize

    Returns:
        Filesystem-safe version of the name
    """
    return name.lower().replace(" ", "_").replace("'", "")


def is_valid_project_path(path: Path) -> tuple[bool, str]:
    """Validate that a path points to a valid Story CLI project.

    Checks for:
    - story.json exists
    - story_data/ directory exists
    - story_data/characters/ directory exists

    Args:
        path: Path to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not path.exists():
        return False, f"Path does not exist: {path}"

    if not path.is_dir():
        return False, f"Path is not a directory: {path}"

    story_json = path / "story.json"
    if not story_json.exists():
        return False, "Missing story.json"

    story_data = path / "story_data"
    if not story_data.exists():
        return False, "Missing story_data/ directory"

    characters_dir = story_data / "characters"
    if not characters_dir.exists():
        return False, "Missing story_data/characters/ directory"

    return True, ""


def validate_genre(genre: str) -> bool:
    """Validate that a genre string is acceptable.

    Args:
        genre: The genre to validate

    Returns:
        True if valid, False otherwise
    """
    if not genre or not genre.strip():
        return False
    # Genre should be 1-50 characters
    return 1 <= len(genre.strip()) <= 50


def validate_synopsis(synopsis: str) -> bool:
    """Validate that a synopsis string is acceptable.

    Args:
        synopsis: The synopsis to validate

    Returns:
        True if valid, False otherwise
    """
    if not synopsis or not synopsis.strip():
        return False
    # Synopsis should be 1-2000 characters
    return 1 <= len(synopsis.strip()) <= 2000
