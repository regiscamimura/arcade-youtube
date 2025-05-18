from typing import Annotated

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from .constants import DEFAULT_MAX_RESULTS


class YouTubeBackend:
    """Low-level YouTube API interactions."""

    def __init__(self, credentials: Annotated[Credentials, "OAuth credentials for YouTube API"]):
        """Initialize the backend.
        Args: credentials: A Credentials object for OAuth authentication"""
        try:
            self.youtube = build("youtube", "v3", credentials=credentials)
        except Exception as e:
            if "API has not been used" in str(e):
                raise Exception("YouTube API is not enabled in your Google Cloud project. Please enable it at https://console.cloud.google.com/apis/library/youtube.googleapis.com")
            raise

    def _execute_request(self, request):
        """Execute a YouTube API request."""
        # TODO: Add proper error handling
        return request.execute()

    def fetch_activities(
        self,
        max_results: Annotated[int, "Maximum number of activities to fetch"] = DEFAULT_MAX_RESULTS,
    ) -> list[dict]:
        """Fetch user activities (watch history)."""
        request = self.youtube.activities().list(
            part="snippet,contentDetails", mine=True, maxResults=max_results
        )
        response = self._execute_request(request)
        return response.get("items", [])

    def fetch_subscriptions(
        self,
        max_results: Annotated[
            int, "Maximum number of subscriptions to fetch"
        ] = DEFAULT_MAX_RESULTS,
    ) -> list[dict]:
        """Fetch user subscriptions."""
        request = self.youtube.subscriptions().list(
            part="snippet", mine=True, maxResults=max_results
        )
        response = self._execute_request(request)
        return response.get("items", [])

    def fetch_video_details(self, video_id: Annotated[str, "YouTube video ID"]) -> dict | None:
        """Fetch detailed information about a video."""
        request = self.youtube.videos().list(part="snippet,contentDetails", id=video_id)
        response = self._execute_request(request)
        return response.get("items", [{}])[0] if response.get("items") else None
