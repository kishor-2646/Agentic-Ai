from llm_setup import create_llm
from tool_calls import get_financial_data, get_stock_price, classify_pe_ratio
tools = [get_financial_data, get_stock_price, classify_pe_ratio]
from langchain.agents import create_agent
import gradio as gr

print("All libraries imported!")
llm = create_llm()      # initialize the llm

SYSTEM_PROMPT = """You are a Personal Investment Research Assistant.
You are NOT a licensed financial advisor — never give personalized buy/sell advice.

Follow these steps sequentially:

1. DECIDE SOURCE: Work out whether the question needs LIVE market data
   (current/today's price, live P/E), STATIC document data (the annual report:
   revenue, profit, EPS, dividend history), or BOTH.
2. RETRIEVE: Call get_financial_data for anything from the annual report.
   Call get_stock_price for anything about a stock's current price today.
3. CLASSIFY: If the user is asking whether a P/E ratio is low/fair/high, you MUST
   call classify_pe_ratio with the numeric P/E value — never judge it yourself.
   This usually means calling get_stock_price first to get the number, then
   classify_pe_ratio with that number (two tool calls in sequence).
4. COMBINE: If a question needs more than one tool, call all of them before answering.
5. LABEL SOURCES: Tool outputs already start with [LIVE] or [DOCUMENT] — keep that
   tag on every number you repeat in your final answer.
6. If a tool returns "not found" or nothing relevant, say so plainly instead of
   guessing or inventing a number.
"""
# create an agent using llm,tools,system_prompt
research_agent = create_agent(
    model=llm, tools=tools, system_prompt=SYSTEM_PROMPT
)

def run_agent(query):
    response = research_agent.invoke(
        {
            "messages": [
                {"role": "user", "content": query}
            ]
        }
    )
    print("\n\n\nACTUAL RESPONSE WITH TOOLS\n\n\n", response)
    return response["messages"][-1].content

def deploy_agent():

    with gr.Blocks(title="Personal Investment Research Agent") as iface:
        gr.Markdown("## Personal Investment Research Agent")
        gr.Markdown(
            """
            ⚠️ Not personalized financial advice. Document data is mock/fictional for this workshop.
            Ask about the annual report (static) or a live stock price (e.g. AAPL) — or both.
            """
        )
        query_input = gr.Textbox(label="Your question", placeholder="e.g. What was Q2 revenue, and what's AAPL trading at right now?")
        ask_button = gr.Button("Ask", variant="primary")
        output = gr.Textbox(label="Answer", lines=15)
        ask_button.click(fn=run_agent, inputs=[query_input], outputs=output)
    iface.launch(debug=True)

if __name__ == "__main__":
    # response = run_agent("What was Q2 revenue?")
    # print("\nCLEAN RESPONSE\n")
    # print(response)

    deploy_agent()
