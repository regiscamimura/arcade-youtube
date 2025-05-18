import re

from arcade_youtube.tools.constants import (
    RESOURCE_ID_PATH,
    SNIPPET_PATH,
)


def format_activity(activity: dict) -> dict:
    """Format a YouTube activity into a standardized structure."""
    snippet = activity.get("snippet", {})
    content_details = activity.get("contentDetails", {})

    # Extract video ID from either watch or playlistItem
    video_id = None
    if "watch" in content_details:
        video_id = content_details["watch"].get("videoId")
    elif "playlistItem" in content_details:
        video_id = content_details["playlistItem"].get("resourceId", {}).get("videoId")

    return {
        "title": snippet.get("title", ""),
        "video_id": video_id,
        "published_at": snippet.get("publishedAt", ""),
        "channel_title": snippet.get("channelTitle", ""),
        "description": snippet.get("description", ""),
    }


def format_subscription(subscription: dict) -> dict:
    """Format subscription data into a clean structure."""
    return {
        "channel_title": subscription.get(SNIPPET_PATH, {}).get("title"),
        "channel_id": subscription.get(SNIPPET_PATH, {}).get(RESOURCE_ID_PATH, {}).get("channelId"),
        "subscribed_at": subscription.get(SNIPPET_PATH, {}).get("publishedAt"),
    }


def parse_duration(duration: str) -> int:
    """Parse ISO 8601 duration into seconds."""
    match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration)
    if match:
        hours, minutes, seconds = (int(x) if x else 0 for x in match.groups())
        return hours * 3600 + minutes * 60 + seconds
    return 0
