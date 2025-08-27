# Agentic Financial Reconciliation Framework

## Overview

This project implements an **agentic framework** for automated financial reconciliation between ERP (Enterprise Resource Planning) data and bank statements. The system leverages a modular, multi-agent architecture to extract, normalize, match, audit, and report on financial records, providing a transparent, explainable, and extensible reconciliation pipeline.

The framework is built using Python, Streamlit for the user interface, and modern LLM-based agent orchestration (LangChain, LangGraph, Gemini/OpenAI). It is designed for extensibility, auditability, and ease of use for both technical and non-technical users.

---

## What is an Agentic Framework?

An **agentic framework** is a software architecture where autonomous, specialized agents collaborate to solve complex tasks. Each agent is responsible for a distinct function and can invoke tools, communicate with other agents, and log its actions. This approach enables modularity, transparency, and the ability to scale or swap out components independently.

In this project, the agentic framework orchestrates the following agents:

- **ExtractorAgent**: Parses ERP Excel and Bank PDF files into structured tables.
- **NormalizerAgent**: Cleans and standardizes the extracted data (dates, amounts, invoice IDs).
- **MatcherAgent**: Reconciles ERP and Bank records using fuzzy logic and heuristics.
- **AuditorAgent**: Classifies unmatched or mismatched items and provides rationales.
- **ReporterAgent**: Generates output files (CSV, Excel, PDF summary, workflow diagram) and collates logs.

Each agent is implemented as an LLM-powered tool-calling agent, with clear prompts and logging for traceability.

---

## Pipeline Workflow

The reconciliation process is fully automated and proceeds through the following stages:

1. **Extraction**: ERP (Excel) and Bank (PDF) files are parsed into structured tables.
2. **Normalization**: Data is cleaned, standardized (e.g., date formats, amounts), and invoice IDs are extracted.
3. **Matching**: ERP and Bank records are matched using fuzzy logic, with rationales for each match.
4. **Auditing**: Discrepancies (unmatched, mismatched, duplicates) are classified and explained.
5. **Reporting**: Outputs are generated, including reconciled files, a PDF summary, a workflow diagram, and agent logs.

### Workflow Diagram

```
flowchart TD
  U["User Uploads ERP (Excel) & Bank (PDF)"] --> E["ExtractorAgent"]
  E --> N["NormalizerAgent"]
  N --> M["MatcherAgent"]
  M --> A["AuditorAgent"]
  A --> R["ReporterAgent"]
  R --> O["Outputs: CSV/Excel, PDF, Logs, Diagram"]
```

---

## Directory Structure

- `streamlit_app.py` — Main Streamlit UI for uploading files and running the pipeline
- `src/agents/` — Agent implementations (extractor, normalizer, matcher, auditor, reporter, coordinator)
- `src/tools/` — Tool functions for file parsing, normalization, matching, reporting, etc.
- `outputs/` — Generated output files (CSV, Excel, PDF, logs, diagrams)
- `Example_files/` — Example ERP and bank statement files for testing
- `requirements.txt` — Python dependencies

---

## Setup & Installation

1. **Clone the repository**

```bash
cd /Users/pi-in-166/Desktop/reconciliation_problem/reconciliation_agents
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file or export the following environment variable:

```
GOOGLE_API_KEY=your_google_api_key_here
```

You can also configure the model and temperature in `src/config.py`.

---

## Usage

### Running the Streamlit App

```bash
streamlit run streamlit_app.py
```

- Upload your ERP file (Excel: `.xlsx` or `.xls`)
- Upload your Bank statement (PDF)
- Specify the output directory (optional)
- Click **Run Reconciliation**

The app will display:
- A summary of discrepancies
- Download links for reconciled CSV, Excel, PDF summary, and workflow diagram
- Agent logs for transparency

---

## Input Formats

### ERP File (Excel/CSV)
- Example (`sample_erp.csv`):

```
Date,Invoice ID,Amount,Status
2025-02-10,INV0001,267.10,Cancelled
2025-02-17,INV0002,1789.75,Paid
...
```

### Bank Statement (PDF)
- Example: See `sample_bank.pdf` or `Example_files/bank_statement.pdf`
- The system expects a tabular PDF with transaction details (date, description, amount, etc.)

---

## Output Files

After running the pipeline, the following files are generated in the output directory:

- `reconciled.csv` — Matched and unmatched records with status and rationales
- `reconciled.xlsx` — Excel version of the above
- `summary.pdf` — PDF summary of the reconciliation
- `workflow.mmd` — Mermaid diagram of the agent workflow
- Agent logs (JSON, included in the app)

Example of `reconciled.csv`:

```
ERP Index,Bank Index,Status,Amount Diff,Rationale
0.0,0.0,Matched,0.0,Exact amount match.
1.0,1.0,Amount mismatch,1.13,Amounts differ by 1.13 (> 0.05).
...
```

---

## Configuration

- **Model & Temperature**: Set in `src/config.py` (default: Gemini 1.5 Pro, temperature 0.2)
- **API Key**: Set `GOOGLE_API_KEY` in your environment or `.env` file
- **Output Directory**: Default is `./outputs`, can be changed in the UI or config

---

## Extending the Framework

- Add new agents or tools in `src/agents/` and `src/tools/`
- Modify prompts or logic for each agent to suit your domain
- The agentic design allows for easy integration of new data sources, matching logic, or reporting formats

---

## Dependencies

Key Python packages:
- `langchain`, `langchain-core`, `langchain-community`, `langgraph`, `langchain-openai`
- `openai`, `tiktoken`, `pandas`, `rapidfuzz`, `python-dateutil`, `pdfplumber`, `reportlab`, `streamlit`, `pydantic`, `matplotlib`, `pyarrow`

See `requirements.txt` for the full list.

---

## Authors & Credits

- Framework and agents: Dr. Ayushi Mandlik
- Built with LangChain, Gemini, and Streamlit

---

## License

This project is for academic and demonstration purposes. Please contact the author for commercial or production use.
