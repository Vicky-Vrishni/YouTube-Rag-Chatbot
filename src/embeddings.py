from langchain_huggingface import HuggingFaceEmbeddings


def get_embedding_model(model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        cache_folder="./model_cache"
    )
    return embeddings


if __name__ == "__main__":
    model = get_embedding_model()
    sample_text = "This is a test sentence."
    vector = model.embed_query(sample_text)
    print("Embedding vector length:", len(vector))
    print("First 5 values:", vector[:5])