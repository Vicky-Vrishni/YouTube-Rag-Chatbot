# YouTube RAG Chatbot

An end-to-end Retrieval-Augmented Generation (RAG) application that lets users chat with any YouTube video. Paste a video link, and ask questions about its content — answers are generated using only the video's transcript, with built-in hallucination detection.

**Live App:** https://youtube-rag-chatbot-2sbbddgnwduy7hu7scq3le.streamlit.app/

## Overview

This project takes a YouTube video, extracts its transcript, and builds a searchable knowledge base from it. When a user asks a question, the system retrieves the most relevant parts of the transcript and uses a large language model to generate a grounded, context-aware answer — while a separate evaluator model checks the answer for faithfulness and relevancy to reduce hallucination.

## Features

- Extracts transcripts directly from YouTube video links
- Splits transcripts into semantically meaningful chunks
- Generates dense vector embeddings for each chunk
- Stores and retrieves chunks using a vector database (ChromaDB)
- Uses context engineering to construct grounded prompts for the LLM
- Generates answers using Llama-3.3-70B-Instruct via Hugging Face Inference API
- Evaluates every answer for faithfulness and relevancy using a separate judge LLM (Groq's gpt-oss-120b), reducing self-bias
- Interactive chat interface built with Streamlit, including source citations and evaluation scores for every answer

## Tech Stack

| Component | Technology |
|---|---|
| Transcript Extraction | youtube-transcript-api |
| Chunking | LangChain (RecursiveCharacterTextSplitter) |
| Embeddings | Hugging Face (sentence-transformers/all-MiniLM-L6-v2) |
| Vector Database | ChromaDB |
| Generation LLM | Llama-3.3-70B-Instruct (Hugging Face Inference API) |
| Evaluation LLM | openai/gpt-oss-120b (Groq API) |
| UI | Streamlit |
| Deployment | Streamlit Community Cloud |

## Architecture



## How It Works

1. The user pastes a YouTube video URL in the sidebar and clicks "Process Video."
2. The transcript is extracted and split into overlapping chunks to preserve context.
3. Each chunk is converted into a vector embedding and stored in ChromaDB.
4. When the user asks a question, it is embedded and compared against stored chunks using similarity search to retrieve the most relevant ones.
5. The retrieved chunks are assembled into a structured prompt (context engineering) instructing the LLM to answer only from the given context.
6. The LLM generates an answer, which is then evaluated by a separate judge model for faithfulness (is it grounded in the context) and relevancy (does it address the question).
7. The answer, its sources, and evaluation scores are displayed in the chat interface.

## Running Locally

```bash
git clone https://github.com/Vicky-Vrishni/YouTube-Rag-Chatbot.git
cd YouTube-Rag-Chatbot
pip install -r requirements.txt
```

Create a `.env` file in the root directory with the following:

```bash
streamlit run app.py
```


## Frequently Asked Questions (FAQ)

### 1. What is a YouTube RAG Chatbot?

It is a Retrieval-Augmented Generation application that allows users to ask questions about the content of a YouTube video using its transcript.

### 2. Does the chatbot use the entire YouTube video?

The chatbot works with the available video transcript rather than directly processing the video itself.

### 3. How does the chatbot reduce hallucinations?

It retrieves relevant transcript chunks to ground the generated answer and uses a separate evaluator model to assess faithfulness and relevancy.

### 4. Which vector database does the project use?

The project uses ChromaDB to store and retrieve transcript embeddings.

### 5. Can I run the project locally?

Yes. Install the dependencies, configure the required API keys and run the Streamlit application as described in the setup instructions.




## Author

Built by Vicky, Final-year B.Tech Information Technology student, GJU Hisar.
