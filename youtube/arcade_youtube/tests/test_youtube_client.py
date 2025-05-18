from pathlib import Path

import pytest
import vcr

from arcade_youtube.tools.youtube_client import (
    get_subscriptions,
    get_watch_history,
    get_watch_time_stats,
)

# Configure VCR
my_vcr = vcr.VCR(
    cassette_library_dir=str(Path(__file__).parent / "fixtures" / "cassettes"),
    record_mode="once",
    match_on=["uri", "method"],
    filter_headers=["Authorization"],
    filter_query_parameters=[
        "client_id",
        "client_secret",
        "refresh_token",
        "access_token",
    ],
    filter_post_data_parameters=[
        "client_id",
        "client_secret",
        "refresh_token",
        "access_token",
    ],
)

@pytest.mark.asyncio
@my_vcr.use_cassette("test_get_watch_history.yaml")
async def test_get_watch_history(context, credentials):
    result = await get_watch_history(context, credentials=credentials, limit=5)
    assert isinstance(result, list)
    if result:
        item = result[0]
        assert "title" in item
        assert "video_id" in item
        assert "published_at" in item
        assert "channel_title" in item
        assert item["video_id"] is not None

@pytest.mark.asyncio
@my_vcr.use_cassette("test_get_subscriptions.yaml")
async def test_get_subscriptions(context, credentials):
    result = await get_subscriptions(context, credentials=credentials, limit=5)
    assert isinstance(result, list)
    if result:
        subscription = result[0]
        assert "channel_title" in subscription
        assert "channel_id" in subscription
        assert "subscribed_at" in subscription

@pytest.mark.asyncio
@my_vcr.use_cassette("test_get_watch_time_stats.yaml")
async def test_get_watch_time_stats(context, credentials):
    result = await get_watch_time_stats(context, credentials=credentials)
    assert isinstance(result, dict)
    assert "total_seconds" in result
    assert "total_hours" in result
    assert "video_count" in result
    assert "average_duration" in result
    assert result["total_seconds"] >= 0
    assert result["total_hours"] >= 0
    assert result["video_count"] >= 0
    assert result["average_duration"] >= 0


