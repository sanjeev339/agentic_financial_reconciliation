from typing import Dict, Any
import pdfplumber
import pandas as pd
from langchain.tools import tool
from io import BytesIO

@tool("read_erp_excel", return_direct=False)
def read_erp_excel(file_bytes: bytes) -> Dict[str, Any]:
    """
    Parse ERP data from an uploaded Excel file.

    Args:
        file_bytes (bytes): Raw bytes of the uploaded Excel file.

    Returns:
        Dict[str, Any]: Parsed ERP data structured as records
                        (e.g., transaction ID, date, amount).

    Author:
        Dr. Ayushi Mandlik
    """
    df = pd.read_excel(BytesIO(file_bytes), dtype={"Invoice ID": str})
    df.columns = [c.strip() for c in df.columns]
    return {"columns": df.columns.tolist(), "records": df.to_dict(orient="records")}

@tool("read_bank_pdf", return_direct=False)
def read_bank_pdf(file_bytes: bytes) -> Dict[str, Any]:
    """
    Parse bank statement data from an uploaded PDF file.

    Args:
        file_bytes (bytes): Raw bytes of the uploaded PDF file.

    Returns:
        Dict[str, Any]: Parsed bank transactions extracted from the PDF.

    Author:
        Dr. Ayushi Mandlik
    """
    rows = []
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables or []:
                header = [h.strip() if isinstance(h, str) else "" for h in table[0]]
                for r in table[1:]:
                    row = {header[i] if i < len(header) else f"col_{i}": r[i] for i in range(len(r))}
                    rows.append(row)
    df = pd.DataFrame(rows)
    rename_map = {}
    for col in df.columns:
        low = str(col).lower().strip()
        if low == "date": rename_map[col] = "Date"
        elif "description" in low: rename_map[col] = "Description"
        elif "amount" in low: rename_map[col] = "Amount"
        elif "ref" in low or low in {"id","ref id"}: rename_map[col] = "Ref ID"
    df = df.rename(columns=rename_map)
    return {"columns": df.columns.tolist(), "records": df.to_dict(orient="records")}
