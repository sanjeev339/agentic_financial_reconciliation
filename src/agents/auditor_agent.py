from langchain_core.messages import SystemMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_openai import ChatOpenAI
from ..config import settings
from ..tools.discrepancy_tools import classify_discrepancies
from ..tools.log_tools import append_log
from src.config import Settings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def build_auditor():
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
         "You are AuditorAgent. Classify unmatched and mismatched items. "
         "Use classify_discrepancies and add clear, human-readable rationales. Always log."),
         MessagesPlaceholder("chat_history"),
         ("human", "{input}"),  # user input will go here
         MessagesPlaceholder(variable_name="agent_scratchpad")
     ])

     tools = [classify_discrepancies, append_log]

     # Use prompt, not list
     agent = create_tool_calling_agent(llm = llm, tools= tools, prompt = prompt)

     return AgentExecutor(agent=agent, tools=tools, verbose=False)
