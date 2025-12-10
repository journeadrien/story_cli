"""Character models for Story CLI.

Defines all character-related Pydantic models for the character wizard.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from story_cli.models.enums import CharacterRole, RelationshipType


class CharacterBasics(BaseModel):
    """Basic character identification."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Character name (unique within project)",
    )
    age: Optional[int] = Field(
        None,
        ge=0,
        le=500,
        description="Character age",
    )
    gender: Optional[str] = Field(
        None,
        max_length=50,
        description="Character gender",
    )
    role: CharacterRole = Field(
        CharacterRole.SUPPORTING,
        description="Character's role in the story",
    )

    @field_validator("name")
    @classmethod
    def validate_character_name(cls, v: str) -> str:
        """Validate character name for filesystem safety."""
        stripped = v.strip()
        if not stripped:
            raise ValueError("Character name cannot be empty")

        # Allow letters, numbers, spaces, hyphens, underscores, apostrophes
        test_str = (
            stripped.replace(" ", "")
            .replace("-", "")
            .replace("_", "")
            .replace("'", "")
        )
        if not test_str.isalnum():
            raise ValueError(
                "Name can only contain letters, numbers, spaces, "
                "hyphens, underscores, and apostrophes"
            )
        return stripped


class HairDescription(BaseModel):
    """Hair appearance details."""

    color: Optional[str] = Field(
        None,
        max_length=50,
        description="Hair color",
    )
    style: Optional[str] = Field(
        None,
        max_length=50,
        description="Hair style (e.g., long, short, curly)",
    )
    length: Optional[str] = Field(
        None,
        max_length=50,
        description="Hair length descriptor",
    )


class EyeDescription(BaseModel):
    """Eye appearance details."""

    color: Optional[str] = Field(
        None,
        max_length=50,
        description="Eye color",
    )
    shape: Optional[str] = Field(
        None,
        max_length=50,
        description="Eye shape descriptor",
    )


class CharacterAppearance(BaseModel):
    """Physical appearance details for consistent visual generation."""

    hair: Optional[HairDescription] = Field(
        None,
        description="Hair details",
    )
    eyes: Optional[EyeDescription] = Field(
        None,
        description="Eye details",
    )
    skin_tone: Optional[str] = Field(
        None,
        max_length=50,
        description="Skin tone",
    )
    height: Optional[str] = Field(
        None,
        max_length=50,
        description="Height descriptor",
    )
    build: Optional[str] = Field(
        None,
        max_length=50,
        description="Body build descriptor",
    )
    distinctive_features: list[str] = Field(
        default_factory=list,
        description="Notable features (scars, birthmarks, etc.)",
    )
    clothing_style: Optional[str] = Field(
        None,
        max_length=200,
        description="Typical clothing style",
    )
    accessories: list[str] = Field(
        default_factory=list,
        description="Common accessories",
    )

    @field_validator("distinctive_features", "accessories")
    @classmethod
    def limit_list_length(cls, v: list[str]) -> list[str]:
        """Limit list to 10 items."""
        if len(v) > 10:
            raise ValueError("Maximum 10 items allowed")
        return v


