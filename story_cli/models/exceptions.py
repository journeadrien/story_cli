"""Custom exceptions for Story CLI.

Provides a hierarchy of exceptions for error handling throughout the application.
"""


class StoryCliError(Exception):
    """Base exception for all Story CLI errors."""

    pass


class ProjectError(StoryCliError):
    """Base exception for project-related errors."""

    pass


class ProjectNotFoundError(ProjectError):
    """Raised when a project directory or structure is not found."""

    def __init__(self, path: str | None = None) -> None:
        self.path = path
        message = "Project not found"
        if path:
            message = f"Project not found at: {path}"
        super().__init__(message)


class ProjectValidationError(ProjectError):
    """Raised when project structure is invalid."""

    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        message = "Invalid project structure: " + "; ".join(errors)
        super().__init__(message)


class ProjectExistsError(ProjectError):
    """Raised when attempting to create a project that already exists."""

    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(f"Project already exists: {name}")


class CharacterError(StoryCliError):
    """Base exception for character-related errors."""

    pass


class CharacterNotFoundError(CharacterError):
    """Raised when a character does not exist."""

    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(f"Character not found: {name}")


class CharacterExistsError(CharacterError):
    """Raised when attempting to create a character that already exists."""

    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(f"Character already exists: {name}")


class RelationshipDependencyError(CharacterError):
    """Raised when attempting to delete a character with existing relationships."""

    def __init__(self, character_name: str, dependent_characters: list[str]) -> None:
        self.character_name = character_name
        self.dependent_characters = dependent_characters
        deps = ", ".join(dependent_characters)
        super().__init__(
            f"Cannot delete '{character_name}': referenced by characters: {deps}"
        )


class LLMError(StoryCliError):
    """Base exception for LLM-related errors."""

    pass


class LLMUnavailableError(LLMError):
    """Raised when the LLM service is not available."""

    def __init__(self, host: str | None = None) -> None:
        self.host = host
        message = "LLM service is not available"
        if host:
            message = f"LLM service is not available at: {host}"
        super().__init__(message)


class LLMTimeoutError(LLMError):
    """Raised when LLM connection times out."""

    def __init__(self, timeout: int) -> None:
        self.timeout = timeout
        super().__init__(f"LLM connection timed out after {timeout} seconds")


class ValidationError(StoryCliError):
    """Raised when input validation fails."""

    def __init__(self, field: str, message: str) -> None:
        self.field = field
        super().__init__(f"Invalid {field}: {message}")
