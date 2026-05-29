import re
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi


def get_youtube_metadata(url):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            return {
                "title": info.get("title"),
                "creator": info.get("uploader"),
                "views": info.get("view_count"),
                "likes": info.get("like_count"),
                "comments": info.get("comment_count"),
                "duration": info.get("duration"),
                "upload_date": info.get("upload_date"),
                "thumbnail": info.get("thumbnail")
            }

    except Exception as e:
        return {
            "error": str(e)
        }


def extract_video_id(url):
    patterns = [
        r"v=([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})"
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def get_youtube_transcript(url):
    video_id = extract_video_id(url)

    if not video_id:
        return "Could not extract video ID"

    try:
        api = YouTubeTranscriptApi()

        transcript = api.fetch(video_id)

        full_text = " ".join(
            [snippet.text for snippet in transcript]
        )

        return full_text

    except Exception as e:
        return f"Transcript Error: {str(e)}"