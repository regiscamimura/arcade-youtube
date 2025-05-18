import json
import logging
import os
from typing import Annotated, Any

from google.oauth2.credentials import Credentials
from openai import OpenAI

from arcade_youtube.tools.youtube_client import get_watch_history

# Configure logging to only show WARNING and above
logging.getLogger().setLevel(logging.WARNING)
logging.getLogger("googleapiclient").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

async def analyze_latest_video(
    credentials: Annotated[Credentials, "OAuth credentials for YouTube API"],
) -> Annotated[dict[str, Any], "Analysis results including video details and AI assessment"]:
    """Analyze the educational value of the most recently watched video using AI."""

    history = await get_watch_history(None, credentials=credentials, limit=1)

    if not history:
        return {"error": "No watch history found"}

    video = history[0]

    prompt = f"""Based on the text content from a video, analyze its educational value:

Title: {video['title']}
Channel: {video['channel_title']}
Description: {video.get('description', '')}

Please analyze this content and provide:
1. Educational value (score 0-10)
2. Main topics/subjects covered
3. Age appropriateness
4. Learning potential
5. Any potential concerns

Important considerations for board games and educational content:
- Board games often teach multiple subjects simultaneously
  (e.g., mythology, history, strategy, critical thinking)
- They can develop various skills (problem-solving, decision-making, social interaction)
- Even entertainment-focused games can have significant educational value
- Consider both direct educational content (e.g., historical facts) and indirect learning
  (e.g., strategic thinking)

Format the response as a JSON object with these fields:
- educational_score (number 0-10)
- topics (array of strings, include both primary and secondary topics)
- age_appropriateness (string: "Young Children", "Teens", "Adults", or "All Ages")
- learning_potential (string: "High", "Medium", or "Low")
- concerns (array of strings, empty if none)
- explanation (string explaining the score and analysis, including both direct and indirect
  educational benefits)

Note: You are analyzing the provided text content only, not watching any video."""

    # Initialize OpenAI client with Arcade configuration
    arcade_api_key = os.environ.get("ARCADE_API_KEY")
    cloud_host = "https://api.arcade.dev/v1"

    client = OpenAI(
        api_key=arcade_api_key,
        base_url=cloud_host,
    )

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert in educational content analysis, with deep knowledge of "
                    "how games and interactive content can provide educational value. Consider "
                    "both direct educational content and indirect learning benefits "
                    "when analyzing content."
                )
            },
            {"role": "user", "content": prompt}
        ],
        model="gpt-4",
        temperature=0.3
    )

    # Extract JSON from markdown code block if present
    content = response.choices[0].message.content
    if "```json" in content:
        # Find the JSON block between ```json and ```
        json_start = content.find("```json") + 7
        json_end = content.find("```", json_start)
        content = content[json_start:json_end].strip()

    # Parse the JSON content
    analysis = json.loads(content)

    data = {
        "video_id": video["video_id"],
        "title": video["title"],
        "published_at": video["published_at"],
        "description": video["description"],
        "channel": video["channel_title"],
        "ai_analysis": analysis
    }

    return data
