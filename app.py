from fastapi import FastAPI, HTTPException, Query
from youtube_transcript_api import YouTubeTranscriptApi
from fastapi.responses import JSONResponse

# Create FastAPI app
app = FastAPI(title="YouTube Transcript API", description="Fetch YouTube video captions via API", version="1.0")

@app.get("/get_captions", summary="Fetch captions for a YouTube video")
async def get_captions(video_id: str = Query(..., description="The YouTube video ID to fetch captions for")):
    """
    Fetch captions for the given YouTube video ID and return them as a single string.
    """
    try:
        # Fetch transcript from YouTube
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])

        # Combine transcript lines into a single string
        combined_transcript = " ".join([line["text"] for line in transcript])

        # Return JSON response
        return JSONResponse({"video_id": video_id, "captions": combined_transcript})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@app.get("/", summary="Health check")
async def root():
    """
    Health check endpoint for testing the service.
    """
    return {"message": "Welcome to the YouTube Transcript API"}
