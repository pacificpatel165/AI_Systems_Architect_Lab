from dataclasses import dataclass, field


# ==========================================================
# Strategy Information
# ==========================================================
@dataclass
class StrategyInfo:
    rewrite: bool = False
    metadata: bool = False
    parent: bool = False
    compression: bool = False


# ==========================================================
# Query Information
# ==========================================================
@dataclass
class QueryInfo:
    question: str
    rewritten_query: str
    query_type: str
    strategy: StrategyInfo = field(default_factory=StrategyInfo)
    document_filter: str | None = None


# ==========================================================
# Retrieval Information
# ==========================================================
@dataclass
class RetrievalInfo:
    retrieved_indices: list = field(default_factory=list)
    ranked_results: list = field(default_factory=list)
    top_indices: list = field(default_factory=list)
    parent_ids: list = field(default_factory=list)
    sources: list = field(default_factory=list)
    details: list = field(default_factory=list)


# ==========================================================
# Context Information
# ==========================================================
@dataclass
class ContextInfo:
    original: str = ""
    compressed: str = ""
    original_length: int = 0
    compressed_length: int = 0
    compression_ratio: float = 0.0


# ==========================================================
# Memory Information
# ==========================================================
@dataclass
class MemoryInfo:
    turns: int = 0


# ==========================================================
# Performance Information
# ==========================================================
@dataclass
class PerformanceInfo:
    retrieved_chunks: int = 0
    returned_chunks: int = 0
    latency: float = 0.0


# ==========================================================
# Pipeline Debug Information
# ==========================================================
@dataclass
class PipelineDebug:
    query: QueryInfo
    retrieval: RetrievalInfo
    context: ContextInfo
    memory: MemoryInfo
    performance: PerformanceInfo
