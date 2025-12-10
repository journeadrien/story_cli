"""Shared pytest fixtures for Story CLI tests."""

import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test projects."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_project(temp_dir: Path) -> Path:
    """Create a sample project structure for testing."""
    project_path = temp_dir / "test-project"
    project_path.mkdir()

    # Create story.json
    story_json = project_path / "story.json"
    story_json.write_text(
        '{"name": "Test Project", "genre": "fantasy", '
        '"synopsis": "A test story", "created_at": "2025-01-01T00:00:00"}'
    )

    # Create story_data structure
    story_data = project_path / "story_data"
    story_data.mkdir()
    (story_data / "characters").mkdir()

    return project_path


@pytest.fixture
def sample_character_data() -> dict:
    """Sample character data for testing."""
    return {
        "basics": {
            "name": "Alex Chen",
            "age": 25,
            "gender": "male",
            "role": "protagonist",
        },
        "appearance": {
            "hair": {"color": "black", "style": "short", "length": "short"},
            "eyes": {"color": "brown", "shape": "almond"},
            "skin_tone": "light",
            "height": "tall",
            "build": "athletic",
            "distinctive_features": ["scar on left cheek"],
            "clothing_style": "casual modern",
            "accessories": ["silver watch"],
        },
        "personality": {
            "primary_traits": ["determined", "compassionate", "curious"],
            "secondary_traits": ["stubborn", "loyal"],
            "flaws": ["impulsive"],
            "speaking_style": "casual",
            "speech_quirks": [],
            "motivations": ["protect family"],
            "fears": ["failure"],
            "secrets": [],
        },
        "backstory": {
            "summary": "A young adventurer seeking their destiny.",
            "full": None,
            "key_events": ["left home at 18"],
            "secrets": [],
        },
        "relationships": [],
        "lora_trigger": None,
    }
