"""YouTube integration toolkit for Arcade."""

from arcade_youtube.tools.youtube_client import (
    get_subscriptions,
    get_watch_history,
    get_watch_time_stats,
)

__all__ = [
    'get_subscriptions',
    'get_watch_history',
    'get_watch_time_stats',
]
