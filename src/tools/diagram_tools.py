from langchain.tools import tool
import os

MERMAID = '''flowchart TD
  U[User Uploads ERP (Excel) & Bank (PDF)] --> E(ExtractorAgent)
  E --> N(NormalizerAgent)
  N --> M(MatcherAgent)
  M --> A(AuditorAgent)
  A --> R(ReporterAgent)
  R --> O[Outputs: CSV/Excel, PDF, Logs, Diagram]
'''

@tool("generate_mermaid")
def generate_mermaid(out_dir: str = "outputs") -> dict:
    """
    Generate a reconciliation process diagram in Mermaid syntax and save it as an output file.

    Args:
        out_dir (str, optional): Directory where the generated Mermaid diagram will be saved.
                                 Defaults to "outputs".

    Returns:
        dict: Metadata containing the file path and diagram content.

    Author:
        Dr. Ayushi Mandlik
    """
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "workflow.mmd")
    with open(path, "w") as f:
        f.write(MERMAID.strip()+"\n")
    return {"mermaid_path": path}
