import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from google.oauth2.credentials import Credentials

from app.content_monitor import analyze_latest_video

# Load environment variables
load_dotenv()

app = FastAPI()


def get_credentials() -> Credentials:
    """Get credentials from environment variables."""
    return Credentials(
        token=os.getenv("YOUTUBE_TOKEN"),
        refresh_token=os.getenv("YOUTUBE_REFRESH_TOKEN"),
        token_uri=os.getenv("YOUTUBE_TOKEN_URI"),
        client_id=os.getenv("YOUTUBE_CLIENT_ID"),
        client_secret=os.getenv("YOUTUBE_CLIENT_SECRET"),
        scopes=["https://www.googleapis.com/auth/youtube.readonly"]
    )

@app.get("/", response_class=HTMLResponse)
async def home():
    with open("youtube/app/templates/index.html") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

def handle_error(error_msg: str, status_code: int = 400) -> None:
    """Raise HTTPException with the given error message and status code."""
    raise HTTPException(status_code=status_code, detail=error_msg)

@app.get("/api/analyze-latest")
async def analyze_latest():
    try:
        credentials = get_credentials()
        result = await analyze_latest_video(credentials)

        if "error" in result:
            handle_error(result["error"])

        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
