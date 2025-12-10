"""Relationship model for Story CLI.

This module re-exports the Relationship model from character.py for convenience.
The Relationship model is embedded within the Character model.
"""

from story_cli.models.character import Relationship

__all__ = ["Relationship"]
