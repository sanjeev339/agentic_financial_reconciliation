from typing import Dict, Any
import os
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from langchain.tools import tool

@tool("export_outputs")
def export_outputs(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Export reconciliation results, discrepancies, and metadata into
    structured output files (e.g., Excel, JSON).

    Args:
        payload (Dict[str, Any]): A dictionary containing reconciliation
                                  results, logs, and classified discrepancies.

    Returns:
        Dict[str, Any]: Metadata about exported files (e.g., file paths).

    Author:
        Dr. Ayushi Mandlik
    """
    out_dir = payload.get("out_dir", "outputs")
    os.makedirs(out_dir, exist_ok=True)
    erp = pd.DataFrame(payload["erp"]["records"])
    bank = pd.DataFrame(payload["bank"]["records"])
    rec_rows = []
    for r in payload["discrepancies"]["results"]:
        rec_rows.append({"ERP Index": r.get("erp_index"), "Bank Index": r.get("bank_index"), "Status": r.get("status"), "Amount Diff": r.get("amount_diff"), "Rationale": " | ".join(r.get("rationale") or [])})
    reconciled_df = pd.DataFrame(rec_rows)
    csv_path = os.path.join(out_dir, "reconciled.csv")
    xlsx_path = os.path.join(out_dir, "reconciled.xlsx")
    report_pdf = os.path.join(out_dir, "summary.pdf")
    reconciled_df.to_csv(csv_path, index=False)
    with pd.ExcelWriter(xlsx_path) as writer:
        reconciled_df.to_excel(writer, sheet_name="reconciliation", index=False)
        erp.to_excel(writer, sheet_name="erp_normalized", index=False)
        bank.to_excel(writer, sheet_name="bank_normalized", index=False)
    c = canvas.Canvas(report_pdf, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2*cm, height-2*cm, "Financial Reconciliation Summary")
    c.setFont("Helvetica", 10)
    totals = reconciled_df["Status"].value_counts().to_dict()
    y = height-3*cm
    for k, v in totals.items():
        c.drawString(2*cm, y, f"{k}: {v}"); y -= 0.6*cm
    c.drawString(2*cm, y, f"Total Records: {len(reconciled_df)}"); y -= 1.0*cm
    c.drawString(2*cm, y, "See reconciled.xlsx and reconciled.csv for details.")
    c.showPage(); c.save()
    return {"csv": csv_path, "xlsx": xlsx_path, "pdf": report_pdf}
