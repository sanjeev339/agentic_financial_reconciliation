from typing import List, Dict, Any
from langchain.tools import tool

GLOBAL_LOG: List[Dict[str, Any]] = []

@tool("append_log")
#def append_log(entry: Dict[str, Any]) -> str:
def append_log(agent: str, action: str, message: str) -> str:
    """
    Append a log entry to the reconciliation log file.
    """
    GLOBAL_LOG.append({
        "agent": agent,
        "action": action,
        "message": message
    })
    return "ok"

@tool("get_logs")
def get_logs(_=None) -> Dict[str, Any]:
    """
    Retrieve all stored reconciliation log entries.

    Args:
        _ (Any): Placeholder argument (not used).

    Returns:
        Dict[str, Any]: A dictionary containing all log records.

    Author:
        Dr. Ayushi Mandlik
    """

    return {"logs": GLOBAL_LOG}
