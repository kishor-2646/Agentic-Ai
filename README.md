# Agentic AI

Two LangChain-powered agentic projects built with **Ollama (Qwen3 0.6B)**, **RAG (FAISS + all-MiniLM)**, and **Gradio** — running entirely on a local machine with no cloud LLM costs.

---

## Projects

### 1. Career Match Agent _(root directory)_

A resume-aware job-search agent that:

- **Retrieves** relevant sections from your PDF resume via RAG (FAISS similarity search)
- **Searches** live Indian job listings through the [Adzuna API](https://developer.adzuna.com/)
- **Matches** jobs to your skills, experience level, and salary expectations
- Presents results in a **Gradio** web UI

| File | Purpose |
|------|---------|
| `demo.py` | LLM sanity check — make sure Ollama is running |
| `rag.py` | PDF ingestion → chunking → FAISS vector store → retrieval QA chain |
| `tool_calls.py` | Tool definitions: web search, resume retriever, live job search |
| `agent.py` | Orchestrates tools with a system prompt, deploys Gradio UI |
| `resume.pdf` | Sample resume used for RAG |

### 2. Personal Investment Research (PIR) Agent _(PIR_Agent/)_

A financial research agent that:

- **Retrieves** data from a mock annual report via RAG
- **Fetches** live stock prices from [Alpha Vantage](https://www.alphavantage.co/)
- **Classifies** P/E ratios as LOW / FAIR / HIGH using deterministic thresholds
- Combines document + live data to answer investment research questions

| File | Purpose |
|------|---------|
| `llm_setup.py` | LLM factory — Ollama Qwen3 0.6B |
| `rag.py` | Annual report ingestion → FAISS retrieval |
| `tool_calls.py` | Tool definitions: financial data retriever, live stock price, P/E classifier |
| `agent.py` | Orchestrates tools, deploys Gradio UI |
| `annual_report.txt` | Mock annual report for Aarav Tech (fictional) |

See [`PIR_Agent/README.md`](PIR_Agent/README.md) for detailed setup and demo queries.

---

## Quick Start

### Prerequisites

- **Python 3.10+**
- **[Ollama](https://ollama.com/)** installed and running

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/kishor-2646/Agentic-Ai.git
cd Agentic-Ai

# 2. Create & activate virtual environment
python -m venv venv
Set-ExecutionPolicy Bypass -Scope CurrentUser -Force   # PowerShell only
.\venv\Scripts\Activate.ps1

# 3. Pull the required Ollama models
ollama pull qwen3:0.6b
ollama pull all-minilm

# 4. Install dependencies
pip install langchain langchain-core langchain-ollama langchain-community langchain-classic gradio python-dotenv pypdf faiss-cpu yfinance requests

# 5. Set up environment variables
copy .env.example .env
# Then edit .env and fill in your API keys
```

### Environment Variables

Copy `.env.example` to `.env` and add your keys:

```env
ADZUNA_APP_ID=<your-adzuna-app-id>
ADZUNA_APP_KEY=<your-adzuna-app-key>
ALPHA_VANTAGE_API_KEY=<your-alpha-vantage-key>
```

> ⚠️ **Never commit `.env` to git.** It is already listed in `.gitignore`.

Get your free API keys:
- **Adzuna** → [developer.adzuna.com](https://developer.adzuna.com/)
- **Alpha Vantage** → [alphavantage.co/support/#api-key](https://www.alphavantage.co/support/#api-key)

### Run

**Career Match Agent** (root):
```bash
python demo.py          # 1. Sanity-check the LLM
python rag.py           # 2. Test retrieval
python tool_calls.py    # 3. Test tools standalone
python agent.py         # 4. Launch Gradio app
```

**PIR Agent**:
```bash
cd PIR_Agent
python llm_setup.py     # 1. Sanity-check the LLM
python rag.py           # 2. Test retrieval
python tool_calls.py    # 3. Test tools standalone
python agent.py         # 4. Launch Gradio app
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | Ollama — Qwen3 0.6B (local, free) |
| Embeddings | all-MiniLM (via Ollama) |
| Vector Store | FAISS (CPU) |
| Framework | LangChain (agents, tools, RAG chains) |
| UI | Gradio |
| APIs | Adzuna (jobs), Alpha Vantage (stocks) |

---

## What I Learned

I accidentally committed a `.env` file with real API keys to a public repo. Git history keeps every version of every file — simply deleting the file doesn't remove it from past commits. I had to:

1. Remove `.env` from tracking (`git rm --cached .env`)
2. Scrub it from history (`git filter-branch`)
3. **Rotate all exposed keys immediately** — this is the only thing that truly neutralizes the leak
4. Add `.env` to `.gitignore` before the first commit (prevention)
5. Provide a `.env.example` so collaborators know what keys are needed

**Rule:** Never hardcode API keys in source code. Always use `os.getenv()` + `python-dotenv`.

---

## License

This project is for educational and workshop purposes.
