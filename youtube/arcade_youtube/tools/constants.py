"""Constants for the YouTube toolkit."""

# API Configuration
YOUTUBE_API_BASE_URL = "https://www.googleapis.com/youtube/v3"
DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 50

# Default limits for tool functions
DEFAULT_WATCH_HISTORY_LIMIT = 5
DEFAULT_SUBSCRIPTIONS_LIMIT = 5

# API Endpoints
ACTIVITIES_ENDPOINT = "/activities"
SUBSCRIPTIONS_ENDPOINT = "/subscriptions"
VIDEOS_ENDPOINT = "/videos"

# Required OAuth scopes
YOUTUBE_READONLY_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"

# Response field paths
SNIPPET_PATH = "snippet"
CONTENT_DETAILS_PATH = "contentDetails"
WATCH_PATH = "watch"
RESOURCE_ID_PATH = "resourceId"
