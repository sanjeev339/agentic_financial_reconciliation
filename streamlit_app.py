import streamlit as st
import pandas as pd
from src.agents.coordinator import run_pipeline
from src.config import settings
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

st.set_page_config(page_title="Agentic Reconciliation", page_icon="🧮", layout="wide")
st.title("🧮 Agentic Financial Reconciliation")

st.markdown("Upload **ERP (Excel)** and **Bank (PDF)**, then run a fully agentic reconciliation pipeline.")

erp_file = st.file_uploader("Upload ERP Excel", type=["xlsx", "xls"])
bank_file = st.file_uploader("Upload Bank PDF", type=["pdf"])

out_dir = st.text_input("Output directory", value=settings.out_dir)

if st.button("Run Reconciliation", type="primary", disabled=not (erp_file and bank_file)):
    with st.spinner("Running agents..."):
        result = run_pipeline(erp_file.read(), bank_file.read(), out_dir=out_dir)

    st.success("Done!")
    st.subheader("Summary")
    disc = result["discrepancies"]["results"]
    disc_df = pd.DataFrame(disc)
    st.dataframe(disc_df, use_container_width=True)

    st.subheader("Outputs")
    st.write("CSV:", result["outputs"]["csv"])
    st.write("Excel:", result["outputs"]["xlsx"])
    st.write("PDF:", result["outputs"]["pdf"])
    st.write("Mermaid Diagram:", result["diagram"]["mermaid_path"])

    st.subheader("Agent Logs")
    logs = result["logs"]["logs"]
    st.json(logs)

    st.download_button("Download reconciled.csv", data=open(result["outputs"]["csv"], "rb").read(), file_name="reconciled.csv")
    st.download_button("Download reconciled.xlsx", data=open(result["outputs"]["xlsx"], "rb").read(), file_name="reconciled.xlsx")
    st.download_button("Download summary.pdf", data=open(result["outputs"]["pdf"], "rb").read(), file_name="summary.pdf")
    st.download_button("Download workflow.mmd", data=open(result["diagram"]["mermaid_path"], "rb").read(), file_name="workflow.mmd")

st.caption("Model & temperature in `src/config.py`. Provide your API key via env var `GOOGLE_API_KEY`.")
