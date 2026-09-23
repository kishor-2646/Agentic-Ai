from urllib3 import response
from demo import create_llm
from tool_calls import web_search,get_job_recommendation,get_resume_data
tools = [web_search,get_job_recommendation,get_resume_data]
from langchain.agents import create_agent
import gradio as gr

print("All libraries imported")
llm = create_llm() #initialise the llm
SYSTEM_PROMPT = """You are an Expert Job Matcher. 
Your task is to find live jobs matching the candidate's resume.

Follow these 4 execution steps sequentially:

1. RETRIEVE RESUME: Call get_resume_data using simple topic keywords (e.g., query="skills", query="experience").
2. EXTRACT LOGIC: From the retrieved resume:
   - Identify candidate experience level (Fresher: 0-1 yrs | Junior: 1-3 yrs | Mid: 3-5 yrs).
   - Pick 1 or 2 core tech keywords (e.g., "python", "fastapi").
   - Set a realistic minimum annual salary in INR (e.g., 500000).
3. SEARCH JOBS: Call get_job_recommendation(what=..., salary_min=...) using your extracted parameters.
4. FORMAT OUTPUT: Present top 3-5 live job results returned by the search tool.

Formatting Rules:
- Display: Job Title, Company, Location, Salary (in ₹ INR), Brief Description, and Apply Link (redirect_url).
- Base recommendations ONLY on live job API results. Never list past companies from the user's resume as new openings.
- If a field is missing in the result, write "Not specified".
"""


#create an agent using tools, llm, System prompts
job_search_agent = create_agent(
    model = llm, tools= tools, system_prompt=SYSTEM_PROMPT
)

def run_agent(role,salary_min):
    response = job_search_agent.invoke(
        {
            "messages": [
                {
                     "role":"user",
                     "content":
                     (
                        f"Find live jobs for the role:{role}"
                        f"The minimum salary is Rs.{salary_min} per year"
                        "use my resume data to match the jobs"
                     )
                }
            ]
        }
    )
    print("\n\n\n ACTUAL AGENT RESPONSE WITH TOOLS \n]n]n", response)
    return response["messages"][-1].content



def deploy_agent():
    with gr.Blocks(title="Career Match Agent") as iface:
        gr.Markdown("#Career Match Agent #")
        gr.Markdown("""## Role: `Soft Engineer`<br>
            Find Job opening that match your resume, using live listing and your indexed data.
            """)
        role_input = gr.Textbox(label= "Job Role", placeholder = "e.g Python Developer, Data Analyst, ML Engineer")
        salary_input = gr.Number(label="Minimum Annual Salary (Rs)", value = 5000000, minimum = 0, precision = 0)
        find_jobs_button = gr.Button("Find my matching jobs",variant="primary")
        output = gr.Textbox(label="Recommended Jobs",lines=20)
        find_jobs_button.click(fn=run_agent,inputs=[role_input, salary_input],outputs=output)
    iface.launch(debug=True)











if __name__ == "__main__":
    response = run_agent(role="Data Analyst",salary_min=600000)
    print("\n CLEAN RESPONSE")
    print(response)
    deploy_agent()
    

