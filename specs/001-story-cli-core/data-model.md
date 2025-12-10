# Data Model: Story CLI Core

**Feature**: 001-story-cli-core
**Date**: 2025-12-10

## Overview

This document defines the Pydantic data models for Story CLI's core entities. All models support JSON serialization for file persistence.

---

## Entity Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                  Project                                     │
│  story.json                                                                  │
│  ├── name: str                                                              │
│  ├── genre: str                                                             │
│  ├── synopsis: str                                                          │
│  └── created_at: datetime                                                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ contains
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Character Index                                 │
│  characters_index.json (auto-generated)                                      │
│  └── characters: list[CharacterIndexEntry]                                  │
│       ├── name: str                                                         │
│       ├── role: CharacterRole                                               │
│       ├── age: int | None                                                   │
│       ├── path: str                                                         │
│       └── updated_at: datetime                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ references
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                Character                                     │
│  story_data/characters/<name>/description.json                              │
│  ├── basics: CharacterBasics                                                │
│  │    ├── name: str (required, unique)                                      │
│  │    ├── age: int | None                                                   │
│  │    ├── gender: str | None                                                │
│  │    └── role: CharacterRole                                               │
│  ├── appearance: CharacterAppearance | None                                 │
│  │    ├── hair: HairDescription | None                                      │
│  │    ├── eyes: EyeDescription | None                                       │
│  │    ├── skin_tone: str | None                                             │
│  │    ├── height: str | None                                                │
│  │    ├── build: str | None                                                 │
│  │    ├── distinctive_features: list[str]                                   │
│  │    ├── clothing_style: str | None                                        │
│  │    └── accessories: list[str]                                            │
│  ├── personality: CharacterPersonality | None                               │
│  │    ├── primary_traits: list[str] (3-5)                                   │
│  │    ├── secondary_traits: list[str] (2-3)                                 │
│  │    ├── flaws: list[str] (1-3)                                            │
│  │    ├── speaking_style: str | None                                        │
│  │    ├── speech_quirks: list[str]                                          │
│  │    ├── motivations: list[str]                                            │
│  │    ├── fears: list[str]                                                  │
│  │    └── secrets: list[str]                                                │
│  ├── backstory: CharacterBackstory | None                                   │
│  │    ├── summary: str                                                      │
│  │    ├── full: str | None                                                  │
│  │    ├── key_events: list[str]                                             │
│  │    └── secrets: list[str]                                                │
│  ├── relationships: list[Relationship]                                      │
│  ├── lora_trigger: str | None (auto-generated)                              │
│  ├── created_at: datetime                                                   │
│  └── updated_at: datetime                                                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ has many
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                               Relationship                                   │
│  (embedded in Character)                                                     │
│  ├── target_character: str (name reference)                                 │
│  ├── type: RelationshipType                                                 │
│  ├── dynamic: str                                                           │
│  ├── initial_feeling: str | None                                            │
│  ├── history: str | None                                                    │
│  └── tension_points: list[str]                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Enumerations

### CharacterRole

```python
class CharacterRole(str, Enum):
    PROTAGONIST = "protagonist"
    LOVE_INTEREST = "love_interest"
    ANTAGONIST = "antagonist"
    SUPPORTING = "supporting"
    BACKGROUND = "background"
```

### RelationshipType

```python
class RelationshipType(str, Enum):
    FAMILY = "family"
    FRIEND = "friend"
    ENEMY = "enemy"
    ROMANTIC = "romantic"
    PROFESSIONAL = "professional"
    ACQUAINTANCE = "acquaintance"
```

---

## Models

### Project

**File**: `story.json` (project root)

```python
class Project(BaseModel):
    """Root project configuration."""

    name: str = Field(..., min_length=1, max_length=100, description="Project name")
    genre: str = Field(..., min_length=1, max_length=50, description="Story genre (e.g., romance, mystery)")
    synopsis: str = Field(..., min_length=1, max_length=2000, description="Brief story synopsis")
    created_at: datetime = Field(default_factory=datetime.now, description="Project creation timestamp")

    @field_validator("name")
    @classmethod
    def validate_project_name(cls, v: str) -> str:
        """Validate project name for filesystem safety."""
        if not v.replace(" ", "").replace("-", "").replace("_", "").isalnum():
            raise ValueError("Project name can only contain letters, numbers, spaces, hyphens, and underscores")
        return v
```

**Validation Rules**:
- `name`: Required, 1-100 chars, filesystem-safe characters only
- `genre`: Required, 1-50 chars
- `synopsis`: Required, 1-2000 chars
- `created_at`: Auto-generated on creation

---

### CharacterBasics

**Section**: Basics phase of character wizard

