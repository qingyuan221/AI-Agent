from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import FakeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

# 加载文档
loader = TextLoader(r"D:\AI_Agent\doubao\text.txt", encoding="utf-8")
documents = loader.load()

# 文本分割
splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
)
chunks = splitter.split_documents(documents)

# 向量库初始化
embedding = FakeEmbeddings(size=384)
db = Chroma.from_documents(chunks, embedding)
retriever = db.as_retriever(search_kwargs={"k": 2})

# 初始化大模型（智谱 GLM）
llm = ChatOpenAI(
    api_key="",
    base_url="https://open.bigmodel.cn/api/paas/v4",
    model="glm-3-turbo"
)

# 提示词模板
prompt = PromptTemplate.from_template(
"""请严格依据下面知识库内容回答问题，禁止编造无关信息。
知识库内容：{context}
用户问题：{question}
"""
)

# 文档格式化
def format_docs(docs):
    return "\n".join([doc.page_content for doc in docs])

# ======================
# ✅ 这里是修复的核心！
# ======================
rag_chain = (
    RunnableParallel({
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    })
    | prompt
    | llm
    | StrOutputParser()
)

if __name__ == "__main__":
    q1 = "什么是RAG？"
    ans1 = rag_chain.invoke(q1)
    print("问题：", q1)
    print("回答：", ans1)
    print("-" * 50)

    q2 = "AI智能体有什么特点？"
    ans2 = rag_chain.invoke(q2)
    print("问题：", q2)
    print("回答：", ans2)