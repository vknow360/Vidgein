from http.client import HTTPException
from urllib.parse import urlparse
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
    CouldNotRetrieveTranscript,
)

ytt_api = YouTubeTranscriptApi()

def extract_video_id(url: str) -> str:
    """
    Handles:
    - https://www.youtube.com/watch?v=dQw4w9WgXcQ
    - https://youtu.be/dQw4w9WgXcQ
    - https://www.youtube.com/embed/dQw4w9WgXcQ
    - https://youtube.com/watch?v=dQw4w9WgXcQ&t=120
    """
    parsed = urlparse(url)
    if parsed is None or parsed.hostname is None:
        raise ValueError("Invalid URL")

    if parsed.hostname in ("youtu.be"):
        return parsed.path.lstrip("/")
    
    if parsed.hostname in ("youtube.com", "www.youtube.com", "m.youtube.com"):
        query = parsed.query
        if query and "v=" in query:
            return query.split("v=")[1]
        elif parsed.path.startswith("/embed"):
            return parsed.path.split("/")[-1]
    
    raise ValueError("Invalid URL")
    

def get_transcript(video_id: str):
    try:
        vid_transcript = ytt_api.fetch(video_id=video_id)
        return vid_transcript.to_raw_data()
    except TranscriptsDisabled:
        # Video owner disabled transcripts
        raise HTTPException(400, "Transcripts are disabled for this video")
    except NoTranscriptFound:
        # No transcript in any language
        raise HTTPException(400, "No transcript found for this video")
    except CouldNotRetrieveTranscript as e:
        # Catch-all for other transcript errors
        raise HTTPException(400, f"Could not retrieve transcript: {e}")
