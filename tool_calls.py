from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
import os
import requests
from dotenv import load_dotenv
from rag import ingest_data
import json

load_dotenv()

print("All libraries imported")

#Tool 1: Web Search tool
web_search = DuckDuckGoSearchRun()

# Tool 2 : Resume data retriever tool 
@tool 
def get_resume_data(query:str)->str:
    """ Retrieve chunks of the candidate's 
    resume via similarity search """
    vector_store = ingest_data()
    response=vector_store.similarity_search(query)
    return response

#Tool 3 : Search live indian job listings
@tool 
def get_job_recommendation(what:str,salary_min:int)->str:
    """Searches live indian job listings 
    (Adzuna) by keyword and minimum salary
    """
    url = f'https://api.adzuna.com/v1/api/jobs/in/search/1?app_id={os.getenv("ADZUNA_APP_ID")}&app_key={os.getenv("ADZUNA_APP_KEY")}&what={what}&salary_min={salary_min}'
    response = requests.get(url)
    return response.json()

if __name__ == "__main__":
    #   tool 1: invoke the web search tool
    #   response = web_search.invoke("Agentic AI 2026 cabale")
    #  print(response)

   #  tool 2 invoke 
   # print(get_resume_data.invoke({"query":"technical skills"})[0])

   # Tool 3 invoke 
    response = get_job_recommendation.invoke({"what":"Data Analyst","salary_min":40000})
    print(json.dumps(response, indent=4))
    print(f"Tool Name : {get_job_recommendation.name}")
    print(f"Tool Arguments : {get_job_recommendation.args}")
    print(f"Tool Description : {get_job_recommendation.description}")

