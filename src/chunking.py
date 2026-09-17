from langchain_text_splitters import RecursiveCharacterTextSplitter
from transcript_extractor import get_transcript


def chunk_transcript(full_text: str, chunk_size: int = 1000, chunk_overlap: int = 200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = splitter.split_text(full_text)
    return chunks


if __name__ == "__main__":
    text, raw_data, video_id = get_transcript("https://www.youtube.com/watch?v=Gfr50f6ZBvo")
    chunks = chunk_transcript(text)
    print("Total chunks:", len(chunks))
    print(chunks[100])
    