from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser

# 1. 初始化大模型
llm = ChatOpenAI(
    api_key="",
    base_url="https://open.bigmodel.cn/api/paas/v4",
    model="glm-3-turbo"
)

# 2. 自定义工具
@tool
def calculator(expr: str) -> str:
    """数学表达式计算，输入格式示例：3*9+15"""
    try:
        return f"计算结果：{eval(expr)}"
    except:
        return "表达式格式错误"

tools = [calculator]
llm = llm.bind_tools(tools)

# 3. 构建带历史对话的提示词
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是带记忆的智能体，记住上下文对话，合理调用工具完成需求"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

# 4. LCEL组装对话链
chat_chain = prompt | llm | StrOutputParser()

# 5. 存放对话历史
chat_history = []

# 6. 多轮对话交互
if __name__ == "__main__":
    print("✅ 带记忆智能体启动，输入exit退出对话\n")
    while True:
        user_input = input("你：")
        if user_input.lower() == "exit":
            print("智能体：再见！")
            break
        
        # 调用链传入历史对话
        res = chat_chain.invoke({
            "input": user_input,
            "chat_history": chat_history
        })
        
        print("智能体：", res)
        # 追加对话记录，存入记忆
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=res))