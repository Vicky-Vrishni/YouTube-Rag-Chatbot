import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
from transcript_extractor import get_transcript
from chunking import chunk_transcript
from vectorstore import create_vectorstore, load_vectorstore
from rag_chain import answer_query
from evaluation import evaluate_faithfulness, evaluate_relevancy, get_eval_llm


st.set_page_config(page_title="YouTube RAG Chatbot", layout="wide")

st.title("YouTube Video Chatbot")
st.caption("Ask questions about any YouTube video using RAG")


if "video_id" not in st.session_state:
    st.session_state.video_id = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


with st.sidebar:
    st.header("Load a Video")
    video_url = st.text_input("YouTube video URL")
    process_button = st.button("Process Video")

    if process_button and video_url:
        with st.spinner("Extracting transcript..."):
            try:
                text, raw_data, video_id = get_transcript(video_url)
            except Exception as e:
                st.error(f"Failed to extract transcript: {e}")
                st.stop()

        with st.spinner("Chunking transcript..."):
            chunks = chunk_transcript(text)

        with st.spinner("Creating embeddings and storing in vector database..."):
            create_vectorstore(chunks, video_id)

        st.session_state.video_id = video_id
        st.session_state.chat_history = []
        st.success(f"Video processed successfully. Total chunks: {len(chunks)}")


if st.session_state.video_id:
    st.subheader(f"Chatting about video: {st.session_state.video_id}")

    for entry in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(entry["question"])
        with st.chat_message("assistant"):
            st.write(entry["answer"])
            with st.expander("Sources used"):
                for i, source in enumerate(entry["sources"]):
                    st.write(f"Source {i + 1}: {source[:200]}")
            with st.expander("Evaluation scores"):
                st.write("Faithfulness:", entry["faithfulness"])
                st.write("Relevancy:", entry["relevancy"])

    user_question = st.chat_input("Ask a question about the video")

    if user_question:
        with st.chat_message("user"):
            st.write(user_question)

        with st.spinner("Generating answer..."):
            answer, sources = answer_query(st.session_state.video_id, user_question)
            context = "\n\n".join(doc.page_content for doc in sources)

        with st.spinner("Evaluating answer..."):
            eval_llm = get_eval_llm()
            faithfulness_result = evaluate_faithfulness(context, answer, eval_llm)
            relevancy_result = evaluate_relevancy(user_question, answer, eval_llm)

        with st.chat_message("assistant"):
            st.write(answer)
            with st.expander("Sources used"):
                for i, doc in enumerate(sources):
                    st.write(f"Source {i + 1}: {doc.page_content[:200]}")
            with st.expander("Evaluation scores"):
                st.write("Faithfulness:", faithfulness_result)
                st.write("Relevancy:", relevancy_result)

        st.session_state.chat_history.append({
            "question": user_question,
            "answer": answer,
            "sources": [doc.page_content for doc in sources],
            "faithfulness": faithfulness_result,
            "relevancy": relevancy_result
        })
else:
    st.info("Enter a YouTube video URL in the sidebar and click 'Process Video' to start.")