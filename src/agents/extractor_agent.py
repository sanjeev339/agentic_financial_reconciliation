from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import Settings
from src.tools.file_tools import read_erp_excel, read_bank_pdf
from src.tools.log_tools import append_log


def build_extractor():
    """
    Build the Extractor Agent.

    Uses Gemini (Google Generative AI) model for extraction tasks.
    Configured via settings.

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
         "You are ExtractorAgent. Parse ERP Excel and Bank PDF into structured tables. Use the provided tools. Always log your actions."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

    tools = [read_erp_excel, read_bank_pdf, append_log]

    agent = create_tool_calling_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    return AgentExecutor(agent=agent, tools=tools, verbose=True)
