import os
from dotenv import load_dotenv

from langchain import hub
from langchain.agents import create_openai_functions_agent
from langchain_openai.chat_models import ChatOpenAI
from langchain.tools import tool
from langchain.pydantic_v1 import BaseModel, Field
from langgraph.graph import END, MessageGraph

from supabase import create_client

from typing import List, Tuple, Annotated, TypedDict
import operator
import datetime
import random
import requests

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
model = ChatOpenAI(temperature=0, api_key=openai_api_key)


############################ --Tools -- #########################################################
class CurrentDateTimeInput(BaseModel):
    pass

@tool("current-date-time", args_schema=CurrentDateTimeInput)
def current_date_time() -> str:
    """
    Function to get the current date and time
    """
    current_datetime = datetime.datetime.now()
    return f"The current date and time is: {current_datetime.strftime('%d/%m/%Y %H:%M')}"

class GetTranscriptsInput(BaseModel):
    pass

@tool("get-transcripts", args_schema=GetTranscriptsInput)
def get_transcripts() -> list[dict]:
    """
    Function to get all transcripts from Supabase
    """
    response = supabase.table("transcripts").select("*").execute()
    return response.get("data", [])

class GetAgentNameAndTypeInput(BaseModel):
    pass

@tool("get-agent-name-and-type", args_schema=GetAgentNameAndTypeInput)
def get_agent_name_and_type() -> tuple[str, str]:
    """
    Function to get agent name and type
    """
    agent_names = ["Austin", "Samantha", "Emma"]
    agent_name = random.choice(agent_names)
    agent_type = "Censored" if random.randint(0, 1) else "Uncensored"
    return agent_name, agent_type

class MakeOutboundCallInput(BaseModel):
    phone_number: str
    agent_type: str
    agent_name: str
    prompt_preamble: str

@tool("make-outbound-call", args_schema=MakeOutboundCallInput)
def make_outbound_call(phone_number: str, agent_type: str, agent_name: str, prompt_preamble: str) -> str:
    """
    Function to make an outbound call
    """
    url = "https://b951a587-42ec-49f6-8b2d-990b152b48d5-00-r0cij1ewiy7d.spock.replit.dev/start_outbound_call"
    payload = {
        "to_phone": phone_number,
        "agent_type": agent_type,
        "agent_name": agent_name,
        "prompt_preamble": prompt_preamble
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return "Outbound call successfully made"
    else:
        return f"Failed to make outbound call, status code: {response.status_code}"


#################################### --STATE-- ######################################################################
graph = MessageGraph()


# Define the nodes

# Define the graph