```python
class CharacterBasics(BaseModel):
    """Basic character identification."""

    name: str = Field(..., min_length=1, max_length=100, description="Character name (unique within project)")
    age: Optional[int] = Field(None, ge=0, le=500, description="Character age")
    gender: Optional[str] = Field(None, max_length=50, description="Character gender")
    role: CharacterRole = Field(CharacterRole.SUPPORTING, description="Character's role in the story")

    @field_validator("name")
    @classmethod
    def validate_character_name(cls, v: str) -> str:
        """Validate character name for filesystem safety."""
        if not v.replace(" ", "").replace("-", "").replace("_", "").replace("'", "").isalnum():
            raise ValueError("Name can only contain letters, numbers, spaces, hyphens, underscores, and apostrophes")
        return v
```

**Validation Rules**:
- `name`: Required, unique within project, filesystem-safe
- `age`: Optional, 0-500 range (for fantasy characters)
- `gender`: Optional, freeform text
- `role`: Defaults to "supporting"

---

### HairDescription

**Section**: Part of CharacterAppearance

```python
class HairDescription(BaseModel):
    """Hair appearance details."""

    color: Optional[str] = Field(None, max_length=50, description="Hair color")
    style: Optional[str] = Field(None, max_length=50, description="Hair style (e.g., long, short, curly)")
    length: Optional[str] = Field(None, max_length=50, description="Hair length descriptor")
```

---

### EyeDescription

**Section**: Part of CharacterAppearance

```python
class EyeDescription(BaseModel):
    """Eye appearance details."""

    color: Optional[str] = Field(None, max_length=50, description="Eye color")
    shape: Optional[str] = Field(None, max_length=50, description="Eye shape descriptor")
```

---

### CharacterAppearance

**Section**: Appearance phase of character wizard

```python
class CharacterAppearance(BaseModel):
    """Physical appearance details for consistent visual generation."""

    hair: Optional[HairDescription] = Field(None, description="Hair details")
    eyes: Optional[EyeDescription] = Field(None, description="Eye details")
    skin_tone: Optional[str] = Field(None, max_length=50, description="Skin tone")
    height: Optional[str] = Field(None, max_length=50, description="Height descriptor")
    build: Optional[str] = Field(None, max_length=50, description="Body build descriptor")
    distinctive_features: list[str] = Field(default_factory=list, max_length=10, description="Notable features (scars, birthmarks, etc.)")
    clothing_style: Optional[str] = Field(None, max_length=200, description="Typical clothing style")
    accessories: list[str] = Field(default_factory=list, max_length=10, description="Common accessories")
```

**Validation Rules**:
- All fields optional
- `distinctive_features`: Max 10 items
- `accessories`: Max 10 items

---

### CharacterPersonality

**Section**: Personality phase of character wizard

```python
class CharacterPersonality(BaseModel):
    """Personality traits for consistent dialogue and behavior."""

    primary_traits: list[str] = Field(default_factory=list, min_length=0, max_length=5, description="Core personality traits (3-5)")
    secondary_traits: list[str] = Field(default_factory=list, min_length=0, max_length=3, description="Secondary traits (2-3)")
    flaws: list[str] = Field(default_factory=list, min_length=0, max_length=3, description="Character flaws (1-3)")
    speaking_style: Optional[str] = Field(None, max_length=100, description="How they speak (formal, casual, etc.)")
    speech_quirks: list[str] = Field(default_factory=list, max_length=5, description="Speech quirks or catchphrases")
    motivations: list[str] = Field(default_factory=list, max_length=5, description="What drives them")
    fears: list[str] = Field(default_factory=list, max_length=5, description="What they fear")
    secrets: list[str] = Field(default_factory=list, max_length=5, description="Hidden aspects of personality")

    @model_validator(mode="after")
    def validate_trait_counts(self) -> "CharacterPersonality":
        """Warn if trait counts are outside recommended ranges."""
        # Note: These are recommendations, not hard constraints
        return self
```

**Validation Rules**:
- `primary_traits`: 0-5 items (recommended 3-5)
- `secondary_traits`: 0-3 items (recommended 2-3)
- `flaws`: 0-3 items (recommended 1-3)
- `speech_quirks`, `motivations`, `fears`, `secrets`: Max 5 items each

---

### CharacterBackstory

**Section**: Backstory phase of character wizard

```python
class CharacterBackstory(BaseModel):
    """Character history and background."""

    summary: str = Field(..., min_length=1, max_length=500, description="Brief backstory summary")
    full: Optional[str] = Field(None, max_length=5000, description="Detailed backstory (optional)")
    key_events: list[str] = Field(default_factory=list, max_length=10, description="Formative life events")
    secrets: list[str] = Field(default_factory=list, max_length=5, description="Things other characters don't know")
```

**Validation Rules**:
- `summary`: Required, 1-500 chars
- `full`: Optional, max 5000 chars
- `key_events`: Max 10 items
- `secrets`: Max 5 items

---

### Relationship

**Section**: Relationships phase of character wizard

