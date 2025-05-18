from typing import Annotated

from arcade.sdk import ToolContext, tool
from arcade.sdk.auth import Google

from arcade_youtube.core.backend import YouTubeBackend
from arcade_youtube.tools.constants import (
    CONTENT_DETAILS_PATH,
    WATCH_PATH,
    YOUTUBE_READONLY_SCOPE,
)
from arcade_youtube.tools.utils import format_activity, format_subscription, parse_duration


@tool(requires_auth=Google(scopes=[YOUTUBE_READONLY_SCOPE]))
async def get_watch_history(
    context: ToolContext,
    limit: Annotated[int, "Number of history items to return"] = 5,
) -> list[dict]:
    """Get recent watch history."""

    backend = YouTubeBackend(context.credentials)
    activities = backend.fetch_activities(max_results=limit)
    return list(map(format_activity, activities))


@tool(requires_auth=Google(scopes=[YOUTUBE_READONLY_SCOPE]))
async def get_subscriptions(
    context: ToolContext,
    limit: Annotated[int, "Number of subscriptions to return"] = 5,
) -> list[dict]:
    """Get recent channel subscriptions."""

    backend = YouTubeBackend(context.credentials)
    subscriptions = backend.fetch_subscriptions(max_results=limit)
    return list(map(format_subscription, subscriptions))


@tool(requires_auth=Google(scopes=[YOUTUBE_READONLY_SCOPE]))
async def get_watch_time_stats(context: ToolContext) -> dict:
    """Get watch time statistics."""

    backend = YouTubeBackend(context.credentials)
    activities = backend.fetch_activities()

    durations = []
    for activity in activities:
        content_details = activity.get(CONTENT_DETAILS_PATH, {})
        watch_info = content_details.get(WATCH_PATH, {})
        video_id = watch_info.get('videoId')

        if not video_id:
            continue

        video = backend.fetch_video_details(video_id)
        if not video:
            continue

        video_content = video.get(CONTENT_DETAILS_PATH, {})
        duration = video_content.get('duration', 'PT0S')
        seconds = parse_duration(duration)

        if seconds:
            durations.append(seconds)

    total = sum(durations)
    count = len(durations)

    return {
        "total_seconds": total,
        "total_hours": round(total / 3600, 2),
        "video_count": count,
        "average_duration": round(total / count if count else 0, 2)
    }
