from langchain_ollama import ChatOllama

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

def main():
    # 1. 创建模型（本地 Ollama）
    llm = ChatOllama(
        model="gemma3:1b",
        temperature=0.7,
    )

    # 2. 构造消息
    messages = [
         SystemMessage(content="你是一个严谨、简洁的技术助手"),
         HumanMessage(content="什么是 RAG？"),
         AIMessage(content="RAG 是一种将检索与生成结合的技术。"),
         HumanMessage(content="那它解决了什么问题？"),
    ]

    # 3. 调用模型
    response = llm.invoke(messages)

    # 4. 输出结果
    print(response.content)

if __name__ == "__main__":
    main()

