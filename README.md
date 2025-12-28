# 📚 Research Paper Management & Analysis Intelligence System

An end-to-end **GenAI-powered research intelligence platform** that helps researchers **ingest, organize, search, analyze, and interact with academic papers** using **LLMs, semantic search, and vector databases**.

This project simulates a real-world system used by **universities, research labs, think tanks, and R&D teams** to manage large-scale scientific literature.

---

## 🚀 Key Features

### 📄 Paper Ingestion & Structuring
- Upload and parse academic research paper PDFs
- Section-level extraction:
  - Abstract
  - Introduction
  - Methods
  - Results / Experiments
  - Conclusion
  - References
- Automatic metadata enrichment (title, authors, year, abstract)

### 🧠 Semantic Search & Discovery
- Vector-based semantic search using **FAISS**
- Section-aware chunking for high-quality retrieval
- Natural language queries across multiple papers
- Retrieve most relevant **papers and sections**

### 🧩 Retrieval-Augmented Generation (RAG)
- LLM-powered question answering grounded in papers
- Citation-aware responses (section-level context)
- Structured paper summaries (planned)

### 📊 Research Intelligence (Planned)
- Trend analysis across years and topics
- Emerging research theme detection
- Citation relationship tracking

### 🖥️ Researcher UI
- Clean **Streamlit-based interface**
- Paper upload, search, and exploration
- Metadata editing (optional)

---

## 🏗️ System Architecture
```
PDFs + Metadata
│
▼
[PDF Parser & Section Extractor]
│
▼
[Paper Data Models (Pydantic)]
│
▼
[Section-Aware Chunking Engine]
│
▼
[Embeddings + FAISS Vector Store]
│
▼
[Semantic Search / RAG Pipeline]
│
▼
[Streamlit Research UI]
```

## 🛠️ Tech Stack

- **LLM**: Groq (FREE - Llama 3.1)
- **Embeddings**: HuggingFace sentence-transformers (FREE - runs locally)
- **Vector Store**: FAISS (FREE - runs locally)
- **Web Search**: Tavily API
- **UI**: Streamlit
- **Framework**: LangChain

## 📁 Project Structure

```
rag-chatbot/
├── config/
│   ├── __init__.py
│   └── settings.py           # Configuration & API keys
├── core/
│   ├── __init__.py
│   ├── document_processor.py # Document loading & splitting
│   ├── embeddings.py         # HuggingFace embeddings
│   ├── vector_store.py       # FAISS operations
│   └── chain.py              # RAG chain orchestration
├── data/
│   ├── documents/            # Uploaded documents
│   └── faiss_index/          # Persisted vector index
├── app.py                    # Main Streamlit app
├── main.py                   # main app
├── requirements.txt
└── README.md
```

## 🚀 Quick Start - Local Development

### 1. Clone and Setup Environment

**Windows (Command Prompt):**
```cmd
# Cloning the repo
git clone https://github.com/USERNAME/REPOSITORY_NAME.git

cd REPOSITORY_NAME

# creating virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Get API Keys (FREE!)

1. **Groq API Key** (FREE): https://console.groq.com/
   - Sign up and copy your API key
2. **Tavily API Key** (FREE tier): https://tavily.com/
   - Sign up and get your API key

### 3. Configure Environment Variables

**Using .env file (Recommended for local development)**

Your `.env` should look like this:
```bash
GROQ_API_KEY=gsk_your_actual_groq_key_here
TAVILY_API_KEY=tvly-your_actual_tavily_key_here
LLM_MODEL=llama-3.3-70b-versatile
LLM_TEMPERATURE=0.7
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
FAST_INDEX_PATH=your_actual_path
TOP_K_RESULT=3
```

⚠️ **IMPORTANT**: 
- Do NOT use quotes around values
- Never commit `.env` to git (it's already in `.gitignore`)

### 4. Run the Application

**All Platforms:**
```bash
python main.py
```

## 📖 SOLID Principles Applied

This project follows SOLID principles for maintainable code:

- **S**ingle Responsibility: Each module has one job
- **O**pen/Closed: Extensible without modifying existing code
- **L**iskov Substitution: Components can be swapped
- **I**nterface Segregation: Small, focused interfaces
- **D**ependency Inversion: Depend on abstractions

