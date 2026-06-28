from dataclasses import dataclass, field
from src.models.debug import PipelineDebug


# ==========================================================
# Assistant Response
# ==========================================================
@dataclass
class AssistantResponse:
    question: str
    answer: str
    sources: list = field(default_factory=list)
    latency: float = 0.0
    success: bool = True
    debug: PipelineDebug | None = None
