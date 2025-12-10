"""Character service for Story CLI.

Handles character CRUD operations and index management.
"""

import json
from datetime import datetime
from pathlib import Path

from story_cli.models.character import (
    Character,
    CharacterIndex,
    CharacterIndexEntry,
)
from story_cli.models.enums import CharacterRole
from story_cli.models.exceptions import (
    CharacterExistsError,
    CharacterNotFoundError,
    ProjectNotFoundError,
    RelationshipDependencyError,
)
from story_cli.utils.validation import sanitize_for_filesystem


class CharacterService:
    """Service for character management operations."""

    STORY_DATA_DIR = "story_data"
    CHARACTERS_DIR = "characters"
    CHARACTERS_INDEX = "characters_index.json"
    DESCRIPTION_FILE = "description.json"

    def __init__(self, project_path: Path) -> None:
        """Initialize service with project path.

        Args:
            project_path: Path to the project root directory
        """
        self.project_path = project_path
        self._characters_dir = project_path / self.STORY_DATA_DIR / self.CHARACTERS_DIR
        self._index_path = project_path / self.STORY_DATA_DIR / self.CHARACTERS_INDEX

    def _validate_project(self) -> None:
        """Ensure the project structure exists."""
        if not self.project_path.exists():
            raise ProjectNotFoundError(str(self.project_path))
        if not self._characters_dir.exists():
            raise ProjectNotFoundError(
                f"Missing characters directory: {self._characters_dir}"
            )

    def _load_index(self) -> CharacterIndex:
        """Load the character index from disk."""
        if not self._index_path.exists():
            return CharacterIndex()
        content = self._index_path.read_text(encoding="utf-8")
        return CharacterIndex.model_validate_json(content)

    def _save_index(self, index: CharacterIndex) -> None:
        """Save the character index to disk."""
        self._index_path.write_text(
            index.model_dump_json(indent=2),
            encoding="utf-8",
        )

    def _get_character_dir(self, name: str) -> Path:
        """Get the directory path for a character."""
        dir_name = sanitize_for_filesystem(name)
        return self._characters_dir / dir_name

    def _get_character_file(self, name: str) -> Path:
        """Get the description.json path for a character."""
        return self._get_character_dir(name) / self.DESCRIPTION_FILE

    def create_character(self, character: Character) -> Path:
        """Create a new character.

        Args:
            character: Character model to save

        Returns:
            Path to character directory

        Raises:
            CharacterExistsError: If character name already exists
            ProjectNotFoundError: If project structure is invalid
        """
        self._validate_project()

        name = character.basics.name
        char_dir = self._get_character_dir(name)

        # Check if character already exists
        if char_dir.exists():
            raise CharacterExistsError(name)

        # Create character directory
        char_dir.mkdir(parents=True)

        # Set timestamps
        now = datetime.now()
        character.created_at = now
        character.updated_at = now

        # Generate LoRA trigger if not set
        if not character.lora_trigger:
            character.lora_trigger = character.generate_lora_trigger()

        # Save character file
        char_file = char_dir / self.DESCRIPTION_FILE
        char_file.write_text(
            character.model_dump_json(indent=2),
            encoding="utf-8",
        )

        # Update index
        index = self._load_index()
        entry = CharacterIndexEntry(
            name=name,
            role=character.basics.role,
            age=character.basics.age,
            path=f"{self.CHARACTERS_DIR}/{char_dir.name}",
            updated_at=now,
        )
        index.add_entry(entry)
        self._save_index(index)

        return char_dir

    def get_character(self, name: str) -> Character:
        """Load a character by name.

        Args:
            name: Character name (case-insensitive)

        Returns:
            Loaded Character model

        Raises:
            CharacterNotFoundError: If character doesn't exist
        """
        self._validate_project()

        # First try the index for the correct path
        index = self._load_index()
        entry = index.get_entry(name)

        if entry:
            char_file = self.project_path / self.STORY_DATA_DIR / entry.path / self.DESCRIPTION_FILE
            if char_file.exists():
                content = char_file.read_text(encoding="utf-8")
                return Character.model_validate_json(content)

        # Fallback: try direct lookup
        char_file = self._get_character_file(name)
        if char_file.exists():
            content = char_file.read_text(encoding="utf-8")
            return Character.model_validate_json(content)

        raise CharacterNotFoundError(name)

    def update_character(self, character: Character) -> None:
        """Update an existing character.

        Args:
            character: Updated Character model

        Raises:
            CharacterNotFoundError: If character doesn't exist
        """
        self._validate_project()

        name = character.basics.name
        char_file = self._get_character_file(name)

        if not char_file.exists():
            # Try finding via index
            index = self._load_index()
            entry = index.get_entry(name)
            if entry:
                char_file = self.project_path / self.STORY_DATA_DIR / entry.path / self.DESCRIPTION_FILE
            if not char_file.exists():
                raise CharacterNotFoundError(name)

        # Update timestamp
        character.updated_at = datetime.now()

        # Regenerate LoRA trigger if appearance changed
        if character.appearance:
            character.lora_trigger = character.generate_lora_trigger()

        # Save character file
        char_file.write_text(
            character.model_dump_json(indent=2),
            encoding="utf-8",
        )

        # Update index
        index = self._load_index()
        entry = CharacterIndexEntry(
            name=name,
            role=character.basics.role,
            age=character.basics.age,
            path=f"{self.CHARACTERS_DIR}/{self._get_character_dir(name).name}",
            updated_at=character.updated_at,
        )
        index.add_entry(entry)
        self._save_index(index)

    def delete_character(self, name: str, force: bool = False) -> list[str]:
        """Delete a character.

        Args:
            name: Character name to delete
            force: If True, also remove relationship references

        Returns:
            List of affected characters (those with relationships to deleted)

        Raises:
            CharacterNotFoundError: If character doesn't exist
            RelationshipDependencyError: If character has relationships and force=False
        """
        self._validate_project()

        # Check if character exists
        char_dir = self._get_character_dir(name)
        if not char_dir.exists():
            # Try finding via index
            index = self._load_index()
            entry = index.get_entry(name)
            if entry:
                char_dir = self.project_path / self.STORY_DATA_DIR / entry.path
            if not char_dir.exists():
                raise CharacterNotFoundError(name)

        # Check for dependencies
        dependencies = self.get_relationship_dependencies(name)

        if dependencies and not force:
            raise RelationshipDependencyError(name, dependencies)

        # Remove relationship references from other characters if force
        if dependencies and force:
            for dep_name in dependencies:
                try:
                    dep_char = self.get_character(dep_name)
                    dep_char.relationships = [
                        r for r in dep_char.relationships
                        if r.target_character.lower() != name.lower()
                    ]
                    self.update_character(dep_char)
                except CharacterNotFoundError:
                    pass

        # Delete character directory
        import shutil
        shutil.rmtree(char_dir)

        # Update index
        index = self._load_index()
        index.remove_entry(name)
        self._save_index(index)

        return dependencies

    def list_characters(
        self,
        role_filter: str | None = None,
    ) -> list[dict]:
        """List all characters with optional filtering.

        Args:
            role_filter: Filter by role (protagonist, antagonist, etc.)

        Returns:
            List of character summary dicts with:
                - name: str
                - role: str
                - age: int | None
                - completion: int (percentage)
        """
        self._validate_project()

        index = self._load_index()
        result = []

        for entry in index.characters:
            # Apply role filter
            if role_filter:
                try:
                    filter_role = CharacterRole(role_filter.lower())
                    if entry.role != filter_role:
                        continue
                except ValueError:
                    # Invalid role filter, skip filtering
                    pass

            # Load full character for completion percentage
            try:
                character = self.get_character(entry.name)
                completion = character.get_completion_percentage()
            except CharacterNotFoundError:
                completion = 0

            result.append({
                "name": entry.name,
                "role": entry.role.value,
                "age": entry.age,
                "completion": completion,
            })

        return result

    def character_exists(self, name: str) -> bool:
        """Check if a character exists."""
        try:
            self._validate_project()
        except ProjectNotFoundError:
            return False

        index = self._load_index()
        return index.get_entry(name) is not None

    def get_relationship_dependencies(self, name: str) -> list[str]:
        """Get names of characters that have relationships to this character.

        Args:
            name: Character name to check

        Returns:
            List of character names with relationships to the given character
        """
        self._validate_project()

        dependencies = []
        index = self._load_index()

        for entry in index.characters:
            if entry.name.lower() == name.lower():
                continue

            try:
                character = self.get_character(entry.name)
                for rel in character.relationships:
                    if rel.target_character.lower() == name.lower():
                        dependencies.append(entry.name)
                        break
            except CharacterNotFoundError:
                pass

        return dependencies

    def rebuild_index(self) -> None:
        """Rebuild the characters_index.json file from disk."""
        self._validate_project()

        index = CharacterIndex()

        # Scan all character directories
        if self._characters_dir.exists():
            for char_dir in self._characters_dir.iterdir():
                if not char_dir.is_dir():
                    continue

                desc_file = char_dir / self.DESCRIPTION_FILE
                if not desc_file.exists():
                    continue

                try:
                    content = desc_file.read_text(encoding="utf-8")
                    character = Character.model_validate_json(content)

                    entry = CharacterIndexEntry(
                        name=character.basics.name,
                        role=character.basics.role,
                        age=character.basics.age,
                        path=f"{self.CHARACTERS_DIR}/{char_dir.name}",
                        updated_at=character.updated_at,
                    )
                    index.add_entry(entry)
                except Exception:
                    # Skip invalid character files
                    continue

        self._save_index(index)


def get_character_service(project_path: Path) -> CharacterService:
    """Get a character service instance for a project."""
    return CharacterService(project_path)
