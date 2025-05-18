import os
from pathlib import Path

import pytest
import vcr
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials

from arcade_youtube.core.backend import YouTubeBackend
from arcade_youtube.core.constants import YOUTUBE_READONLY_SCOPE

# Load environment variables from .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

# Configure VCR
my_vcr = vcr.VCR(
    cassette_library_dir=str(Path(__file__).parent / "fixtures" / "cassettes"),
    record_mode="once",
    match_on=["uri", "method"],
    filter_headers=["Authorization"],
)


@pytest.fixture
def credentials():
    """Provide OAuth credentials for testing."""
    creds = Credentials(
        token=os.getenv("YOUTUBE_TEST_TOKEN"),
        refresh_token=os.getenv("YOUTUBE_TEST_REFRESH_TOKEN"),
        token_uri=os.getenv("YOUTUBE_TEST_TOKEN_URI"),
        client_id=os.getenv("YOUTUBE_TEST_CLIENT_ID"),
        client_secret=os.getenv("YOUTUBE_TEST_CLIENT_SECRET"),
        scopes=[YOUTUBE_READONLY_SCOPE],
    )

    # If token is expired, refresh it and update env var
    if creds.expired:
        creds.refresh(None)
        os.environ["YOUTUBE_TEST_TOKEN"] = creds.token
    
    return creds


@pytest.fixture
def backend(credentials):
    """Provide a YouTubeBackend instance."""
    return YouTubeBackend(credentials)


@my_vcr.use_cassette("test_fetch_activities.yaml")
def test_fetch_activities(backend):
    """Test fetching activities using recorded API responses."""
    result = backend.fetch_activities(max_results=10)

    # Verify the result structure
    assert isinstance(result, list)
    if result:  # If we have any activities
        activity = result[0]
        assert "snippet" in activity
        assert "contentDetails" in activity
        assert "playlistItem" in activity["contentDetails"]
        assert "resourceId" in activity["contentDetails"]["playlistItem"]
        assert "videoId" in activity["contentDetails"]["playlistItem"]["resourceId"]


@my_vcr.use_cassette("test_fetch_subscriptions.yaml")
def test_fetch_subscriptions(backend):
    """Test fetching subscriptions using recorded API responses."""
    result = backend.fetch_subscriptions(max_results=5)

    # Verify the result structure
    assert isinstance(result, list)
    if result:  # If we have any subscriptions
        subscription = result[0]
        assert "snippet" in subscription
        assert "resourceId" in subscription["snippet"]
        assert "channelId" in subscription["snippet"]["resourceId"]


@my_vcr.use_cassette("test_fetch_video_details.yaml")
def test_fetch_video_details(backend):
    """Test fetching video details using recorded API responses."""
    # Using a known video ID (e.g., a popular video that's unlikely to be deleted)
    video_id = "dQw4w9WgXcQ"  # Example video ID
    result = backend.fetch_video_details(video_id)

    # Verify the result structure
    assert result is not None
    assert "snippet" in result
    assert "contentDetails" in result
    assert result["id"] == video_id


@my_vcr.use_cassette("test_fetch_video_details_not_found.yaml")
def test_fetch_video_details_not_found(backend):
    """Test fetching video details for a non-existent video."""
    # Using an obviously fake video ID
    video_id = "nonexistent_video_id_123456789"
    result = backend.fetch_video_details(video_id)

    # Verify the result
    assert result is None
