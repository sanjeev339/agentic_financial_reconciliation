from typing import Dict, Any
import pandas as pd
from langchain.tools import tool

@tool("classify_discrepancies")
def classify_discrepancies(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Classify discrepancies found during reconciliation between ERP and bank records.

    Args:
        payload (Dict[str, Any]): A dictionary containing matched/unmatched records
                                  and discrepancy details.

    Returns:
        Dict[str, Any]: A structured classification of discrepancies
                        (e.g., missing entries, mismatched values).

    Author:
        Dr. Ayushi Mandlik
    """
    erp_df = pd.DataFrame(payload["erp"]["records"]).copy()
    bank_df = pd.DataFrame(payload["bank"]["records"]).copy()
    matches = payload["matches"]["matches"]
    erp_unmatched = set(payload["matches"]["erp_unmatched"])
    bank_unmatched = set(payload["matches"]["bank_unmatched"])

    results, seen_pairs = [], set()
    for m in matches:
        e = erp_df.iloc[m["erp_index"]].to_dict()
        b = bank_df.iloc[m["bank_index"]].to_dict()
        key = (m["erp_index"], m["bank_index"])
        if key in seen_pairs: continue
        seen_pairs.add(key)
        amt_e = e.get("Amount"); amt_b = b.get("Amount")
        diff, label, rationale = None, "Matched", []
        if amt_e is not None and amt_b is not None:
            diff = round(abs(amt_e - amt_b), 2)
            if diff == 0:
                label = "Matched"; rationale.append("Exact amount match.")
            elif diff <= 0.05:
                label = "Rounding difference"; rationale.append(f"Amounts differ by {diff}, within rounding tolerance (≤ 0.05).")
            else:
                label = "Amount mismatch"; rationale.append(f"Amounts differ by {diff} (> 0.05).")
        inv = (e.get("Invoice ID") or "").strip().upper()
        dup_erp = (erp_df["Invoice ID"].astype(str).str.upper() == inv).sum() > 1 if inv and "Invoice ID" in erp_df else False
        dup_bank = ("Invoice ID" in bank_df) and ((bank_df["Invoice ID"].astype(str).str.upper() == inv).sum() > 1) if inv else False
        if dup_erp or dup_bank:
            label = "Duplicate"; rationale.append("Invoice ID appears multiple times in one dataset.")
        results.append({"erp_index": m["erp_index"], "bank_index": m["bank_index"], "status": label, "amount_diff": diff, "rationale": rationale})
    for i in erp_unmatched:
        results.append({"erp_index": i, "bank_index": None, "status": "Missing in Bank", "amount_diff": None, "rationale": ["ERP record has no corresponding bank transaction after matching."]})
    for j in bank_unmatched:
        results.append({"erp_index": None, "bank_index": j, "status": "Missing in ERP", "amount_diff": None, "rationale": ["Bank transaction has no corresponding ERP record after matching."]})
    return {"results": results}
