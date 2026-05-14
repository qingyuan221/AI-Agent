from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import FakeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
#1.加载本地文档
loader = TextLoader(r"D:\AI_Agent\doubao\text.txt", encoding="utf-8")
documents = loader.load()


#2.文档分块
splitters = RecursiveCharacterTextSplitter(
    chunk_size = 100,
    chunk_overlap = 20,
)
chunks = splitters.split_documents(documents)
#3.假嵌入+向量库
embedding = FakeEmbeddings(size=384)
db = Chroma.from_documents(chunks,embedding)
#4.转为检索器
retriever = db.as_retriever(search_kwargs = {"k":2})
#5.初始化大模型
llm = ChatOpenAI(
    api_key="",
    base_url="https://open.bigmodel.cn/api/paas/v4",
    model = "glm-3-turbo"
)
#6.RAG专用提示器模板
template = """
请严格根据下面的知识库内容回答问题，不要编造额外信息。
知识库内容：{context}
用户问题：{question}
"""
prompt = PromptTemplate(input_variables=["context","question"],template=template)
#7.构建RAG链
rag_chain =prompt |llm| StrOutputParser()
#8.提问检索生成回答
question = "什么是AI智能体"
#先检索相关文档
rel_docs = retriever.invoke(question)
#拼接上下文
context = "/n".join([doc.page_content for doc in rel_docs])
# 调用RAG链
ans = rag_chain.invoke({"context":context,"question":question})
print("用户问题,question")
print("-"*20)
print("AI回答:\n",ans)