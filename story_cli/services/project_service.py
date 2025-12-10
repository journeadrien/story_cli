"""Project service for Story CLI.

Handles project lifecycle operations including creation, validation, and opening.
"""

import json
from datetime import datetime
from pathlib import Path

from story_cli.models.exceptions import (
    ProjectExistsError,
    ProjectNotFoundError,
    ProjectValidationError,
)
from story_cli.models.project import Project
from story_cli.utils.validation import sanitize_for_filesystem


class ProjectService:
    """Service for project management operations."""

    # Expected project structure
    STORY_JSON = "story.json"
    STORY_DATA_DIR = "story_data"
    CHARACTERS_DIR = "characters"
    CHARACTERS_INDEX = "characters_index.json"

    def create_project(
        self,
        name: str,
        genre: str,
        synopsis: str,
        parent_dir: Path | None = None,
    ) -> Path:
        """Create a new project with the given metadata.

        Args:
            name: Project name (used as directory name)
            genre: Story genre
            synopsis: Brief story synopsis
            parent_dir: Parent directory for project (defaults to cwd)

        Returns:
            Path to created project directory

        Raises:
            ProjectExistsError: If project directory already exists
            ValueError: If validation fails
        """
        # Use current working directory if not specified
        parent = parent_dir or Path.cwd()

        # Create filesystem-safe directory name
        dir_name = sanitize_for_filesystem(name)
        project_path = parent / dir_name

        # Check if project already exists
        if project_path.exists():
            raise ProjectExistsError(name)

        # Create the project model (validates the data)
        project = Project(
            name=name,
            genre=genre,
            synopsis=synopsis,
        )

        # Create directory structure
        project_path.mkdir(parents=True)
        story_data_path = project_path / self.STORY_DATA_DIR
        story_data_path.mkdir()
        characters_path = story_data_path / self.CHARACTERS_DIR
        characters_path.mkdir()

        # Write story.json
        story_json_path = project_path / self.STORY_JSON
        story_json_path.write_text(
            project.model_dump_json(indent=2),
            encoding="utf-8",
        )

        # Initialize empty character index
        index_path = story_data_path / self.CHARACTERS_INDEX
        index_data = {"characters": []}
        index_path.write_text(
            json.dumps(index_data, indent=2),
            encoding="utf-8",
        )

        return project_path

    def validate_project(self, path: Path) -> tuple[bool, list[str]]:
        """Validate project structure without loading.

        Args:
            path: Path to project directory

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors: list[str] = []

        # Check project directory exists
        if not path.exists():
            errors.append(f"Project directory does not exist: {path}")
            return False, errors

        if not path.is_dir():
            errors.append(f"Path is not a directory: {path}")
            return False, errors

        # Check story.json exists
        story_json_path = path / self.STORY_JSON
        if not story_json_path.exists():
            errors.append(f"Missing {self.STORY_JSON}")
        elif not story_json_path.is_file():
            errors.append(f"{self.STORY_JSON} is not a file")
        else:
            # Try to parse story.json
            try:
                content = story_json_path.read_text(encoding="utf-8")
                Project.model_validate_json(content)
            except json.JSONDecodeError as e:
                errors.append(f"Invalid JSON in {self.STORY_JSON}: {e}")
            except Exception as e:
                errors.append(f"Invalid project data in {self.STORY_JSON}: {e}")

        # Check story_data directory
        story_data_path = path / self.STORY_DATA_DIR
        if not story_data_path.exists():
            errors.append(f"Missing {self.STORY_DATA_DIR} directory")
        elif not story_data_path.is_dir():
            errors.append(f"{self.STORY_DATA_DIR} is not a directory")
        else:
            # Check characters directory
            characters_path = story_data_path / self.CHARACTERS_DIR
            if not characters_path.exists():
                errors.append(f"Missing {self.STORY_DATA_DIR}/{self.CHARACTERS_DIR} directory")
            elif not characters_path.is_dir():
                errors.append(f"{self.STORY_DATA_DIR}/{self.CHARACTERS_DIR} is not a directory")

        return len(errors) == 0, errors

    def open_project(self, path: Path | None = None) -> Project:
        """Open and validate an existing project.

        Args:
            path: Path to project directory (defaults to cwd)

        Returns:
            Loaded Project model

        Raises:
            ProjectNotFoundError: If project directory doesn't exist
            ProjectValidationError: If project structure is invalid
        """
        project_path = path or Path.cwd()

        # Validate the project structure
        is_valid, errors = self.validate_project(project_path)
        if not is_valid:
            if not project_path.exists() or self.STORY_JSON not in [e for e in errors if self.STORY_JSON in e]:
                raise ProjectNotFoundError(str(project_path))
            raise ProjectValidationError(errors)

        # Load and return the project
        story_json_path = project_path / self.STORY_JSON
        content = story_json_path.read_text(encoding="utf-8")
        return Project.model_validate_json(content)

    def get_project_summary(self, path: Path) -> dict:
        """Get project summary for display.

        Args:
            path: Path to project directory

        Returns:
            Dictionary with:
                - name: str
                - genre: str
                - synopsis: str
                - character_count: int
                - last_modified: datetime
        """
        # Load the project
        project = self.open_project(path)

        # Count characters from index
        character_count = 0
        index_path = path / self.STORY_DATA_DIR / self.CHARACTERS_INDEX
        if index_path.exists():
            try:
                index_data = json.loads(index_path.read_text(encoding="utf-8"))
                character_count = len(index_data.get("characters", []))
            except (json.JSONDecodeError, KeyError):
                # Fall back to counting directories
                characters_dir = path / self.STORY_DATA_DIR / self.CHARACTERS_DIR
                if characters_dir.exists():
                    character_count = sum(
                        1 for d in characters_dir.iterdir() if d.is_dir()
                    )

        # Get last modified time
        story_json_path = path / self.STORY_JSON
        last_modified = datetime.fromtimestamp(story_json_path.stat().st_mtime)

        return {
            "name": project.name,
            "genre": project.genre,
            "synopsis": project.synopsis,
            "character_count": character_count,
            "last_modified": last_modified,
        }


# Singleton instance
_project_service: ProjectService | None = None


def get_project_service() -> ProjectService:
    """Get the global project service instance."""
    global _project_service
    if _project_service is None:
        _project_service = ProjectService()
    return _project_service
