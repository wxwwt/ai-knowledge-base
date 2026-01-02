# rag/index/vector_store.py

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from typing import List

_COLLECTION_NAME = "rag_v1"

_vectorstore = None

def get_vectorstore(documents: List[Document] | None = None) -> Chroma:
    global _vectorstore

    if _vectorstore is not None:
        return _vectorstore

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    if documents is None:
        # 后面阶段可以 load 本地持久化
        raise ValueError("First time init requires documents")

    _vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name=_COLLECTION_NAME
    )

    return _vectorstore
