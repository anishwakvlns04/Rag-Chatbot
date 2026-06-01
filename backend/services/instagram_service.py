import os
import yt_dlp
import whisper
import uuid

def get_instagram_metadata(url):

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
            print("\n===== INSTAGRAM INFO KEYS =====")
            print(info.keys())

            description = (
                info.get("description")
                or ""
            )

            hashtags = [
                word
                for word in description.split()
                if word.startswith("#")
            ]

            print("HASHTAGS:", hashtags)

            return {
                "title": info.get("title"),
                "creator": info.get("uploader"),
                "views": info.get("view_count"),
                "likes": info.get("like_count"),
                "comments": info.get("comment_count"),
                "duration": info.get("duration"),
                "upload_date": info.get("upload_date"),
                "thumbnail": info.get("thumbnail"),
                "hashtags": hashtags,
                "followers": None
            }

    except Exception as e:

        return {
            "error": str(e)
        }


def get_instagram_transcript(url):

    try:

        output_file = (
            f"instagram_{uuid.uuid4()}"
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

        return result["text"]

    except Exception as e:

        return (
            f"Transcript Error: {str(e)}"
        )