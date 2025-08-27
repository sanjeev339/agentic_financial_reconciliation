from langchain_core.messages import SystemMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from ..config import settings
from ..tools.reporting_tools import export_outputs
from ..tools.diagram_tools import generate_mermaid
from ..tools.log_tools import get_logs, append_log

from src.config import Settings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def build_reporter():
     """Builds the MatcherAgent that reconciles ERP & Bank rows using Gemini.

     Author: Dr. Ayushi Mandlik
     """
     settings = Settings()
     llm = ChatGoogleGenerativeAI(
         model=settings.model,         # e.g., "gemini-1.5-pro"
         temperature=settings.temperature,
         google_api_key=settings.google_api_key
     )

     # Build a proper prompt
     prompt = ChatPromptTemplate.from_messages([
         ("system",
         "You are ReporterAgent. Produce the final outputs: reconciled files, PDF summary, and workflow diagram."
         "Use export_outputs and generate_mermaid. Retrieve logs with get_logs and include paths in your final message."),
         MessagesPlaceholder("chat_history"),
         ("human", "{input}"),  # user input will go here
         MessagesPlaceholder(variable_name="agent_scratchpad")
     ])

     tools = [export_outputs, generate_mermaid, get_logs, append_log]

     # Use prompt, not list
     agent = create_tool_calling_agent(llm = llm, tools= tools, prompt = prompt)

     return AgentExecutor(agent=agent, tools=tools, verbose=False)
