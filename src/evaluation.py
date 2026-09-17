import os
from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
from rag_chain import answer_query, get_api_key

load_dotenv()


FAITHFULNESS_PROMPT = """You are an evaluator checking if an answer is faithful to the given context.

Context:
{context}

Answer:
{answer}

Task: Check if the answer is fully supported by the context. Give a score between 0 and 1, where:
- 1 means the answer is completely based on the context, no made-up information.
- 0 means the answer contains information not present in the context at all.

Respond in this exact format:
Score: <number between 0 and 1>
Reason: <short explanation>
"""

RELEVANCY_PROMPT = """You are an evaluator checking if an answer is relevant to the question asked.

Question:
{question}

Answer:
{answer}

Task: Check how relevant the answer is to the question. Give a score between 0 and 1, where:
- 1 means the answer directly and fully addresses the question.
- 0 means the answer is unrelated to the question.

Respond in this exact format:
Score: <number between 0 and 1>
Reason: <short explanation>
"""


def get_eval_llm():
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.0,
        api_key=get_api_key("GROQ_API_KEY")
    )
    return llm


def evaluate_faithfulness(context: str, answer: str, llm) -> str:
    prompt = FAITHFULNESS_PROMPT.format(context=context, answer=answer)
    result = llm.invoke(prompt)
    return result.content


def evaluate_relevancy(question: str, answer: str, llm) -> str:
    prompt = RELEVANCY_PROMPT.format(question=question, answer=answer)
    result = llm.invoke(prompt)
    return result.content


def evaluate_answer(video_id: str, question: str):
    answer, sources = answer_query(video_id, question)
    context = "\n\n".join(doc.page_content for doc in sources)

    eval_llm = get_eval_llm()

    faithfulness_result = evaluate_faithfulness(context, answer, eval_llm)
    relevancy_result = evaluate_relevancy(question, answer, eval_llm)

    return answer, faithfulness_result, relevancy_result


if __name__ == "__main__":
    video_id = "Gfr50f6ZBvo"
    question = "What is this video about?"

    answer, faithfulness_result, relevancy_result = evaluate_answer(video_id, question)

    print("Question:", question)
    print("Answer:", answer)
    print("=" * 50)
    print("Faithfulness evaluation:")
    print(faithfulness_result)
    print("=" * 50)
    print("Relevancy evaluation:")
    print(relevancy_result)




