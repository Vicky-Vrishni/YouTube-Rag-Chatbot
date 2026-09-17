from transcript_extractor import get_transcript
from chunking import chunk_transcript
from embeddings import get_embedding_model


if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=Gfr50f6ZBvo"

    text, raw_data, video_id = get_transcript(video_url)
    chunks = chunk_transcript(text)

    print("Video ID:", video_id)
    print("Total chunks created:", len(chunks))
    print("=" * 50)

    model = get_embedding_model()
    vectors = model.embed_documents(chunks)

    for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
        print(f"Chunk {i + 1}:")
        print("Text preview:", chunk[:200])
        print("Vector length:", len(vector))
        print(vector[167])
        print("-" * 50)


