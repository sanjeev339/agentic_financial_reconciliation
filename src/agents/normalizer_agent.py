from langchain_core.messages import SystemMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import Settings
from src.tools.normalize_tools import normalize_erp, normalize_bank
from src.tools.log_tools import append_log

def build_normalizer():
    """Builds the NormalizerAgent that cleans and standardizes ERP & Bank data.

    Author: Dr. Ayushi Mandlik
    """
    settings = Settings()
    llm = ChatGoogleGenerativeAI(
        model=settings.model,
        temperature=settings.temperature,
        google_api_key=settings.google_api_key
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are NormalizerAgent. Standardize dates (ISO), normalize amounts (2dp), "
         "and extract Invoice IDs from bank descriptions.\n\n"
         "You have access to the following tools:\n{tools}\n\n"
         "Always log actions."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")  # ✅ Explicit variable_name
    ])

    tools = [normalize_erp, normalize_bank, append_log]

    agent = create_tool_calling_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    return AgentExecutor(agent=agent, tools=tools, verbose=True)
