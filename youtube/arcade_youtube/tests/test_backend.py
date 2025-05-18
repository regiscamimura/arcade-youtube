import os
import unittest
import vcr
from google.oauth2.credentials import Credentials
from ..core.backend import YouTubeBackend

# Configure VCR
my_vcr = vcr.VCR(
    cassette_library_dir='fixtures/cassettes',
    record_mode='once',
    match_on=['uri', 'method'],
    filter_headers=['Authorization'],  # Don't record auth headers
    decode_compressed_response=True
)

class TestYouTubeBackend(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures before running any tests."""
        # Create test credentials from environment variables
        cls.credentials = Credentials(
            token=os.getenv('YOUTUBE_TEST_TOKEN'),
            refresh_token=os.getenv('YOUTUBE_TEST_REFRESH_TOKEN'),
            token_uri=os.getenv('YOUTUBE_TEST_TOKEN_URI', 'https://oauth2.googleapis.com/token'),
            client_id=os.getenv('YOUTUBE_TEST_CLIENT_ID'),
            client_secret=os.getenv('YOUTUBE_TEST_CLIENT_SECRET'),
            scopes=['https://www.googleapis.com/auth/youtube.readonly']
        )

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.backend = YouTubeBackend(self.credentials)

    @my_vcr.use_cassette('test_fetch_activities.yaml')
    def test_fetch_activities(self):
        """Test fetching activities using recorded API responses."""
        result = self.backend.fetch_activities(max_results=10)
        
        # Verify the result structure
        self.assertIsInstance(result, list)
        if result:  # If we have any activities
            activity = result[0]
            self.assertIn('snippet', activity)
            self.assertIn('contentDetails', activity)
            self.assertIn('watch', activity['contentDetails'])

    @my_vcr.use_cassette('test_fetch_subscriptions.yaml')
    def test_fetch_subscriptions(self):
        """Test fetching subscriptions using recorded API responses."""
        result = self.backend.fetch_subscriptions(max_results=5)
        
        # Verify the result structure
        self.assertIsInstance(result, list)
        if result:  # If we have any subscriptions
            subscription = result[0]
            self.assertIn('snippet', subscription)
            self.assertIn('resourceId', subscription['snippet'])
            self.assertIn('channelId', subscription['snippet']['resourceId'])

    @my_vcr.use_cassette('test_fetch_video_details.yaml')
    def test_fetch_video_details(self):
        """Test fetching video details using recorded API responses."""
        # Using a known video ID (e.g., a popular video that's unlikely to be deleted)
        video_id = 'dQw4w9WgXcQ'  # Example video ID
        result = self.backend.fetch_video_details(video_id)
        
        # Verify the result structure
        self.assertIsNotNone(result)
        self.assertIn('snippet', result)
        self.assertIn('contentDetails', result)
        self.assertEqual(result['id'], video_id)

    @my_vcr.use_cassette('test_fetch_video_details_not_found.yaml')
    def test_fetch_video_details_not_found(self):
        """Test fetching video details for a non-existent video."""
        # Using an obviously fake video ID
        video_id = 'nonexistent_video_id_123456789'
        result = self.backend.fetch_video_details(video_id)
        
        # Verify the result
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main() 