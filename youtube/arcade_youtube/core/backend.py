from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


class YouTubeBackend:
    """Low-level YouTube API interactions."""

    def __init__(self, credentials: Credentials):
        self.youtube = build('youtube', 'v3', credentials=credentials)

    def _execute_request(self, request):
        """Execute a YouTube API request."""
        # TODO: Add proper error handling
        return request.execute()

    def fetch_activities(self, max_results: int = 50) -> list[dict]:
        """Fetch user activities (watch history)."""
        request = self.youtube.activities().list(
            part="snippet,contentDetails",
            mine=True,
            maxResults=max_results
        )
        response = self._execute_request(request)
        return response.get('items', [])

    def fetch_subscriptions(self, max_results: int = 50) -> list[dict]:
        """Fetch user subscriptions."""
        request = self.youtube.subscriptions().list(
            part="snippet",
            mine=True,
            maxResults=max_results
        )
        response = self._execute_request(request)
        return response.get('items', [])

    def fetch_video_details(self, video_id: str) -> dict | None:
        """Fetch detailed information about a video."""
        request = self.youtube.videos().list(
            part="snippet,contentDetails",
            id=video_id
        )
        response = self._execute_request(request)
        return response.get('items', [{}])[0] if response.get('items') else None
