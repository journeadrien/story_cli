"""Entry point for running Story CLI as a module.

Usage:
    python -m story_cli [COMMAND] [OPTIONS]
"""

from story_cli.cli.main import app

if __name__ == "__main__":
    app()
