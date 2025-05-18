import logging
from typing import Annotated

from arcade.sdk import ToolContext, tool
from arcade.sdk.auth import Google
from google.oauth2.credentials import Credentials

from arcade_youtube.core.backend import YouTubeBackend
from arcade_youtube.tools.constants import (
    CONTENT_DETAILS_PATH,
    WATCH_PATH,
    YOUTUBE_READONLY_SCOPE,
)
from arcade_youtube.tools.utils import format_activity, format_subscription, parse_duration

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@tool(requires_auth=Google(scopes=[YOUTUBE_READONLY_SCOPE]))
async def get_watch_history(
    context: ToolContext,
    credentials: Annotated[Credentials, "OAuth credentials for YouTube API"],
    limit: Annotated[int, "Number of history items to return"] = 5,
) -> list[dict]:
    """Get recent watch history."""
    backend = YouTubeBackend(credentials)
    activities = backend.fetch_activities(max_results=limit)
    logger.debug(f"Raw activities from API: {activities}")

    # Process both watch and playlistItem activities
    watch_activities = []
    for activity in activities:
        content_details = activity.get(CONTENT_DETAILS_PATH, {})
        # Check for watch activity
        watch_video_id = content_details.get(WATCH_PATH, {}).get("videoId")
        playlist_video_id = content_details.get("playlistItem", {}) \
            .get("resourceId", {}) \
            .get("videoId")
        if watch_video_id or playlist_video_id:
            watch_activities.append(activity)

    logger.debug(f"Filtered watch activities: {watch_activities}")

    formatted = [format_activity(a) for a in watch_activities]
    logger.debug(f"Formatted activities: {formatted}")
    return formatted


@tool(requires_auth=Google(scopes=[YOUTUBE_READONLY_SCOPE]))
async def get_subscriptions(
    context: ToolContext,
    credentials: Annotated[Credentials, "OAuth credentials for YouTube API"],
    limit: Annotated[int, "Number of subscriptions to return"] = 5,
) -> list[dict]:
    """Get recent channel subscriptions."""

    backend = YouTubeBackend(credentials)
    subscriptions = backend.fetch_subscriptions(max_results=limit)
    return list(map(format_subscription, subscriptions))


@tool(requires_auth=Google(scopes=[YOUTUBE_READONLY_SCOPE]))
async def get_watch_time_stats(
    context: ToolContext,
    credentials: Annotated[Credentials, "OAuth credentials for YouTube API"],
) -> dict:
    """Get watch time statistics."""

    backend = YouTubeBackend(credentials)
    activities = backend.fetch_activities()

    durations = []
    for activity in activities:
        content_details = activity.get(CONTENT_DETAILS_PATH, {})
        watch_info = content_details.get(WATCH_PATH, {})
        video_id = watch_info.get("videoId")

        if not video_id:
            continue

        video = backend.fetch_video_details(video_id)
        if not video:
            continue

        video_content = video.get(CONTENT_DETAILS_PATH, {})
        duration = video_content.get("duration", "PT0S")
        seconds = parse_duration(duration)

        if seconds:
            durations.append(seconds)

    total = sum(durations)
    count = len(durations)

    return {
        "total_seconds": total,
        "total_hours": round(total / 3600, 2),
        "video_count": count,
        "average_duration": round(total / count if count else 0, 2),
    }
