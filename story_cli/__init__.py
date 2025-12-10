"""Story CLI - AI-Powered Visual Novel Story Builder.

A terminal-based creative writing assistant that helps authors develop
visual novel stories through structured wizards and iterative planning
workflows, powered by local LLMs.
"""

__version__ = "0.1.0"
__author__ = "Story CLI Team"

from story_cli.models.exceptions import StoryCliError

__all__ = ["__version__", "__author__", "StoryCliError"]