```python
class Relationship(BaseModel):
    """Defines a relationship to another character."""

    target_character: str = Field(..., description="Name of the related character")
    type: RelationshipType = Field(..., description="Type of relationship")
    dynamic: str = Field(..., min_length=1, max_length=200, description="Description of the relationship dynamic")
    initial_feeling: Optional[str] = Field(None, max_length=200, description="How they felt about each other initially")
    history: Optional[str] = Field(None, max_length=500, description="History of the relationship")
    tension_points: list[str] = Field(default_factory=list, max_length=5, description="Sources of conflict or tension")
```

**Validation Rules**:
- `target_character`: Required (must exist in project)
- `type`: Required, from RelationshipType enum
- `dynamic`: Required, 1-200 chars
- `initial_feeling`: Optional, max 200 chars
- `history`: Optional, max 500 chars
- `tension_points`: Max 5 items

---

### Character (Complete Model)

**File**: `story_data/characters/<name>/description.json`

```python
class Character(BaseModel):
    """Complete character model combining all phases."""

    basics: CharacterBasics = Field(..., description="Basic character info")
    appearance: Optional[CharacterAppearance] = Field(None, description="Physical appearance")
    personality: Optional[CharacterPersonality] = Field(None, description="Personality traits")
    backstory: Optional[CharacterBackstory] = Field(None, description="Character history")
    relationships: list[Relationship] = Field(default_factory=list, description="Relationships to other characters")
    lora_trigger: Optional[str] = Field(None, description="Auto-generated LoRA trigger for image generation")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")

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
```

---

### CharacterIndexEntry

**File**: `story_data/characters_index.json`

```python
class CharacterIndexEntry(BaseModel):
    """Entry in the character index for fast lookups."""

    name: str = Field(..., description="Character name")
    role: CharacterRole = Field(..., description="Character role")
    age: Optional[int] = Field(None, description="Character age")
    path: str = Field(..., description="Relative path to character directory")
    updated_at: datetime = Field(..., description="Last update timestamp")


class CharacterIndex(BaseModel):
    """Character index for fast lookups."""

    characters: list[CharacterIndexEntry] = Field(default_factory=list, description="List of character entries")
```

---

## File Structure

```
<project-name>/
├── story.json                           # Project metadata
└── story_data/
    ├── characters_index.json            # Auto-generated index
    └── characters/
        ├── alex_chen/
        │   └── description.json         # Full character data
        ├── sarah_miller/
        │   └── description.json
        └── ...
```

---

## State Transitions

### Character Lifecycle

```
[Not Created]
    │
    │ story new character
    ▼
[Wizard: Basics] ─────────────────────┐
    │                                 │
    │ complete basics                 │ quit (partial save offered)
    ▼                                 │
[Wizard: Appearance] ─────────────────┤
    │                                 │
    │ complete appearance             │
    ▼                                 │
[Wizard: Personality] ────────────────┤
    │                                 │
    │ complete personality            │
    ▼                                 │
[Wizard: Backstory] ──────────────────┤
    │                                 │
    │ complete backstory              │
    ▼                                 │
[Wizard: Relationships] ──────────────┤
    │                                 │
    │ complete relationships          │
    ▼                                 │
[Wizard: Review] ─────────────────────┘
    │
    │ save
    ▼
[Saved] ◄──────────────────────────────
    │         │
    │ edit    │ delete (with confirmation)
    ▼         ▼
[Editing]  [Deleted]
```

### Project Lifecycle

```
[Not Initialized]
    │
    │ story init <name>
    ▼
[Initialized]
    │
    │ story open (or story open <path>)
    ▼
[Open/Active]
    │
    │ (implicit close on exit)
    ▼
[Closed]
```

---

## Validation Rules Summary

| Entity | Field | Rule |
|--------|-------|------|
| Project | name | Required, 1-100 chars, filesystem-safe |
| Project | genre | Required, 1-50 chars |
| Project | synopsis | Required, 1-2000 chars |
| Character | basics.name | Required, unique, filesystem-safe |
| Character | basics.age | 0-500 |
| Character | basics.role | Enum: protagonist, love_interest, antagonist, supporting, background |
| Character | personality.primary_traits | Max 5 items |
| Character | backstory.summary | Required if backstory provided, 1-500 chars |
| Character | backstory.full | Max 5000 chars |
| Relationship | target_character | Must exist in project |
| Relationship | type | Enum: family, friend, enemy, romantic, professional, acquaintance |
| Relationship | dynamic | Required, 1-200 chars |

---

## Indexes and Lookups

### characters_index.json

- **Purpose**: Fast character lookups without reading all files
- **Rebuilt**: Automatically when any character is created, modified, or deleted
- **Contents**: Name, role, age, path, updated_at for each character

### Usage Patterns

```python
# List all characters
index = CharacterIndex.model_validate_json(index_path.read_text())
for entry in index.characters:
    print(f"{entry.name} ({entry.role.value})")

# Filter by role
protagonists = [e for e in index.characters if e.role == CharacterRole.PROTAGONIST]

# Load full character
char_path = project_path / entry.path / "description.json"
character = Character.model_validate_json(char_path.read_text())
```
