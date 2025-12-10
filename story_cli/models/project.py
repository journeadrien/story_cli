"""Project model for Story CLI.

Defines the Project entity that represents a story project.
"""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class Project(BaseModel):
    """Root project configuration stored in story.json."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Project name",
    )
    genre: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Story genre (e.g., romance, mystery, fantasy)",
    )
    synopsis: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Brief story synopsis",
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Project creation timestamp",
    )

    @field_validator("name")
    @classmethod
    def validate_project_name(cls, v: str) -> str:
        """Validate project name for filesystem safety."""
        stripped = v.strip()
        if not stripped:
            raise ValueError("Project name cannot be empty")

        # Check for valid characters
        test_str = stripped.replace(" ", "").replace("-", "").replace("_", "")
        if not test_str.isalnum():
            raise ValueError(
                "Project name can only contain letters, numbers, "
                "spaces, hyphens, and underscores"
            )
        return stripped

    @field_validator("genre")
    @classmethod
    def validate_genre(cls, v: str) -> str:
        """Validate and normalize genre."""
        stripped = v.strip()
        if not stripped:
            raise ValueError("Genre cannot be empty")
        return stripped.lower()

    @field_validator("synopsis")
    @classmethod
    def validate_synopsis(cls, v: str) -> str:
        """Validate synopsis."""
        stripped = v.strip()
        if not stripped:
            raise ValueError("Synopsis cannot be empty")
        return stripped

    class Config:
        """Pydantic model configuration."""

        json_schema_extra = {
            "example": {
                "name": "My Visual Novel",
                "genre": "romance",
                "synopsis": "A heartwarming story about finding love in unexpected places.",
                "created_at": "2025-01-01T12:00:00",
            }
        }
