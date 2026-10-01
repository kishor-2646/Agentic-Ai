Personal Investment Research Agent

RAG + tool-calling agent over a mock annual report, combined with live stock
price data. Mirrors the structure of the resume/job-matcher workshop repo.

SETUP TO CREATE venv (skip if you're reusing the existing Agentic_AI venv)

open terminal
1. Create a virtual environment using below command:
python -m venv venv

2. Give PowerShell permission to run activation scripts:
Set-ExecutionPolicy Bypass -Scope CurrentUser -Force

3. Activate the virtual environment:
.\venv\Scripts\Activate.ps1

Inside the virtual environment run the following commands:

ollama pull qwen3:0.6b
ollama pull all-minilm

pip install langchain langchain-core langchain-ollama langchain-community langchain-classic gradio python-dotenv pypdf faiss-cpu yfinance

RUN ORDER

python demo.py          # 1. sanity check the LLM
python rag.py            # 2. test retrieval — ask it "What was Q2 revenue?"
python tool_calls.py    # 3. test both tools standalone
python agent.py          # 4. launches the Gradio app

DEMO QUERIES

- "What was Aarav Tech's revenue in Q2 of FY2025-26?"           (retrieval only) tool 1
- "What's AAPL trading at right now, and what's its P/E?"        (live only) tool 2
- "What was Q2 revenue, and how does that compare to AAPL's live price?"  (both tools)
-  "Is AAPL's current P/E ratio low, fair, or high?"                         (tool 3)
- is pe ratio 12.5 fair


ENVIRONMENT VARIABLES

This project uses Alpha Vantage for live stock data. You need a .env file
in the repo root with the following key:

    ALPHA_VANTAGE_API_KEY=<your-key-here>

See .env.example for the template. Copy it to .env and fill in your key.
Never commit the real .env — it is listed in .gitignore.


WHAT I LEARNED

I accidentally committed a .env file containing real API keys to a public repo.
Git history preserves every committed file, so simply deleting it isn't enough —
the keys had to be rotated (regenerated) immediately. Lesson: always add .env to
.gitignore before the first commit, use os.getenv() in code, and provide a
.env.example so collaborators know which variables are needed without seeing
real values.

