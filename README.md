# AI Knowledge Base (RAG Demo)

这是一个用于学习和实践 **AI 应用开发 / RAG（Retrieval-Augmented Generation）** 的个人项目。

项目目标：
- 跑通完整的 RAG 流程
- 理解 LangChain 在 AI 应用中的角色
- 为后续 Agent / 多模型支持打基础

---

## 🚀 技术栈

- Python 3.10+
- LangChain
- Ollama（本地大模型）
- ChromaDB（向量数据库）

---

## 🧠 项目架构（第一阶段）

```text
文档 → Chunk → Embedding → Vector DB → Retrieval → LLM → Answer
```
