from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

def main():
    # 1. 创建模型（本地 Ollama）
    llm = ChatOllama(
        model="gemma3:1b",
        temperature=0.7,
    )

#     system_message = """
# 你只能根据提供的上下文回答。
# 如果上下文中没有相关信息，必须原样输出：

# Thought: 我不知道
# Answer: 我不知道

# 禁止使用常识、猜测、历史经验、训练数据。
# """

#     user_message = "什么是project 23协议"


    KNOWLEDGE_BASE = """
【内部项目记录】

项目代号：Project Aurora-42

该项目于 2025-12-15 内部启动，目标是为一家
中型制造企业构建私有化 AI 知识库系统。

关键技术选型：
- 后端语言：Python 3.12
- LLM 运行方式：Ollama 本地部署
- 向量数据库：Chroma
- 框架：LangChain

特殊约定：
Aurora-42 项目中，“蓝鲸协议”指的是一种
内部定义的数据同步流程，与公开互联网无关。
"""

    system_message = f"""
System:
你只能根据以下 Context 回答问题。
Context:
{KNOWLEDGE_BASE}

你是一个遵循 ReAct 格式的助手。
回答时必须严格按照以下格式：

Thought: 你的内部思考（简短）
Answer: 给用户的最终回答
"""

    user_message = "aurora-42是在哪一天启动的？"

    # 2. 构造消息
    messages = [
        #  SystemMessage(content=system_message),
         HumanMessage(content=user_message),
    ]

    # 3. 调用模型
    response = llm.invoke(messages)

    # 4. 输出结果
    _, answer = parse_response(response.content)
    print(answer)

def parse_response(text: str):
    thought_lines = []
    answer_lines = []

    current = None

    for line in text.splitlines():
        if line.startswith("Thought:"):
            current = "thought"
            thought_lines.append(line.replace("Thought:", "").strip())
        elif line.startswith("Answer:"):
            current = "answer"
            answer_lines.append(line.replace("Answer:", "").strip())
        else:
            if current == "thought":
                thought_lines.append(line)
            elif current == "answer":
                answer_lines.append(line)

    thought = "\n".join(thought_lines).strip()
    answer = "\n".join(answer_lines).strip()

    print(f"Thought: {thought}")
    print(f"Answer: {answer}")

    return thought, answer


if __name__ == "__main__":
    main()

