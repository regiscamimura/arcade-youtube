import os
from typing import Annotated, Any

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, JSONResponse
from google.oauth2.credentials import Credentials
from pydantic import BaseModel, Field

from app.content_monitor import analyze_latest_video
from arcade_youtube.tools.constants import YOUTUBE_READONLY_SCOPE

# Load environment variables
load_dotenv()

# Define response models
class AIAnalysis(BaseModel):
    educational_score: float = Field(..., ge=0, le=10, description="Educational value score from 0 to 10")
    topics: list[str] = Field(..., description="List of topics covered in the video")
    age_appropriateness: str = Field(..., description="Age group the content is appropriate for")
    learning_potential: str = Field(..., description="Potential for learning from the content")
    concerns: list[str] = Field(..., description="List of potential concerns")
    explanation: str = Field(..., description="Detailed explanation of the analysis")

class VideoAnalysis(BaseModel):
    video_id: str = Field(..., description="YouTube video ID")
    title: str = Field(..., description="Video title")
    published_at: str = Field(..., description="Publication date and time")
    description: str = Field(..., description="Video description")
    channel: str = Field(..., description="Channel name")
    ai_analysis: AIAnalysis = Field(..., description="AI-generated analysis of the video")

# Initialize FastAPI app with metadata
app = FastAPI(
    title="YouTube Content Monitor",
    description="A parental monitoring dashboard that provides insights into YouTube activity",
    version="1.0.0",
    docs_url=None,  # Disable default docs
    redoc_url=None,  # Disable default redoc
)

def get_credentials() -> Credentials:
    """Get credentials from environment variables."""
    return Credentials(
        token=os.getenv("YOUTUBE_TOKEN"),
        refresh_token=os.getenv("YOUTUBE_REFRESH_TOKEN"),
        token_uri=os.getenv("YOUTUBE_TOKEN_URI"),
        client_id=os.getenv("YOUTUBE_CLIENT_ID"),
        client_secret=os.getenv("YOUTUBE_CLIENT_SECRET"),
        scopes=[YOUTUBE_READONLY_SCOPE]
    )

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the main dashboard interface."""
    with open("youtube/app/templates/index.html") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

def handle_error(error_msg: str, status_code: int = 400) -> None:
    """Raise HTTPException with the given error message and status code."""
    raise HTTPException(status_code=status_code, detail=error_msg)

@app.get(
    "/api/analyze-latest",
    response_model=VideoAnalysis,
    responses={
        400: {"description": "No watch history found"},
        500: {"description": "Internal server error"}
    },
    summary="Analyze Latest Video",
    description="Analyzes the educational value of the most recently watched YouTube video using AI."
)
async def analyze_latest() -> Annotated[dict[str, Any], "Analysis results including video details and AI assessment"]:
    """Analyze the educational value of the most recently watched video."""
    try:
        credentials = get_credentials()
        result = await analyze_latest_video(credentials)

        if "error" in result:
            handle_error(result["error"])

        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

# Custom documentation endpoints
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css",
    )

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title=app.title + " - ReDoc",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
    )

@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_endpoint():
    return get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
