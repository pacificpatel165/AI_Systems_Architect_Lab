from dataclasses import dataclass
from src.models.debug import PipelineDebug


# ==========================================================
# Retrieval Result
# ==========================================================
@dataclass
class RetrievalResult:
    debug: PipelineDebug
