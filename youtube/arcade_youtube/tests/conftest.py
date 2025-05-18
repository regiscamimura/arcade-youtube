import os
from pathlib import Path

import pytest
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials

from arcade_youtube.core.constants import YOUTUBE_READONLY_SCOPE

# Load environment variables from .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)


@pytest.fixture
def credentials():
    """Provide OAuth credentials for testing."""
    return Credentials(
        token=os.getenv("YOUTUBE_TEST_TOKEN"),
        refresh_token=os.getenv("YOUTUBE_TEST_REFRESH_TOKEN"),
        token_uri=os.getenv("YOUTUBE_TEST_TOKEN_URI"),
        client_id=os.getenv("YOUTUBE_TEST_CLIENT_ID"),
        client_secret=os.getenv("YOUTUBE_TEST_CLIENT_SECRET"),
        scopes=[YOUTUBE_READONLY_SCOPE],
    )


@pytest.fixture
def context():
    """Provide a ToolContext instance."""
    from arcade.sdk import ToolContext
    return ToolContext()
