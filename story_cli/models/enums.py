"""Enumeration types for Story CLI models.

Defines character roles, relationship types, and other enumerated values.
"""

from enum import Enum


class CharacterRole(str, Enum):
    """Character's role in the story."""

    PROTAGONIST = "protagonist"
    LOVE_INTEREST = "love_interest"
    ANTAGONIST = "antagonist"
    SUPPORTING = "supporting"
    BACKGROUND = "background"


class RelationshipType(str, Enum):
    """Type of relationship between characters."""

    FAMILY = "family"
    FRIEND = "friend"
    ENEMY = "enemy"
    ROMANTIC = "romantic"
    PROFESSIONAL = "professional"
    ACQUAINTANCE = "acquaintance"


class WizardPhase(str, Enum):
    """Phases of the character creation wizard."""

    BASICS = "basics"
    APPEARANCE = "appearance"
    PERSONALITY = "personality"
    BACKSTORY = "backstory"
    RELATIONSHIPS = "relationships"
    REVIEW = "review"
