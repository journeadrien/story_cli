"""Character-related prompts for LLM interactions.

Contains prompt templates for AI-assisted character creation features.
"""


def get_name_suggestion_prompt(genre: str, role: str, count: int = 5) -> str:
    """Generate a prompt for suggesting character names.

    Args:
        genre: Story genre (e.g., romance, fantasy)
        role: Character role (e.g., protagonist, antagonist)
        count: Number of names to suggest

    Returns:
        Prompt string for LLM
    """
    return f"""Suggest {count} character names for a {role} in a {genre} story.

Requirements:
- Names should fit the genre and role
- Include a mix of styles (modern, traditional, unique)
- Names should be memorable and easy to pronounce
- Consider cultural diversity

Return ONLY the names, one per line, no numbering or explanations.
"""


def get_appearance_expansion_prompt(brief_description: str, genre: str) -> str:
    """Generate a prompt for expanding a brief appearance description.

    Args:
        brief_description: User's brief appearance description
        genre: Story genre for context

    Returns:
        Prompt string for LLM
    """
    return f"""Expand this brief character appearance description into structured details for a {genre} story.

Brief description: "{brief_description}"

Provide detailed descriptions for each of these aspects in JSON format:
{{
  "hair": {{
    "color": "description of hair color",
    "style": "how the hair is styled",
    "length": "hair length"
  }},
  "eyes": {{
    "color": "eye color",
    "shape": "eye shape description"
  }},
  "skin_tone": "skin tone description",
  "height": "height descriptor (short, average, tall)",
  "build": "body build description",
  "distinctive_features": ["list of notable features"],
  "clothing_style": "typical clothing style",
  "accessories": ["common accessories"]
}}

Keep descriptions concise (1-3 words each when possible).
Return ONLY the JSON, no other text.
"""


def get_trait_suggestion_prompt(
    role: str,
    existing_traits: list[str],
    genre: str,
    count: int = 5,
) -> str:
    """Generate a prompt for suggesting personality traits.

    Args:
        role: Character role
        existing_traits: Already chosen traits
        genre: Story genre
        count: Number of traits to suggest

    Returns:
        Prompt string for LLM
    """
    existing_str = ", ".join(existing_traits) if existing_traits else "none yet"
    return f"""Suggest {count} personality traits for a {role} character in a {genre} story.

Already chosen traits: {existing_str}

Requirements:
- Traits should complement the existing ones
- Include a mix of positive traits and interesting flaws
- Consider traits that create good story dynamics
- Traits should fit the genre conventions

Return ONLY the traits, one per line, no numbering or explanations.
Each trait should be 1-2 words.
"""


def get_backstory_expansion_prompt(
    notes: str,
    character_name: str,
    genre: str,
) -> str:
    """Generate a prompt for expanding backstory notes.

    Args:
        notes: User's brief backstory notes
        character_name: Character's name
        genre: Story genre

    Returns:
        Prompt string for LLM
    """
    return f"""Expand these brief backstory notes into a detailed character backstory for {character_name} in a {genre} story.

Notes: "{notes}"

Write a 2-3 paragraph backstory that:
- Incorporates all the user's notes
- Adds context and motivation
- Creates hooks for story development
- Maintains consistency with the genre
- Suggests formative life events

Write in third person, past tense.
Keep it under 500 words.
"""


def get_backstory_questions_prompt(
    character_name: str,
    role: str,
    genre: str,
    count: int = 5,
) -> str:
    """Generate a prompt for backstory development questions.

    Args:
        character_name: Character's name
        role: Character role
        genre: Story genre
        count: Number of questions

    Returns:
        Prompt string for LLM
    """
    return f"""Generate {count} thought-provoking questions to help develop the backstory of {character_name}, a {role} in a {genre} story.

Questions should:
- Reveal character motivations and fears
- Create opportunities for interesting plot connections
- Help define relationships and conflicts
- Be specific enough to inspire detailed answers
- Fit the genre conventions

Return ONLY the questions, one per line, no numbering.
"""


def get_trait_contradiction_check_prompt(traits: list[str]) -> str:
    """Generate a prompt for checking trait contradictions.

    Args:
        traits: List of personality traits to check

    Returns:
        Prompt string for LLM
    """
    traits_str = ", ".join(traits)
    return f"""Analyze these personality traits for potential contradictions:
{traits_str}

If any traits seem to contradict each other, list each contradictory pair.
If there are no contradictions, respond with "No contradictions found."

Format for contradictions:
trait1 - trait2: brief explanation of why they conflict

Consider that some "contradictions" can actually create interesting character depth.
Only flag truly incompatible trait combinations.
"""


# System prompts for different contexts
SYSTEM_PROMPT_CHARACTER_CREATION = """You are a creative writing assistant helping an author develop characters for their visual novel story.

Your role is to:
- Provide creative, genre-appropriate suggestions
- Help flesh out character details
- Maintain consistency with the story's tone
- Offer options without being prescriptive

Keep responses concise and focused on the specific request.
"""

SYSTEM_PROMPT_APPEARANCE = """You are helping describe character appearances for a visual novel.

Focus on:
- Visual details that would translate well to art
- Distinctive features that make characters memorable
- Genre-appropriate aesthetics
- Consistency in description style
"""

SYSTEM_PROMPT_PERSONALITY = """You are helping develop character personalities for a visual novel.

Focus on:
- Traits that create interesting story dynamics
- Personality aspects that affect dialogue and choices
- Character depth through contradictions and growth potential
- Genre-appropriate archetypes with unique twists
"""

SYSTEM_PROMPT_BACKSTORY = """You are helping develop character backstories for a visual novel.

Focus on:
- Motivations and formative experiences
- Connections to other characters and plot
- Secrets and hidden depths
- Story hooks for character arcs
"""
