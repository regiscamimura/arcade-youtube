# Arcade YouTube Toolkit

The core toolkit for tracking and analyzing YouTube activity. This package provides the building blocks for creating YouTube monitoring applications.

## Directory Structure

- `core/` - Backend implementation details (you probably don't need to look here)
- `tools/` - The main interface for developers. Contains:
  - YouTube API clients
  - Helper functions and utilities
  - All the good stuff you'll actually use

> 💡 **Developer Tip**: Focus on the `tools` directory - that's where all the developer-friendly interfaces live. The `core` directory contains implementation details that you typically won't need to interact with directly.

## Features

- Track YouTube watch history and viewing patterns
- Monitor subscriptions and channel preferences
- Analyze search activity and content interests
- Educational content analysis and categorization

## API Reference

### YouTubeTracker

The main class for tracking YouTube activity.

```python
tracker = YouTubeTracker()
```

#### Methods

- `start_monitoring()` - Begin tracking YouTube activity
- `get_watch_history()` - Retrieve watch history
- `get_subscriptions()` - Get channel subscriptions
- `get_search_history()` - Access search history
- `analyze_content(video_id)` - Analyze video content

### YouTube Client Methods

The toolkit provides several methods for interacting with YouTube data:

- `get_watch_history(credentials, limit=5)`: Retrieves recent watch history, including both direct video watches and playlist views. Returns a list of formatted activity records.
- `get_subscriptions(credentials, limit=5)`: Fetches recent channel subscriptions, returning a formatted list of subscribed channels.
- `get_watch_time_stats(credentials)`: Calculates detailed watch time statistics, including total watch time in seconds and hours, video count, and average video duration.

All methods require Google OAuth credentials with the YouTube read-only scope.

## Development

### Testing

The toolkit uses vcrpy for testing. See the main README for details on our testing approach.

### Contributing

When adding new features:
1. Add tests using vcrpy
2. Update the API documentation
3. Follow the existing code style
