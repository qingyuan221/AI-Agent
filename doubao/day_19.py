from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_community.embeddings import FakeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.tools import tool


#1.初始化大模型
llm = ChatOpenAI(
   api_key="",
    base_url="https://open.bigmodel.cn/api/paas/v4",
    model = "glm-3-turbo",
)
#2.构建rag
#加载文本数据
loader = TextLoader(
    file_path="./doubao/text.txt",
    encoding="utf-8",
)
doc = loader.load()
#文本分割
splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,     #文本分块最大数
    chunk_overlap=20,   #文本允许的最大重复数
    separators=["\n\n","\n"," ", ""],   #文本分割符
    length_function=len,  #统计文本长度
)
chunks = splitter.split_documents(doc)

#向量库

embeddings = FakeEmbeddings(size=284)
vector_db = Chroma.from_documents(chunks,embeddings)
retriever = vector_db.as_retriever(search_kwargs={"k": 2})
#拼接检索工程
def get_knowledge(query: str) -> str:
    res_docs = retriever.invoke(query)
    return "\n".join([d.page_content for d in res_docs])


#3调用工具
def calculate(expr: str) -> str:
    """进行数学运算，传入加减乘除表达式，例：100-20*3"""
    try:
        return f"运算结果：{eval(expr)}"
    except:
        return "表达式错误，无法计算"

@tool
def search_knowledge(question: str) -> str:
    """查询本地知识库内容，用于解答RAG、智能体相关专业问题"""
    return get_knowledge(question)

tools = [calculate, search_knowledge]
llm_bind = llm.bind_tools(tools)

# 4. 带记忆+知识库+工具 提示词
# ======================
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是全能智能体，可调用计算工具、知识库查询工具，同时记住聊天上下文，回答简洁准确"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{user_input}")
])
strparser = StrOutputParser()
#5.chain链
chain = prompt | llm_bind |strparser

#存储记忆对话
chat_history = []

# 5. 交互运行
# ======================
if __name__ == "__main__":
    print("🚀 知识库融合智能体启动，输入 exit 退出\n")
    while True:
        user_text = input("你：")
        if user_text.lower() == "exit":
            print("智能体：拜拜~")
            break
        
        answer = chain.invoke({
            "user_input": user_text,
            "history": chat_history
        })
        print("智能体：", answer)
        
        # 保存对话记忆
        chat_history.append(HumanMessage(content=user_text))
        chat_history.append(AIMessage(content=answer))