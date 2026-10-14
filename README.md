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
| Transcript Extraction | youtube-transcript-api | youtube-transcript-disabled
| Chunking | LangChain (RecursiveCharacterTextSplitter) |
| Embeddings | Hugging Face (sentence-transformers/all-MiniLM-L6-v2) |
| Vector Database | ChromaDB |
| Generation LLM | Llama-3.3-70B-Instruct (Hugging Face Inference API) |
| Evaluation LLM | openai/gpt-oss-120b (Groq API) |
| UI | Streamlit |
| Deployment | Streamlit Community Cloud |

## Architecture


flowchart TD
    A["User"] --> B["Streamlit UI"]
    B --> C["YouTube Video URL"]
    C --> D["Transcript Extractor"]
    D --> E["Transcript Text"]
    E --> F["Text Chunking"]
    F --> G["Embeddings"]
    G --> H[("Vector Store")]
    I["User Question"] --> J["Question Embedding"]
    J --> K["Similarity Search"]
    H --> K
    K --> L["Relevant Transcript Chunks"]
    L --> M["LLM"]
    M --> N["Answer to User"]

    D -. "Extraction failure" .-> O["Error Handling"]
    O --> B


The YouTube RAG Chatbot follows a Retrieval-Augmented Generation (RAG) workflow to answer questions using the content of YouTube videos.

### Workflow

1. **User Input:** The user provides a YouTube video URL through the application interface.
2. **Transcript Extraction:** The transcript extractor retrieves the video's available transcript.
3. **Error Handling:** Invalid video inputs and transcript extraction failures are handled with clear, controlled error messages.
4. **Text Processing:** The transcript is processed and split into smaller chunks suitable for retrieval.
5. **Embedding Generation:** Text chunks are converted into vector representations.
6. **Vector Storage and Retrieval:** The system searches for transcript chunks relevant to the user's question.
7. **Answer Generation:** The retrieved context is passed to the language model to generate a context-based response.
8. **Response Display:** The generated answer is returned to the user through the application interface.

### High-Level Data Flow

**YouTube URL → Transcript Extraction → Text Chunking → Embeddings → Vector Retrieval → LLM → Answer**

The retrieval step helps the language model focus on relevant video content instead of relying solely on its pretrained knowledge.



### Robust Transcript Error Handling

- Validates YouTube video URLs and video IDs before attempting transcript extraction.
- Handles unavailable transcripts, disabled captions, and inaccessible videos with clear error messages.
- Uses custom exceptions to distinguish invalid video inputs from transcript extraction failures.
- Avoids exposing raw internal exception details in user-facing error messages.
- Preserves the original exception as the cause to support debugging.

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

# Python cache
__pycache__/
*.py[cod]

# Virtual environments
venv/
.venv/

# Environment variables
.env
.env.*

# Jupyter Notebook
.ipynb_checkpoints/

# IDE files
.vscode/
.idea/

# Logs
*.log


## Author

Built by Vicky, Final-year B.Tech Information Technology student, GJU Hisar.
