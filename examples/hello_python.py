from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen3:4b",
)

response = llm.invoke("用一句话解释什么是 LangChain")
print(response.content)
