from dataclasses import dataclass
from langchain_core.documents import Document
from typing import List


@dataclass
class RetrieveResult:
    document: Document
    score: int
    hit_rules: List[str]

