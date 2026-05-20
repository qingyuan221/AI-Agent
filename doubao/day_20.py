from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import FakeEmbeddings
from langchain_community.vectorstores import Chroma

# 1. 大模型
llm = ChatOpenAI(
    api_key="",
    base_url="https://open.bigmodel.cn/api/paas/v4",
    model = "glm-3-turbo",
)

# 2. RAG 知识库
loader = TextLoader(r"D:\AI_Agent\doubao\text.txt", encoding="utf-8")
documents = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
chunks = splitter.split_documents(documents)
embedding = FakeEmbeddings(size=384)
db = Chroma.from_documents(chunks, embedding)
retriever = db.as_retriever(k=2)

def get_rag_context(q):
    docs = retriever.invoke(q)
    return "\n".join([d.page_content for d in docs])

# 3. 工具定义
@tool
def calculate(expression: str) -> str:
    """数学计算工具，支持加减乘除"""
    try:
        return f"计算结果：{eval(expression)}"
    except:
        return "计算错误"

@tool
def query_knowledge(question: str) -> str:
    """查询本地知识库"""
    return get_rag_context(question)

tools = [calculate, query_knowledge]
tool_map = {
    "calculate": calculate,
    "query_knowledge": query_knowledge
}

# 4. 智能体 = 模型自动调用 + 执行工具 + 返回答案
def agent_run(user_input, chat_history):
    # 加入用户问题
    chat_history.append(HumanMessage(content=user_input))
    
    # 第一步：模型判断要调用什么工具
    response = llm.bind_tools(tools).invoke(chat_history)
    
    # 第二步：如果调用了工具，就执行
    tool_calls = response.tool_calls
    if tool_calls:
        for call in tool_calls:
            tool_name = call["name"]
            tool_args = call["args"]
            tool_result = tool_map[tool_name].invoke(tool_args)
            
            # 把工具结果返回给模型
            chat_history.append(response)
            chat_history.append(ToolMessage(tool_result, tool_call_id=call["id"]))
        
        # 第三步：模型根据工具结果，生成最终回答
        final_answer = llm.invoke(chat_history)
    else:
        # 不用工具，直接回答
        final_answer = response

    chat_history.append(AIMessage(content=final_answer.content))
    return final_answer.content

# 5. 启动对话
if __name__ == "__main__":
    chat_history = []
    print(" 第20天：任务拆解智能体")
    while True:
        user = input("你：")
        if user.lower() == "exit":
            break
        ans = agent_run(user, chat_history)
        print("AI：", ans)