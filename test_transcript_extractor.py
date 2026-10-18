
import pytest
from unittest.mock import Mock, patch

from src.transcript_extractor import (
    extract_video_id,
    get_transcript,
    InvalidVideoError,
    TranscriptUnavailableError,
    TranscriptExtractionError,
)


def test_extract_video_id_from_watch_url():
    video_id = "abcdefghijk"

    result = extract_video_id(
        f"https://www.youtube.com/watch?v={video_id}"
    )

    assert result == video_id


def test_extract_video_id_from_short_url():
    video_id = "abcdefghijk"

    result = extract_video_id(
        f"https://youtu.be/{video_id}"
    )

    assert result == video_id


def test_extract_video_id_from_raw_id():
    assert extract_video_id("abcdefghijk") == "abcdefghijk"


@pytest.mark.parametrize("invalid_input", ["", "   ", "not-a-valid-url", None])
def test_invalid_video_input_raises_error(invalid_input):
    with pytest.raises(InvalidVideoError):
        extract_video_id(invalid_input)


@patch("src.transcript_extractor.YouTubeTranscriptApi")
def test_get_transcript_success(mock_api_class):
    video_id = "abcdefghijk"
    segments = [
        {"text": "Hello", "start": 0.0, "duration": 1.0},
        {"text": "world", "start": 1.0, "duration": 1.0},
    ]

    mock_transcript = Mock()
    mock_transcript.to_raw_data.return_value = segments
    mock_api_class.return_value.fetch.return_value = mock_transcript

    text, returned_segments, returned_id = get_transcript(video_id)

    assert text == "Hello world"
    assert returned_segments == segments
    assert returned_id == video_id
    mock_api_class.return_value.fetch.assert_called_once_with(
        video_id,
        languages=["en", "hi"],
    )


@patch("src.transcript_extractor.YouTubeTranscriptApi")
def test_empty_transcript_raises_unavailable_error(mock_api_class):
    mock_transcript = Mock()
    mock_transcript.to_raw_data.return_value = []
    mock_api_class.return_value.fetch.return_value = mock_transcript

    with pytest.raises(TranscriptUnavailableError):
        get_transcript("abcdefghijk")


@patch("src.transcript_extractor.YouTubeTranscriptApi")
def test_unexpected_api_error_is_wrapped(mock_api_class):
    mock_api_class.return_value.fetch.side_effect = RuntimeError(
        "Network failure"
    )

    with pytest.raises(TranscriptExtractionError):
        get_transcript("abcdefghijk")
