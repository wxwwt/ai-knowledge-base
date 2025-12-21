from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

def main():
    # 1. 创建模型（本地 Ollama）
    llm = ChatOllama(
        model="gemma3:1b",
        temperature=0.7,
    )

    system_message = """
你是一个遵循 ReAct 格式的助手。
回答时必须严格按照以下格式：

Thought: 你的内部思考（简短）
Answer: 给用户的最终回答
"""

    user_message = "为什么 LLM 需要 system / user / assistant 这三种角色？"

    # 2. 构造消息
    messages = [
         SystemMessage(content=system_message),
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

