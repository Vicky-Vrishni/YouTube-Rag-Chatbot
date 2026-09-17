from youtube_transcript_api import YouTubeTranscriptApi
import re


def extract_video_id(url_or_id: str) -> str:
    
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'youtu\.be\/([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)

    if len(url_or_id) == 11:
        return url_or_id

    raise ValueError("Please provide a valid YouTube URL or video ID.")


def get_transcript(video_url_or_id: str, languages=None):
    if languages is None:
        languages = ['en', 'hi']

    video_id = extract_video_id(video_url_or_id)

    try:
        api = YouTubeTranscriptApi()
        fetched_transcript = api.fetch(video_id, languages=languages)
    except Exception as e:
        raise Exception(f"Failed to fetch transcript: {e}")

    raw_data = fetched_transcript.to_raw_data()
    full_text = " ".join(segment["text"] for segment in raw_data)

    return full_text, raw_data, video_id


if __name__ == "__main__":
    sample_url = "https://www.youtube.com/watch?v=Gfr50f6ZBvo"
    text, raw_data, video_id = get_transcript(sample_url)
    print("Video ID:", video_id)
    print("Total segments fetched:", len(raw_data))
    print("Last segment start time (seconds):", raw_data[-1]["start"])
    print("Total transcript character count:", len(text))
    
    print(text)