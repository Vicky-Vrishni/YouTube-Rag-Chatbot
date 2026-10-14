
import re

from youtube_transcript_api import (
    YouTubeTranscriptApi,
    YouTubeTranscriptDisabled,
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)


class TranscriptExtractionError(Exception):
    """Base exception for transcript extraction failures."""


class InvalidVideoError(TranscriptExtractionError):
    """Raised when the YouTube URL or video ID is invalid."""


class TranscriptUnavailableError(TranscriptExtractionError):
    """Raised when the video transcript cannot be retrieved."""


def extract_video_id(url_or_id: str) -> str:
    """Extract and validate an 11-character YouTube video ID."""

    if not isinstance(url_or_id, str) or not url_or_id.strip():
        raise InvalidVideoError(
            "Please provide a valid YouTube URL or video ID."
        )

    value = url_or_id.strip()

    patterns = [
        r"(?:v=|/)([0-9A-Za-z_-]{11})(?:[?&#/]|$)",
        r"youtu\.be/([0-9A-Za-z_-]{11})(?:[?&#/]|$)",
    ]

    for pattern in patterns:
        match = re.search(pattern, value)

        if match:
            return match.group(1)

    if re.fullmatch(r"[0-9A-Za-z_-]{11}", value):
        return value

    raise InvalidVideoError(
        "Please provide a valid YouTube URL or video ID."
    )


def get_transcript(video_url_or_id: str, languages=None):
    """Fetch a transcript and return text, segments, and video ID."""

    video_id = extract_video_id(video_url_or_id)

    if languages is None:
        languages = ["en", "hi"]

    try:
        api = YouTubeTranscriptApi()
        fetched_transcript = api.fetch(
            video_id,
            languages=languages,
        )
        raw_data = fetched_transcript.to_raw_data()

        if not raw_data:
            raise TranscriptUnavailableError(
                "The video transcript is empty."
            )

        full_text = " ".join(
            segment["text"] for segment in raw_data
        )

        return full_text, raw_data, video_id

    except (
        YouTubeTranscriptDisabled,
        TranscriptsDisabled,
        NoTranscriptFound,
        VideoUnavailable,
    ) as error:
        raise TranscriptUnavailableError(
            "A transcript is unavailable for this video. "
            "Check whether captions are enabled and accessible."
        ) from error

    except TranscriptExtractionError:
        raise

    except Exception as error:
        raise TranscriptExtractionError(
            "Unable to fetch the transcript right now. "
            "Please try again later."
        ) from error