class CharacterPersonality(BaseModel):
    """Personality traits for consistent dialogue and behavior."""

    primary_traits: list[str] = Field(
        default_factory=list,
        description="Core personality traits (3-5)",
    )
    secondary_traits: list[str] = Field(
        default_factory=list,
        description="Secondary traits (2-3)",
    )
    flaws: list[str] = Field(
        default_factory=list,
        description="Character flaws (1-3)",
    )
    speaking_style: Optional[str] = Field(
        None,
        max_length=100,
        description="How they speak (formal, casual, etc.)",
    )
    speech_quirks: list[str] = Field(
        default_factory=list,
        description="Speech quirks or catchphrases",
    )
    motivations: list[str] = Field(
        default_factory=list,
        description="What drives them",
    )
    fears: list[str] = Field(
        default_factory=list,
        description="What they fear",
    )
    secrets: list[str] = Field(
        default_factory=list,
        description="Hidden aspects of personality",
    )

    @field_validator("primary_traits")
    @classmethod
    def limit_primary_traits(cls, v: list[str]) -> list[str]:
        """Limit primary traits to 5 items."""
        if len(v) > 5:
            raise ValueError("Maximum 5 primary traits allowed")
        return v

    @field_validator("secondary_traits", "flaws")
    @classmethod
    def limit_secondary_traits(cls, v: list[str]) -> list[str]:
        """Limit secondary traits and flaws to 3 items."""
        if len(v) > 3:
            raise ValueError("Maximum 3 items allowed")
        return v

    @field_validator("speech_quirks", "motivations", "fears", "secrets")
    @classmethod
    def limit_list_items(cls, v: list[str]) -> list[str]:
        """Limit lists to 5 items."""
        if len(v) > 5:
            raise ValueError("Maximum 5 items allowed")
        return v


class CharacterBackstory(BaseModel):
    """Character history and background."""

    summary: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Brief backstory summary",
    )
    full: Optional[str] = Field(
        None,
        max_length=5000,
        description="Detailed backstory (optional)",
    )
    key_events: list[str] = Field(
        default_factory=list,
        description="Formative life events",
    )
    secrets: list[str] = Field(
        default_factory=list,
        description="Things other characters don't know",
    )

    @field_validator("key_events")
    @classmethod
    def limit_key_events(cls, v: list[str]) -> list[str]:
        """Limit key events to 10 items."""
        if len(v) > 10:
            raise ValueError("Maximum 10 key events allowed")
        return v

    @field_validator("secrets")
    @classmethod
    def limit_secrets(cls, v: list[str]) -> list[str]:
        """Limit secrets to 5 items."""
        if len(v) > 5:
            raise ValueError("Maximum 5 secrets allowed")
        return v


class Relationship(BaseModel):
    """Defines a relationship to another character."""

    target_character: str = Field(
        ...,
        description="Name of the related character",
    )
    type: RelationshipType = Field(
        ...,
        description="Type of relationship",
    )
    dynamic: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Description of the relationship dynamic",
    )
    initial_feeling: Optional[str] = Field(
        None,
        max_length=200,
        description="How they felt about each other initially",
    )
    history: Optional[str] = Field(
        None,
        max_length=500,
        description="History of the relationship",
    )
    tension_points: list[str] = Field(
        default_factory=list,
        description="Sources of conflict or tension",
    )

    @field_validator("tension_points")
    @classmethod
    def limit_tension_points(cls, v: list[str]) -> list[str]:
        """Limit tension points to 5 items."""
        if len(v) > 5:
            raise ValueError("Maximum 5 tension points allowed")
        return v


