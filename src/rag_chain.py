import os
from dotenv import load_dotenv

def get_api_key(key_name: str) -> str:
    try:
        return st.secrets[key_name]
    except Exception:
        return os.getenv(key_name)


    
import streamlit as st
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate
from vectorstore import load_vectorstore

load_dotenv()

PROMPT_TEMPLATE = """You are a helpful AI assistant that answers ONLY provided questions based only on the provided video transcript context.

Context from the video:
{context}

Question: {question}

Instructions:
- Answer ONLY using the information present in the context above.
- If the answer is NOT present in the context, say "I don't have enough information from this video to answer that."
- Do NOT MAKE UP information that is not in the context.
- Keep the ANSWER CLEAR and CONCISE.

Answer: """


def get_llm():
    endpoint = HuggingFaceEndpoint(
        repo_id="meta-llama/Llama-3.3-70B-Instruct",
        task="text-generation",
        temperature=0,
       huggingfacehub_api_token=get_api_key("HF_TOKEN")
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
