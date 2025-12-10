"""Pydantic data models for Story CLI.

This module contains all data models used for project, character,
and relationship management.
"""

from story_cli.models.character import (
    Character,
    CharacterAppearance,
    CharacterBackstory,
    CharacterBasics,
    CharacterIndex,
    CharacterIndexEntry,
    CharacterPersonality,
    EyeDescription,
    HairDescription,
    Relationship,
)
from story_cli.models.enums import CharacterRole, RelationshipType
from story_cli.models.exceptions import (
    CharacterExistsError,
    CharacterNotFoundError,
    LLMTimeoutError,
    LLMUnavailableError,
    ProjectExistsError,
    ProjectNotFoundError,
    ProjectValidationError,
    RelationshipDependencyError,
    StoryCliError,
    ValidationError,
)
from story_cli.models.project import Project

__all__ = [
    # Project
    "Project",
    # Character
    "Character",
    "CharacterBasics",
    "CharacterAppearance",
    "CharacterPersonality",
    "CharacterBackstory",
    "CharacterIndex",
    "CharacterIndexEntry",
    "HairDescription",
    "EyeDescription",
    "Relationship",
    # Enums
    "CharacterRole",
    "RelationshipType",
    # Exceptions
    "StoryCliError",
    "ProjectNotFoundError",
    "ProjectValidationError",
    "ProjectExistsError",
    "CharacterNotFoundError",
    "CharacterExistsError",
    "RelationshipDependencyError",
    "LLMUnavailableError",
    "LLMTimeoutError",
    "ValidationError",
]
