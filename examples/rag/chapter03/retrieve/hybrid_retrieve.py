# rag/retrieve/hybrid_retrieve.py

from typing import List
from langchain_core.documents import Document
from examples.rag.chapter03.retrieve.models import HybridRetrieveItem
from examples.rag.chapter03.retrieve.rule_retrieve import retrieve as rule_retrieve
from examples.rag.chapter03.retrieve.vector_retrieve import vector_retrieve


def hybrid_retrieve(
    query: str,
    documents: List[Document],
    top_k_rule: int = 5,
    top_k_vector: int = 5,
    debug: bool = False
) -> List[HybridRetrieveItem]:
    """
    Hybrid Recall：
    - Rule Retrieve
    - Vector Retrieve
    - 合并 + 去重 + 标注来源
    """

    hybrid_map = {}

    # ---------- 1. 规则召回 ----------
    rule_results = rule_retrieve(
        query=query,
        documents=documents,
        top_k=top_k_rule,
        debug=debug
    )

    for r in rule_results:
        key = r.document.page_content
        hybrid_map[key] = HybridRetrieveItem(
            document=r.document,
            score=r.score,
            rule_score=r.score,
            vector_score=None,
            sources=["rule"]
        )

    # ---------- 2. 向量召回 ----------
    vector_results = vector_retrieve(
        query=query,
        documents=documents,
        top_k=top_k_vector
    )

    # vector_retrieve 返回 List[Document]，暂时使用固定分数
    # 后续可以改进为返回带分数的结果
    for doc in vector_results:
        key = doc.page_content
        # 暂时使用固定分数，后续可以从 similarity_search_with_score 获取
        vec_score = 1.0

        if key in hybrid_map:
            item = hybrid_map[key]
            item.vector_score = vec_score
            if "vector" not in item.sources:
                item.sources.append("vector")
            # 简单合并分数（先不纠结公式）
            item.score += vec_score
        else:
            hybrid_map[key] = HybridRetrieveItem(
                document=doc,
                score=vec_score,
                rule_score=None,
                vector_score=vec_score,
                sources=["vector"]
            )

    results = list(hybrid_map.values())

    if debug:
        print("====== Hybrid Recall Result ======")
        for r in results:
            print(
                f"score={r.score:.3f} "
                f"sources={r.sources} "
                f"rule={r.rule_score} "
                f"vector={r.vector_score}"
            )
            print(r.document.page_content)
            print("----")

    return results
