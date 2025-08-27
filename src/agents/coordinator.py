from typing import Dict, Any
from .extractor_agent import build_extractor
from .normalizer_agent import build_normalizer
from .matcher_agent import build_matcher
from .auditor_agent import build_auditor
from .reporter_agent import build_reporter
from ..tools.log_tools import append_log

def run_pipeline(erp_bytes: bytes, bank_bytes: bytes, out_dir: str = "outputs") -> Dict[str, Any]:
    extractor = build_extractor()
    normalizer = build_normalizer()
    matcher = build_matcher()
    auditor = build_auditor()
    reporter = build_reporter()

    append_log.invoke({"agent":"Coordinator","action":"start","message":"Extracting ERP & Bank"})
    erp_table = extractor.tools[0].invoke({"file_bytes": erp_bytes})
    bank_table = extractor.tools[1].invoke({"file_bytes": bank_bytes})
    append_log.invoke({"agent":"ExtractorAgent","action":"done","message":"Parsed ERP & Bank"})

    append_log.invoke({"agent":"Coordinator","action":"start","message":"Normalizing"})
    erp_norm = normalizer.tools[0].invoke({"payload": erp_table})
    bank_norm = normalizer.tools[1].invoke({"payload": bank_table})
    append_log.invoke({"agent":"NormalizerAgent","action":"done","message":"Normalization complete"})

    append_log.invoke({"agent":"Coordinator","action":"start","message":"Matching"})
    match_payload = {"erp": erp_norm, "bank": bank_norm}
    matches = matcher.tools[0].invoke({"payload": match_payload})
    append_log.invoke({"agent":"MatcherAgent","action":"done","message":"Preliminary matches computed"})

    append_log.invoke({"agent":"Coordinator","action":"start","message":"Classifying discrepancies"})
    disc_payload = {"erp": erp_norm, "bank": bank_norm, "matches": matches}
    discrepancies = auditor.tools[0].invoke({"payload": disc_payload})
    append_log.invoke({"agent":"AuditorAgent","action":"done","message":"Discrepancies labeled"})

    append_log.invoke({"agent":"Coordinator","action":"start","message":"Exporting outputs"})
    export_payload = {"erp": erp_norm, "bank": bank_norm, "discrepancies": discrepancies, "out_dir": out_dir}
    outputs = reporter.tools[0].invoke({"payload": export_payload})
    diagram = reporter.tools[1].invoke({"out_dir": out_dir})
    logs = reporter.tools[2].invoke({"_": None})

    return {"erp": erp_norm, "bank": bank_norm, "matches": matches, "discrepancies": discrepancies, "outputs": outputs, "diagram": diagram, "logs": logs}
