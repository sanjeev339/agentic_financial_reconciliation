from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import Settings
from src.tools.match_tools import match_records
from src.tools.log_tools import append_log


def build_matcher():
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
         "You are MatcherAgent. Reconcile ERP & Bank rows using fuzzy logic and heuristics. "
         "Call `match_records`, then write a brief rationale for match quality, and log it."),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),  # user input will go here
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

    tools = [match_records, append_log]

    # Use prompt, not list
    agent = create_tool_calling_agent(llm = llm, tools= tools, prompt = prompt)

    return AgentExecutor(agent=agent, tools=tools, verbose=False)
