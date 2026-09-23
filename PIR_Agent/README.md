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


- No .env / API keys needed yet since yfinance is key-free. If you swap to
  Alpha Vantage or add the Adzuna-style pattern back, bring back python-dotenv
  + os.getenv the way tool_calls.py's job-search version did.





