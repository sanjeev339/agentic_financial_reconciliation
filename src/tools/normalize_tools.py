from typing import Dict, Any
import pandas as pd
from dateutil import parser
from langchain.tools import tool
import re

def _to_date(x):
    if pd.isna(x) or x == "":
        return None
    try:
        return parser.parse(str(x)).date().isoformat()
    except Exception:
        return None

def _to_amount(x):
    try:
        return round(float(str(x).replace(',', '')), 2)
    except Exception:
        return None

@tool("normalize_erp")
def normalize_erp(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize ERP data for reconciliation by standardizing formats
    such as dates, amounts, and identifiers.

    Args:
        payload (Dict[str, Any]): Raw ERP data.

    Returns:
        Dict[str, Any]: Normalized ERP records ready for matching.

    Author:
        Dr. Ayushi Mandlik
    """
    df = pd.DataFrame(payload["records"])
    if "Date" in df: df["Date"] = df["Date"].apply(_to_date)
    if "Amount" in df: df["Amount"] = df["Amount"].apply(_to_amount)
    if "Invoice ID" in df: df["Invoice ID"] = df["Invoice ID"].astype(str).str.strip().str.upper()
    if "Status" in df: df["Status"] = df["Status"].astype(str).str.strip().str.title()
    return {"records": df.to_dict(orient="records")}

@tool("normalize_bank")
def normalize_bank(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize bank statement data for reconciliation by standardizing
    transaction formats.

    Args:
        payload (Dict[str, Any]): Raw bank data.

    Returns:
        Dict[str, Any]: Normalized bank records ready for matching.

    Author:
        Dr. Ayushi Mandlik
    """
    df = pd.DataFrame(payload["records"])
    if "Date" in df: df["Date"] = df["Date"].apply(_to_date)
    if "Amount" in df: df["Amount"] = df["Amount"].apply(_to_amount)
    if "Description" in df:
        def extract_inv(text):
            if not isinstance(text, str): return None
            m = re.search(r"(?:INV[-\s]?)(\d+)", text, flags=re.I)
            return "INV" + m.group(1).zfill(4) if m else None
        df["Invoice ID"] = df["Description"].apply(extract_inv)
    return {"records": df.to_dict(orient="records")}
