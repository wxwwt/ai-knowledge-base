# rag/retrieve/models.py

from dataclasses import dataclass
from langchain_core.documents import Document
from typing import List, Optional

@dataclass
class HybridRetrieveItem:
    document: Document
    score: float
    sources: List[str]   # ["rule", "vector"]
    rule_score: Optional[float] = None
    vector_score: Optional[float] = None
