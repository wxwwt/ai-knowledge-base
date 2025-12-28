from typing import List
from langchain_core.documents import Document
from ex05_retrieve_result import RetrieveResult

import re
from typing import List

# 将自然语言 query 转成"高信息密度关键词"
# 去除掉噪声
def normalize_query(query: str) -> List[str]:
    """
    将自然语言 query 转成"高信息密度关键词"

    示例：
    - 什么是蓝精灵协议？ → ["蓝精灵协议"]
    - 请介绍一下 aurora-42 项目 → ["aurora-42", "项目"]
    """

    q = query.lower().strip()

    # 1. 去掉常见疑问/口水词
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

    # 2. 按空格 / 标点拆
    tokens = re.split(r"\s+|，|,|。|；|;", q)

    # 3. 去空 & 去短词
    tokens = [
        t.strip()
        for t in tokens
        if len(t.strip()) >= 2
    ]

    return tokens


# =========================
# 预置：模拟"知识库文档"
# （你之后会替换成你自己拆分的）
# =========================

DOCUMENTS: List[Document] = [
    Document(
        page_content="项目代号：Project Aurora-42。该项目于 2025-12-15 内部启动，目标是为一家中型制造企业构建私有化 AI 知识库系统。",
        metadata={
            "source": "internal_project_record.txt",
            "project": "aurora-42",
            "section": "项目背景",
            "doc_type": "内部项目记录"
        }
    ),
    Document(
        page_content="关键技术选型：后端语言 Python 3.12，LLM 运行方式为 Ollama 本地部署，向量数据库使用 Chroma，框架为 LangChain。",
        metadata={
            "source": "internal_project_record.txt",
            "project": "aurora-42",
            "section": "技术选型",
            "doc_type": "内部项目记录"
        }
    ),
    Document(
        page_content='特殊约定：Aurora-42 项目中，"蓝鲸协议"指的是一种内部定义的数据同步流程，与公开互联网无关。',
        metadata={
            "source": "internal_project_record.txt",
            "project": "Aurora-42",
            "section": "特殊约定",
            "doc_type": "protocol"
        }
    ),
     Document(
        page_content='特殊约定：Burora-52 项目中，"蓝精灵协议"指的是一种内部定义的数据同步流程，与公开互联网无关。',
        metadata={
            "source": "internal_project_record.txt",
            "project": "Burora-52",
            "section": "特殊约定",
            "doc_type": "protocol"
        }
    )
]


# =========================
# 核心接口（V2）
# =========================

def retrieve(query: str, top_k: int = 3) -> List[Document]:
    keywords = normalize_query(query)
    results: List[RetrieveResult] = []

    for doc in DOCUMENTS:
        score = 0
        hit_rules = []

        content_lower = doc.page_content.lower()

        # ---------- R1：内容关键词命中 ----------
        for kw in keywords:
            if kw in content_lower:
                score += 3
                hit_rules.append(f"content_hit:{kw}")

        # ---------- R2：项目名命中 ----------
        project = doc.metadata.get("project", "").lower()
        for kw in keywords:
            if kw in project:
                score += 2
                hit_rules.append(f"project_hit:{kw}")

        # ---------- R3：协议类文档 ----------
        if ("协议" in query or "protocol" in query.lower()) \
           and doc.metadata.get("doc_type") == "protocol":
            score += 2
            hit_rules.append("protocol_match")

        if score > 0:
            results.append(
                RetrieveResult(
                    document=doc,
                    score=score,
                    hit_rules=hit_rules
                )
            )

    # ---------- 排序 ----------
    results.sort(key=lambda x: x.score, reverse=True)

    # ---------- DEBUG（强烈建议你保留） ----------
    for r in results:
        print(f"[score={r.score}] rules={r.hit_rules}")
        print(r.document.page_content)
        print("----")

    return [r.document for r in results[:top_k]]

    """
    根据用户 query，使用规则检索相关 Document

    V1 版本特性：
    - 纯规则
    - 可解释
    - 不依赖向量
    """

    query_lower = query.lower()
    results: List[Document] = []

    # ---------- 规则 1：强规则（项目名直命中，短路） ----------
    if "aurora-42" in query_lower or "aurora 42" in query_lower:
        for doc in DOCUMENTS:
            if doc.metadata.get("project") == "aurora-42":
                results.append(doc)

        # 强规则命中，直接返回（短路）
        return results[:top_k]

    # ---------- 规则 2：关键词命中 ----------
    for doc in DOCUMENTS:
        content_lower = doc.page_content.lower()
        # 没有去除噪声的版本
        # if any(keyword in content_lower for keyword in query_lower.split()):
        # 去除噪声之后的版本
        keywords = normalize_query(query)
        if any(keyword in content_lower for keyword in keywords):
            results.append(doc)

    # ---------- 规则 3：metadata 过滤（简单示例） ----------
    if "协议" in query or "protocol" in query_lower:
        results = [
            doc for doc in results
            if doc.metadata.get("doc_type") == "protocol"
        ]

    # ---------- 规则 4：去重 ----------
    seen = set()
    unique_results = []
    for doc in results:
        key = doc.page_content
        if key not in seen:
            seen.add(key)
            unique_results.append(doc)

    # ---------- 规则 5：TopK 截断 ----------
    return unique_results[:top_k]

# 写一个main来测试这个类
if __name__ == "__main__":
    # query = "什么是aurora-42项目？"
    # results = retrieve(query)
    # print(results)
   
    # query = "什么是burora-52项目？"
    # results = retrieve(query)
    # print(results)

    query = "什么是蓝精灵协议？"
    results = retrieve(query)
    print(results)

    # query = "什么是蓝鲸协议？"
    # results = retrieve(query)
    # print(results)

    # query = "北京今天的天气怎么样"
    # results = retrieve(query)
    # print(results)

