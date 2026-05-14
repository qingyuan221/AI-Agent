from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import FakeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ======================
# 1. 加载 + 分割文档
# ======================
loader = TextLoader(r"D:\AI_Agent\doubao\text.txt", encoding="utf-8")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
chunks = splitter.split_documents(documents)

# ======================
# 2. 向量库
# ======================
embedding = FakeEmbeddings(size=384)
db = Chroma.from_documents(chunks, embedding)
retriever = db.as_retriever(search_kwargs={"k": 2})

# ======================
# 3. 大模型
# ======================
llm = ChatOpenAI(
    api_key="",
    base_url="https://open.bigmodel.cn/api/paas/v4",
    model="glm-3-turbo"
)

# ======================
# 4. RAG 提示词
# ======================
template = """
根据以下知识库内容回答问题，不要编造。

知识库：{context}
问题：{question}

回答：
"""
prompt = PromptTemplate(input_variables=["context", "question"], template=template)

# ======================
# 5. 新版 RAG 链式（无弃用包）
# ======================
def format_docs(docs):
    return "\n".join([doc.page_content for doc in docs])

# 构建 RAG 链
rag_chain = (
    {
        "context": lambda x: format_docs(retriever.invoke(x["question"])),
        "question": lambda x: x["question"]
    }
    | prompt
    | llm
    | StrOutputParser()
)

# ======================
# 6. 提问
# ======================
question = "什么是RAG？"
result = rag_chain.invoke({"question": question})

print("问题：", question)
print("-" * 50)
print("回答：", result)