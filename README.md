**MCQGenChatbot**

**Project Summary**
- **Description**: A lightweight project that demonstrates generating multiple-choice questions (MCQs) using generative AI patterns. The project implements a retrieval-augmented generation pipeline that combines an LLM with an embedding-based vector store to produce contextually relevant MCQs from provided text and knowledge.

**Features**
- **Generate MCQs**: Produce question stems and multiple-choice options from given text.
- **Retrieval-Augmented Generation (RAG)**: Use embeddings and a local vector store to retrieve context relevant to a prompt.
- **Local Vector Store**: Uses a Chroma-backed SQLite store in `vector_db/` for persistent embeddings and fast similarity search.
- **Modular code**: Separation between LLM logic and processing pipeline (`src/llm_logic.py`, `src/processor.py`).
- **Ask / Chat**: Converse with the knowledge base using an interactive ask/chat flow. The chat feature leverages the same retrieval pipeline to fetch supporting context and then uses the LLM to generate concise, grounded answers or follow-up prompts.


**Architecture & File Layout**
- **Entry points**: [app.py](app.py), [try.py](try.py)
- **Core modules**: [src/llm_logic.py](src/llm_logic.py), [src/processor.py](src/processor.py)
- **Vector DB**: `vector_db/` (Chroma DB files, including `chroma.sqlite3`)
- **Supporting files**: `requirements.txt`, `README.md`

**Technologies Used**
- **Python 3.8+**: Core language for the project.
- **LLM Providers**: Designed to work with hosted LLM APIs (e.g., OpenAI). Set your provider via environment variables and the code's client configuration.
- **Embeddings & Vector Search**: Chroma (local) for storing and querying embedding vectors.
- **Libraries**: Typical dependencies are listed in `requirements.txt` (e.g., transformers / openai / chromadb / sentence-transformers - check the file for exact pins).

**Gen AI Concepts (brief overview)**
- **Large Language Models (LLMs)**: Pretrained models that generate text given prompts. This project uses an LLM via API calls to generate MCQ text.
- **Embeddings**: Dense vector representations of text that capture semantic meaning. Used to index and retrieve relevant document chunks for a prompt.
- **Vector Databases / Similarity Search**: Store embeddings and perform nearest-neighbor search to fetch relevant context (Chroma in this repo).
- **Retrieval-Augmented Generation (RAG)**: Combine retrieved context with LLM prompts so answers (here, MCQs) are grounded in source material.
- **Prompt Engineering**: Carefully designing system and user prompts to steer the LLM output (question style, number of distractors, difficulty level).

**Setup Instructions**

- **Prerequisites**: Python 3.8+ and `git` installed.
- **Create a virtual environment (Windows PowerShell)**:

```powershell
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

- **On macOS / Linux**:

```bash
python3 -m venv venv
source venv/bin/activate
```

- **Install dependencies**:

```bash
pip install -r requirements.txt
```

- **Environment variables**
- **OPENAI_API_KEY** (or equivalent for your LLM provider): set this in your shell prior to running the app. Example (PowerShell):

```powershell
$env:OPENAI_API_KEY = "sk-..."
```

- **Run the application**

```bash
python app.py
# or a simple runner during development
python try.py
```

- **Ask / Chat usage**

You can use the chat/ask functionality to ask freeform questions within the context of uploaded document that are answered using retrieval + LLM generation. Typical usage patterns:

- Start the app and select the chat/ask mode (check `app.py` for CLI flags or interactive prompts).
- Provide a question; the system will retrieve relevant passages from `vector_db/`, include them in the prompt, and return a concise answer along with citations (if implemented).

If there is no dedicated UI, use `try.py` or extend `src/llm_logic.py` to call the chat function programmatically for experimentation.

**Using the Vector DB**
- The repository includes a pre-populated Chroma store at `vector_db/chroma.sqlite3` (and a UUID folder). You can replace or rebuild the store by running the embedding/ingestion routine in `src/processor.py` (see the module for usage notes).

**Development Notes**
- **Where to modify prompts**: `src/llm_logic.py` contains the prompt templates and LLM-call logic.
- **Processing pipeline**: `src/processor.py` handles chunking, embedding, and vector store interactions.
- **Quick iteration**: Modify prompt templates, run `python try.py` with sample text, and review outputs.

**Security & Privacy**
- **Data sent to LLMs**: Any text you send to an external LLM provider may be logged by that provider. Avoid sending sensitive or personal data.
- **Local Vector DB**: The Chroma store is local to this repository under `vector_db/`; secure the repo if it contains sensitive text.

**Disclaimer**
- **Academic mini-project**: This repository is an academic mini-project created while exploring generative AI techniques and is intended for learning and experimentation only. It is not production-ready. Exercise caution when using generated content.

**Contributing**
- Feel free to open issues or PRs for bug fixes, improvements, or suggested prompt templates.

**Acknowledgments & References**
- Retrieval-Augmented Generation (RAG) patterns, embedding models, and vector DB tooling inspired this project.

**License**
- This project is provided for educational use. Add a license of your choice if you intend to share or publish widely.


