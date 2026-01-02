from typing import List
from langchain_core.documents import Document
from ..index.vector_store import get_vectorstore

def vector_retrieve(
    query: str,
    documents: List[Document],
    top_k: int = 3
) -> List[Document]:
    """
    向量召回（V1）

    特点：
    - 只负责“找相似”
    - 不负责业务规则
    - 不做排序策略
    """

    vectorstore = get_vectorstore(documents)

    results = vectorstore.similarity_search(
        query=query,
        k=top_k
    )

    return results

if __name__ == "__main__":
    
    DOCUMENTS: list[Document] = [
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
    query = "什么是蓝精灵协议？"
    results = vector_retrieve(query, DOCUMENTS)
    print(results)