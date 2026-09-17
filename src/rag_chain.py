import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate
from vectorstore import load_vectorstore

load_dotenv()

PROMPT_TEMPLATE = """You are a helpful assistant that answers questions based only on the provided video transcript context.

Context from the video:
{context}

Question: {question}

Instructions:
- Answer only using the information present in the context above.
- If the answer is not present in the context, say "I don't have enough information from this video to answer that."
- Do not make up information that is not in the context.
- Keep the answer clear and concise.

Answer:"""


def get_llm():
    endpoint = HuggingFaceEndpoint(
        repo_id="meta-llama/Llama-3.3-70B-Instruct",
        task="text-generation",
        temperature=0,
        huggingfacehub_api_token=os.getenv("HF_TOKEN")
    )
    llm = ChatHuggingFace(llm=endpoint)
    return llm


def build_context(retrieved_docs) -> str:
    context_parts = [doc.page_content for doc in retrieved_docs]
    return "\n\n".join(context_parts)


def answer_query(video_id: str, question: str, k: int = 4):
    vectorstore = load_vectorstore(video_id)
    retrieved_docs = vectorstore.similarity_search(question, k=k)

    context = build_context(retrieved_docs)

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    formatted_prompt = prompt.format(context=context, question=question)

    llm = get_llm()
    response = llm.invoke(formatted_prompt)

    return response.content, retrieved_docs


if __name__ == "__main__":
    video_id = "Gfr50f6ZBvo"
    question = "What is this video about?"

    answer, sources = answer_query(video_id, question)

    print("Question:", question)
    print("Answer:", answer)
    print("=" * 50)
    print("Sources used:")
    for i, doc in enumerate(sources):
        print(f"Source {i + 1}:", doc.page_content[:200])