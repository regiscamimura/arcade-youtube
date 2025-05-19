# YouTube Monitoring Dashboard

A sample application demonstrating how to use the Arcade YouTube Toolkit to create a parental monitoring dashboard. This is an "almost agentic" application that provides insights into YouTube activity without taking autonomous actions.

## Features

- Educational content analysis
- Viewing pattern insights
- Channel subscription tracking
- Search activity monitoring

## Tech Stack

- FastAPI for the backend API
- Vue.js for the frontend interface
- Educational insights generation

## Setup

1. Make sure you have the main toolkit installed and configured (see main README)

2. Set up YouTube OAuth credentials:
   - Follow the detailed instructions in the [main README](../README.md#setting-up-your-environment-variables-)
   - For this app specifically, you'll need to set these environment variables:
     ```env
     YOUTUBE_TOKEN=your_token_here
     YOUTUBE_REFRESH_TOKEN=your_refresh_token_here
     YOUTUBE_TOKEN_URI=https://oauth2.googleapis.com/token
     YOUTUBE_CLIENT_ID=your_client_id_here
     YOUTUBE_CLIENT_SECRET=your_client_secret_here
     ```
   - You can generate these tokens using the `get_tokens.py` script in the toolkit:
     ```bash
     python get_tokens.py path/to/client_secrets.json
     ```

3. Set up Arcade.dev credentials:
   - Sign up or sign in to arcade.dev and grab an API key there. Add an ARCADE_API_KEY variable to the .env file, as shown in the .env.example. It's needed for using AI tools, and that's done with OpenAI but through Arcade.dev platform.

3. Start the dashboard:
```bash
# Using uvicorn (recommended)
uvicorn web_interface:app --reload

# Or using the Python script
python web_interface.py
```

4. Access the dashboard at `http://localhost:8000`

## API Documentation

The API documentation is automatically generated and available in two formats:

1. **Swagger UI** - Interactive API documentation with testing capabilities
   - Access at: `http://localhost:8000/docs`
   - Features:
     - Interactive API testing
     - Request/response examples
     - Schema validation
     - Authentication details

2. **ReDoc** - Beautiful, responsive API documentation
   - Access at: `http://localhost:8000/redoc`
   - Features:
     - Clean, modern interface
     - Detailed schema information
     - Search functionality
     - Mobile-friendly design

The documentation is generated from the code using FastAPI's built-in OpenAPI support, ensuring it's always up-to-date with the actual implementation.

### Endpoints

#### GET `/api/analyze-latest`
Analyzes the educational value of the most recently watched YouTube video using AI.

**Response:**
```json
{
  "video_id": "string",
  "title": "string",
  "published_at": "datetime",
  "description": "string",
  "channel": "string",
  "ai_analysis": {
    "educational_score": "number (0-10)",
    "topics": ["array of strings"],
    "age_appropriateness": "Young Children | Teens | Adults | All Ages",
    "learning_potential": "High | Medium | Low",
    "concerns": ["array of strings"],
    "explanation": "string"
  }
}
```

**Error Responses:**
- `400 Bad Request`: If no watch history is found
- `500 Internal Server Error`: For other server errors

**Authentication:**
Requires YouTube OAuth credentials configured via environment variables:
- `YOUTUBE_TOKEN`
- `YOUTUBE_REFRESH_TOKEN`
- `YOUTUBE_TOKEN_URI`
- `YOUTUBE_CLIENT_ID`
- `YOUTUBE_CLIENT_SECRET`

## Development

### Project Structure

- `templates/` - Vue.js templates and components
- `web_interface.py` - FastAPI application
- `content_monitor.py` - Content analysis logic

### Adding Features

When adding new features:
1. Update the FastAPI endpoints in `web_interface.py`
2. Add corresponding Vue.js components
3. Implement content analysis in `content_monitor.py`

## Future Enhancements

- AI-powered content recommendations
- Automatic educational video suggestions
- Smart notifications for concerning content
- Integration with other parental control tools

## License

MIT License - see the main [LICENSE](../LICENSE) file for details.