class Character(BaseModel):
    """Complete character model combining all phases."""

    basics: CharacterBasics = Field(
        ...,
        description="Basic character info",
    )
    appearance: Optional[CharacterAppearance] = Field(
        None,
        description="Physical appearance",
    )
    personality: Optional[CharacterPersonality] = Field(
        None,
        description="Personality traits",
    )
    backstory: Optional[CharacterBackstory] = Field(
        None,
        description="Character history",
    )
    relationships: list[Relationship] = Field(
        default_factory=list,
        description="Relationships to other characters",
    )
    lora_trigger: Optional[str] = Field(
        None,
        description="Auto-generated LoRA trigger for image generation",
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Creation timestamp",
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        description="Last update timestamp",
    )

    def get_completion_percentage(self) -> int:
        """Calculate how complete the character profile is."""
        sections = [
            self.basics is not None,
            self.appearance is not None,
            self.personality is not None,
            self.backstory is not None,
            len(self.relationships) > 0,
        ]
        return int(sum(sections) / len(sections) * 100)

    def generate_lora_trigger(self) -> str:
        """Generate LoRA trigger string from appearance."""
        if not self.appearance:
            return self.basics.name.lower().replace(" ", "_")

        parts = [self.basics.name.lower().replace(" ", "_")]

        if self.appearance.hair:
            hair_parts = []
            if self.appearance.hair.color:
                hair_parts.append(self.appearance.hair.color)
            if self.appearance.hair.style:
                hair_parts.append(self.appearance.hair.style)
            if hair_parts:
                parts.append("_".join(hair_parts) + "_hair")

        if self.appearance.eyes and self.appearance.eyes.color:
            parts.append(f"{self.appearance.eyes.color}_eyes")

        if self.appearance.distinctive_features:
            for feature in self.appearance.distinctive_features[:2]:
                parts.append(feature.lower().replace(" ", "_"))

        return ", ".join(parts)

    @model_validator(mode="after")
    def update_lora_trigger(self) -> "Character":
        """Auto-update LoRA trigger when appearance changes."""
        if self.appearance and not self.lora_trigger:
            self.lora_trigger = self.generate_lora_trigger()
        return self

    class Config:
        """Pydantic model configuration."""

        json_schema_extra = {
            "example": {
                "basics": {
                    "name": "Alex Chen",
                    "age": 25,
                    "gender": "non-binary",
                    "role": "protagonist",
                },
                "appearance": {
                    "hair": {"color": "black", "style": "short", "length": "short"},
                    "eyes": {"color": "brown", "shape": "almond"},
                    "skin_tone": "tan",
                    "height": "average",
                    "build": "athletic",
                    "distinctive_features": ["small scar on chin"],
                    "clothing_style": "casual streetwear",
                    "accessories": ["silver necklace"],
                },
                "personality": {
                    "primary_traits": ["curious", "determined", "empathetic"],
                    "secondary_traits": ["witty", "stubborn"],
                    "flaws": ["impulsive", "overthinks"],
                    "speaking_style": "casual and warm",
                    "speech_quirks": ["uses 'like' often"],
                    "motivations": ["finding the truth", "protecting family"],
                    "fears": ["being alone", "failure"],
                    "secrets": ["witnessed a crime as a child"],
                },
                "backstory": {
                    "summary": "A journalism student uncovering family secrets.",
                    "key_events": ["parents' divorce", "moved to new city"],
                },
                "relationships": [],
                "created_at": "2025-01-01T12:00:00",
                "updated_at": "2025-01-01T12:00:00",
            }
        }


class CharacterIndexEntry(BaseModel):
    """Entry in the character index for fast lookups."""

    name: str = Field(
        ...,
        description="Character name",
    )
    role: CharacterRole = Field(
        ...,
        description="Character role",
    )
    age: Optional[int] = Field(
        None,
        description="Character age",
    )
    path: str = Field(
        ...,
        description="Relative path to character directory",
    )
    updated_at: datetime = Field(
        ...,
        description="Last update timestamp",
    )


class CharacterIndex(BaseModel):
    """Character index for fast lookups."""

    characters: list[CharacterIndexEntry] = Field(
        default_factory=list,
        description="List of character entries",
    )

    def get_entry(self, name: str) -> Optional[CharacterIndexEntry]:
        """Get an entry by character name (case-insensitive)."""
        name_lower = name.lower()
        for entry in self.characters:
            if entry.name.lower() == name_lower:
                return entry
        return None

    def add_entry(self, entry: CharacterIndexEntry) -> None:
        """Add or update an entry."""
        # Remove existing entry with same name
        self.characters = [e for e in self.characters if e.name.lower() != entry.name.lower()]
        self.characters.append(entry)

    def remove_entry(self, name: str) -> bool:
        """Remove an entry by name. Returns True if removed."""
        original_len = len(self.characters)
        self.characters = [e for e in self.characters if e.name.lower() != name.lower()]
        return len(self.characters) < original_len
