import re
import os
import uuid
import yt_dlp
import whisper

from youtube_transcript_api import (
    YouTubeTranscriptApi
)


def get_youtube_metadata(url):

    try:

        ydl_opts = {
            "quiet": True,
            "skip_download": True
        }

        with yt_dlp.YoutubeDL(
            ydl_opts
        ) as ydl:

            info = ydl.extract_info(
                url,
                download=False
            )

            return {
                "title": info.get("title"),
                "creator": info.get("uploader"),
                "views": info.get("view_count"),
                "likes": info.get("like_count"),
                "comments": info.get("comment_count"),
                "duration": info.get("duration"),
                "upload_date": info.get("upload_date"),
                "thumbnail": info.get("thumbnail"),

                "followers": info.get(
                    "channel_follower_count"
                ),

                "hashtags": info.get(
                    "tags",
                    []
                )
            }

    except Exception as e:

        return {
            "error": str(e)
        }


def extract_video_id(url):

    patterns = [
        r"v=([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
        r"shorts/([a-zA-Z0-9_-]{11})",
        r"embed/([a-zA-Z0-9_-]{11})"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            url
        )

        if match:
            return match.group(1)

    return None


def get_youtube_transcript_whisper(url):

    try:

        output_file = (
            f"youtube_{uuid.uuid4()}"
        )

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": output_file
        }

        with yt_dlp.YoutubeDL(
            ydl_opts
        ) as ydl:

            ydl.download([url])

        audio_file = None

        for file in os.listdir("."):

            if file.startswith(
                output_file
            ):
                audio_file = file
                break

        if not audio_file:

            return (
                "Transcript Error: "
                "Audio download failed"
            )

        model = whisper.load_model(
            "base"
        )

        result = model.transcribe(
            audio_file
        )
        try:
            os.remove(audio_file)
        except:
            pass

        return result["text"]

    except Exception as e:

        return (
            f"Transcript Error: {str(e)}"
        )


def get_youtube_transcript(url):

    video_id = extract_video_id(
        url
    )

    if not video_id:

        return (
            "Could not extract video ID"
        )

    try:

        api = YouTubeTranscriptApi()

        transcript = api.fetch(
            video_id
        )

        full_text = " ".join(
            [
                snippet.text
                for snippet in transcript
            ]
        )

        return full_text

    except Exception as e:

        print(
            "\nYOUTUBE TRANSCRIPT ERROR:"
        )

        print(
            type(e).__name__
        )

        print(
            str(e)
        )

        print(
            "\nTrying Whisper fallback..."
        )

        return (
            get_youtube_transcript_whisper(
                url
            )
        )