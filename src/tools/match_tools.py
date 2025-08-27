from typing import Dict, Any
import pandas as pd
from langchain.tools import tool
from rapidfuzz import fuzz

def _match_row(erp_row, bank_df):
    inv = str(erp_row.get("Invoice ID") or "").strip().upper()
    amt = erp_row.get("Amount")
    candidates = bank_df.copy()
    if "Invoice ID" in candidates.columns and inv:
        candidates = candidates[candidates["Invoice ID"] == inv]
    if amt is not None and "Amount" in candidates.columns:
        candidates["amt_diff"] = (candidates["Amount"] - amt).abs()
        candidates = candidates.sort_values("amt_diff")
    if "Description" in candidates.columns and inv:
        candidates["desc_score"] = candidates["Description"].astype(str).apply(lambda s: fuzz.partial_ratio(s.upper(), inv))
        candidates = candidates.sort_values(["amt_diff","desc_score"], ascending=[True, False])
    if len(candidates) == 0:
        return None, None
    best = candidates.iloc[0].to_dict()
    amt_diff = abs((best.get("Amount") or 0) - (amt or 0))
    score = int(best.get("desc_score", 0)) - (amt_diff * 10)
    return best, score

@tool("match_records")
def match_records(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Match ERP records with bank statement records to identify aligned
    and mismatched entries.

    Args:
        payload (Dict[str, Any]): A dictionary containing normalized ERP
                                  and bank records.

    Returns:
        Dict[str, Any]: A mapping of matched, unmatched, and partially matched records.

    Author:
        Dr. Ayushi Mandlik
    """
    erp_df = pd.DataFrame(payload["erp"]["records"])
    bank_df = pd.DataFrame(payload["bank"]["records"])
    matches, used_bank_idx = [], set()
    for i, erp_row in erp_df.iterrows():
        best, score = _match_row(erp_row, bank_df)
        if best is None: continue
        idx = bank_df.index[(bank_df["Date"]==best.get("Date")) & (bank_df["Amount"]==best.get("Amount"))].tolist()
        idx = idx[0] if idx else None
        if idx is not None and idx not in used_bank_idx:
            used_bank_idx.add(idx)
            matches.append({"erp_index": int(i), "bank_index": int(idx), "score": float(score), "bank_row": best})
    erp_unmatched = [int(i) for i in range(len(erp_df)) if i not in [m["erp_index"] for m in matches]]
    bank_unmatched = [int(i) for i in range(len(bank_df)) if i not in used_bank_idx]
    return {"matches": matches, "erp_unmatched": erp_unmatched, "bank_unmatched": bank_unmatched}
