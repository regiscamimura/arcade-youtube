import re

from arcade_youtube.tools.constants import (
    CONTENT_DETAILS_PATH,
    RESOURCE_ID_PATH,
    SNIPPET_PATH,
    WATCH_PATH,
)


def format_activity(activity: dict) -> dict:
    """Format activity data into a clean structure."""
    return {
        "title": activity.get(SNIPPET_PATH, {}).get('title'),
        "video_id": activity.get(CONTENT_DETAILS_PATH, {}).get(WATCH_PATH, {}).get('videoId'),
        "published_at": activity.get(SNIPPET_PATH, {}).get('publishedAt'),
        "channel_title": activity.get(SNIPPET_PATH, {}).get('channelTitle')
    }

def format_subscription(subscription: dict) -> dict:
    """Format subscription data into a clean structure."""
    return {
        "channel_title": subscription.get(SNIPPET_PATH, {}).get('title'),
        "channel_id": subscription.get(SNIPPET_PATH, {}).get(RESOURCE_ID_PATH, {}).get('channelId'),
        "subscribed_at": subscription.get(SNIPPET_PATH, {}).get('publishedAt')
    }

def parse_duration(duration: str) -> int:
    """Parse ISO 8601 duration into seconds."""
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
    if match:
        hours, minutes, seconds = (int(x) if x else 0 for x in match.groups())
        return hours * 3600 + minutes * 60 + seconds
    return 0
