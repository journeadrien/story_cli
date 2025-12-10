"""LLM service for Story CLI.

Handles integration with Ollama for AI-assisted content generation.
"""

import json
from typing import AsyncIterator

import httpx

from story_cli.models.exceptions import LLMTimeoutError, LLMUnavailableError
from story_cli.prompts.character_prompts import (
    SYSTEM_PROMPT_APPEARANCE,
    SYSTEM_PROMPT_BACKSTORY,
    SYSTEM_PROMPT_CHARACTER_CREATION,
    SYSTEM_PROMPT_PERSONALITY,
    get_appearance_expansion_prompt,
    get_backstory_expansion_prompt,
    get_backstory_questions_prompt,
    get_name_suggestion_prompt,
    get_trait_contradiction_check_prompt,
    get_trait_suggestion_prompt,
)
from story_cli.utils.config import LLMConfig, get_llm_config


class LLMService:
    """Service for LLM-powered content generation using Ollama."""

    def __init__(self, config: LLMConfig | None = None) -> None:
        """Initialize LLM service.

        Args:
            config: LLM configuration. If None, loads from environment.
        """
        self.config = config or get_llm_config()
        self._available: bool | None = None

    @property
    def base_url(self) -> str:
        """Get the Ollama API base URL."""
        return self.config.host.rstrip("/")

    async def is_available(self) -> bool:
        """Check if the LLM service is available.

        Returns:
            True if LLM responds within timeout, False otherwise.
        """
        if self._available is not None:
            return self._available

        try:
            async with httpx.AsyncClient(timeout=self.config.timeout) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                self._available = response.status_code == 200
        except (httpx.ConnectError, httpx.TimeoutException):
            self._available = False

        return self._available

    def reset_availability_cache(self) -> None:
        """Reset the cached availability status."""
        self._available = None

    async def _generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        stream: bool = False,
    ) -> str | AsyncIterator[str]:
        """Generate content from the LLM.

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            stream: Whether to stream the response

        Returns:
            Generated text or async iterator of chunks

        Raises:
            LLMUnavailableError: If LLM is not available
            LLMTimeoutError: If connection times out
        """
        if not await self.is_available():
            raise LLMUnavailableError(self.config.host)

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.config.model,
            "messages": messages,
            "stream": stream,
        }

        if stream:
            return self._stream_response(payload)
        else:
            return await self._get_response(payload)

    async def _get_response(self, payload: dict) -> str:
        """Get a complete response from the LLM.

        Args:
            payload: Request payload

        Returns:
            Complete response text
        """
        try:
            async with httpx.AsyncClient(timeout=None) as client:
                # Connection timeout, but no read timeout for generation
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                    timeout=httpx.Timeout(self.config.timeout, read=None),
                )
                response.raise_for_status()
                data = response.json()
                return data.get("message", {}).get("content", "")
        except httpx.TimeoutException:
            raise LLMTimeoutError(self.config.timeout)
        except httpx.ConnectError:
            self._available = False
            raise LLMUnavailableError(self.config.host)

    async def _stream_response(self, payload: dict) -> AsyncIterator[str]:
        """Stream a response from the LLM.

        Args:
            payload: Request payload

        Yields:
            Text chunks as they arrive
        """
        import json

        try:
            async with httpx.AsyncClient(timeout=None) as client:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/api/chat",
                    json=payload,
                    timeout=httpx.Timeout(self.config.timeout, read=None),
                ) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if line:
                            try:
                                data = json.loads(line)
                                content = data.get("message", {}).get("content", "")
                                if content:
                                    yield content
                            except json.JSONDecodeError:
                                continue
        except httpx.TimeoutException:
            raise LLMTimeoutError(self.config.timeout)
        except httpx.ConnectError:
            self._available = False
            raise LLMUnavailableError(self.config.host)

    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:
        """Generate content from the LLM.

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt

        Returns:
            Generated text
        """
        result = await self._generate(prompt, system_prompt, stream=False)
        return result  # type: ignore

    async def generate_stream(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> AsyncIterator[str]:
        """Generate content from the LLM with streaming.

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt

        Yields:
            Text chunks as they arrive
        """
        result = await self._generate(prompt, system_prompt, stream=True)
        async for chunk in result:  # type: ignore
            yield chunk

    async def chat_stream(
        self,
        message: str,
        context: str | None = None,
    ) -> AsyncIterator[str]:
        """Stream a chat response.

        Args:
            message: User message
            context: Optional project context

        Yields:
            Text chunks as they arrive

        Raises:
            LLMUnavailableError: If LLM is not available
        """
        system_prompt = (
            "You are a creative writing assistant helping an author develop "
            "their visual novel story. Be helpful, creative, and supportive."
        )
        if context:
            system_prompt += f"\n\nProject context:\n{context}"

        async for chunk in self.generate_stream(message, system_prompt):
            yield chunk

    # Character creation AI features (T047-T052)

    async def suggest_names(
        self,
        genre: str,
        role: str,
        count: int = 5,
    ) -> list[str]:
        """Generate name suggestions based on genre and role.

        Args:
            genre: Story genre
            role: Character role
            count: Number of suggestions

        Returns:
            List of suggested names (empty if LLM unavailable)
        """
        if not await self.is_available():
            return []

        try:
            prompt = get_name_suggestion_prompt(genre, role, count)
            response = await self.generate(prompt, SYSTEM_PROMPT_CHARACTER_CREATION)
            # Parse response - one name per line
            names = [
                name.strip()
                for name in response.strip().split("\n")
                if name.strip()
            ]
            return names[:count]
        except (LLMUnavailableError, LLMTimeoutError):
            return []

    async def expand_appearance(
        self,
        brief_description: str,
        genre: str,
    ) -> dict | None:
        """Expand a brief description into structured appearance.

        Args:
            brief_description: User's brief description
            genre: Story genre for context

        Returns:
            Dictionary with appearance fields, or None if unavailable

        Raises:
            LLMUnavailableError: If LLM is not available
        """
        prompt = get_appearance_expansion_prompt(brief_description, genre)
        response = await self.generate(prompt, SYSTEM_PROMPT_APPEARANCE)

        # Try to parse JSON response
        try:
            # Find JSON in response (in case there's extra text)
            start = response.find("{")
            end = response.rfind("}") + 1
            if start != -1 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass

        return None

    async def suggest_traits(
        self,
        role: str,
        existing_traits: list[str],
        genre: str,
        count: int = 5,
    ) -> list[str]:
        """Suggest personality traits based on role.

        Args:
            role: Character role
            existing_traits: Already chosen traits
            genre: Story genre
            count: Number of suggestions

        Returns:
            List of suggested traits (empty if LLM unavailable)
        """
        if not await self.is_available():
            return []

        try:
            prompt = get_trait_suggestion_prompt(role, existing_traits, genre, count)
            response = await self.generate(prompt, SYSTEM_PROMPT_PERSONALITY)
            # Parse response - one trait per line
            traits = [
                trait.strip()
                for trait in response.strip().split("\n")
                if trait.strip()
            ]
            return traits[:count]
        except (LLMUnavailableError, LLMTimeoutError):
            return []

    async def expand_backstory(
        self,
        notes: str,
        character_name: str,
        genre: str,
    ) -> str:
        """Expand brief notes into full backstory.

        Args:
            notes: User's brief notes
            character_name: Character's name
            genre: Story genre

        Returns:
            Expanded backstory text

        Raises:
            LLMUnavailableError: If LLM is not available
        """
        prompt = get_backstory_expansion_prompt(notes, character_name, genre)
        return await self.generate(prompt, SYSTEM_PROMPT_BACKSTORY)

    async def generate_backstory_questions(
        self,
        character_name: str,
        role: str,
        genre: str,
        count: int = 5,
    ) -> list[str]:
        """Generate questions to help flesh out backstory.

        Args:
            character_name: Character's name
            role: Character role
            genre: Story genre
            count: Number of questions

        Returns:
            List of questions (empty if LLM unavailable)
        """
        if not await self.is_available():
            return []

        try:
            prompt = get_backstory_questions_prompt(character_name, role, genre, count)
            response = await self.generate(prompt, SYSTEM_PROMPT_BACKSTORY)
            # Parse response - one question per line
            questions = [
                q.strip()
                for q in response.strip().split("\n")
                if q.strip() and q.strip().endswith("?")
            ]
            return questions[:count]
        except (LLMUnavailableError, LLMTimeoutError):
            return []

    async def check_trait_contradictions(
        self,
        traits: list[str],
    ) -> list[tuple[str, str]]:
        """Check for contradictory traits.

        Args:
            traits: List of trait strings

        Returns:
            List of (trait1, trait2) tuples that contradict
        """
        if not await self.is_available() or len(traits) < 2:
            return []

        try:
            prompt = get_trait_contradiction_check_prompt(traits)
            response = await self.generate(prompt, SYSTEM_PROMPT_PERSONALITY)

            # Check if no contradictions
            if "no contradiction" in response.lower():
                return []

            # Parse contradictions (format: "trait1 - trait2: explanation")
            contradictions = []
            for line in response.strip().split("\n"):
                if " - " in line and ":" in line:
                    pair_part = line.split(":")[0].strip()
                    if " - " in pair_part:
                        parts = pair_part.split(" - ")
                        if len(parts) >= 2:
                            contradictions.append((parts[0].strip(), parts[1].strip()))

            return contradictions
        except (LLMUnavailableError, LLMTimeoutError):
            return []


# Singleton instance
_llm_service: LLMService | None = None


def get_llm_service() -> LLMService:
    """Get the global LLM service instance."""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
