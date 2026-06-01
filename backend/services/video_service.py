from services.youtube_service import (
    get_youtube_metadata,
    get_youtube_transcript
)

from services.instagram_service import (
    get_instagram_metadata,
    get_instagram_transcript
)


def get_metadata(url):

    if "instagram.com" in url.lower():

        return get_instagram_metadata(
            url
        )

    return get_youtube_metadata(
        url
    )


def get_transcript(url):

    if "instagram.com" in url.lower():

        return get_instagram_transcript(
            url
        )

    return get_youtube_transcript(
        url
    )