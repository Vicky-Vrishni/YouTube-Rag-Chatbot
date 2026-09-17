from langchain_chroma import Chroma
from embeddings import get_embedding_model


def create_vectorstore(chunks: list, video_id: str, persist_directory: str = "../chroma_db"):
    embeddings = get_embedding_model()

    metadatas = [{"video_id": video_id, "chunk_index": i} for i in range(len(chunks))]

    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory=persist_directory,
        collection_name=f"video_{video_id}"
    )
    return vectorstore


def load_vectorstore(video_id: str, persist_directory: str = "../chroma_db"):
    embeddings = get_embedding_model()

    vectorstore = Chroma(
        collection_name=f"video_{video_id}",
        embedding_function=embeddings,
        persist_directory=persist_directory
    )
    return vectorstore


if __name__ == "__main__":
    from transcript_extractor import get_transcript
    from chunking import chunk_transcript

    text, raw_data, video_id = get_transcript("https://www.youtube.com/watch?v=Gfr50f6ZBvo")
    chunks = chunk_transcript(text)

    vectorstore = create_vectorstore(chunks, video_id)
    print("Vectorstore created. Total chunks stored:", len(chunks))




    