from typing import Annotated, Dict, Any
from arcade.sdk import ToolContext, tool
from arcade.sdk.auth import Google
from arcade_youtube.tools.youtube_client import get_watch_history
from arcade_youtube.core.backend import YouTubeBackend
import openai

@tool(requires_auth=Google())
async def analyze_latest_video(
    context: Annotated[ToolContext, "The tool context containing credentials"],
) -> Annotated[Dict[str, Any], "Analysis results including video details and AI assessment"]:
    """Analyze the educational value of the most recently watched video using AI."""
    history = await get_watch_history(context, limit=1)
    if not history:
        return {"error": "No watch history found"}
        
    video = history[0]
    backend = YouTubeBackend(context.credentials)
    video_details = backend.fetch_video_details(video["video_id"])
    
    if not video_details:
        return {"error": "Could not fetch video details"}
        
    snippet = video_details.get("snippet", {})
    title = snippet.get("title", "")
    description = snippet.get("description", "")
    channel = snippet.get("channelTitle", "")
    
    # Prepare prompt for AI analysis
    prompt = f"""Analyze this YouTube video for its educational value:

Title: {title}
Channel: {channel}
Description: {description}

Please analyze:
1. Educational value (score 0-10)
2. Main topics/subjects covered
3. Age appropriateness
4. Learning potential
5. Any potential concerns

Format the response as a JSON object with these fields:
- educational_score (number 0-10)
- topics (array of strings)
- age_appropriateness (string: "Young Children", "Teens", "Adults", or "All Ages")
- learning_potential (string: "High", "Medium", or "Low")
- concerns (array of strings, empty if none)
- explanation (string explaining the score and analysis)"""

    # Get AI analysis
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in educational content analysis. Analyze videos for their educational value and learning potential."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3  # Lower temperature for more consistent analysis
    )
    
    analysis = response.choices[0].message.content
    
    return {
        "video_id": video["video_id"],
        "title": title,
        "channel": channel,
        "ai_analysis": analysis
    } 