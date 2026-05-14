from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import FakeEmbeddings
from langchain_community.vectorstores import Chroma
#1.加载文档
loader = TextLoader(r"D:\AI_Agent\doubao\text.txt", encoding="utf-8")
documents = loader.load()
#2.文本分割
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 100,
    chunk_overlap = 20,
)
chunks = splitter.split_documents(documents)
print(f"文本分割为{len(chunks)}")
#3.初始化嵌入
embedding = FakeEmbeddings(size = 384)
#4.存入向量库
db = Chroma.from_documents(chunks,embedding)
print("已全部存入")
#5.相似度检索
query = "什么是RAG"
result_docs = db.similarity_search(query,k=2)
print("用户提问:",query)
