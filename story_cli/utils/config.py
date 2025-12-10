"""Environment configuration handling for Story CLI.

Manages system-level settings via environment variables.
"""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class LLMConfig:
    """Configuration for LLM connection."""

    host: str
    model: str
    timeout: int

    @classmethod
    def from_env(cls) -> "LLMConfig":
        """Create LLM config from environment variables."""
        return cls(
            host=os.getenv("STORY_OLLAMA_HOST", "http://localhost:11434"),
            model=os.getenv("STORY_MODEL", "qwen3:32b"),
            timeout=int(os.getenv("STORY_LLM_TIMEOUT", "10")),
        )


def get_llm_config() -> LLMConfig:
    """Get the current LLM configuration."""
    return LLMConfig.from_env()


# Default configuration instance
DEFAULT_LLM_CONFIG = LLMConfig(
    host="http://localhost:11434",
    model="qwen3:32b",
    timeout=10,
)
