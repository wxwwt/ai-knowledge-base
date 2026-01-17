# rag/retrieve/rule_retrieve.py

from typing import List
from langchain_core.documents import Document
from examples.rag.chapter03.retrieve.models import HybridRetrieveItem
import re


# =========================
# Query 归一化（去噪）
# =========================

def normalize_query(query: str) -> List[str]:
    """
    将自然语言 query 转成高信息密度关键词
    """
    q = query.lower().strip()

    noise_patterns = [
        r"什么是",
        r"请介绍",
        r"介绍一下",
        r"是什么",
        r"如何",
        r"怎么",
        r"吗",
        r"\?",
        r"？",
    ]

    for p in noise_patterns:
        q = re.sub(p, "", q)

    tokens = re.split(r"\s+|，|,|。|；|;", q)

    tokens = [
        t.strip()
        for t in tokens
        if len(t.strip()) >= 2
    ]

    return tokens


# =========================
# 核心规则检索接口
# =========================

def retrieve(
    query: str,
    documents: List[Document],
    top_k: int = 3,
    debug: bool = False
) -> List[HybridRetrieveItem]:
    """
    规则检索（Rule-based Retrieve）

    特点：
    - 纯规则
    - 可解释
    - 不依赖向量 / LLM
    """

    keywords = normalize_query(query)
    results: List[HybridRetrieveItem] = []

    query_lower = query.lower()

    for doc in documents:
        score = 0.0
        hit_rules = []

        content_lower = doc.page_content.lower()
        project = doc.metadata.get("project", "").lower()
        doc_type = doc.metadata.get("doc_type", "")

        # ---------- R1：内容关键词命中 ----------
        for kw in keywords:
            if kw in content_lower:
                score += 3
                hit_rules.append(f"content_hit:{kw}")

        # ---------- R2：项目名命中 ----------
        for kw in keywords:
            if kw in project:
                score += 2
                hit_rules.append(f"project_hit:{kw}")

        # ---------- R3：协议类语义增强 ----------
        if (
            ("协议" in query or "protocol" in query_lower)
            and doc_type == "protocol"
        ):
            score += 2
            hit_rules.append("protocol_match")

        if score > 0:
            results.append(
                HybridRetrieveItem(
                    document=doc,
                    score=float(score),
                    sources=["rule"],
                    rule_score=float(score),
                    vector_score=None
                )
            )

    # ---------- 排序 ----------
    results.sort(key=lambda x: x.score, reverse=True)

    # ---------- Debug 输出 ----------
    if debug:
        print("====== Rule Retrieve Debug ======")
        for r in results:
            print(f"[score={r.score}] sources={r.sources} rule_score={r.rule_score}")
            print(r.document.page_content)
            print("----")

    return results[:top_k]
