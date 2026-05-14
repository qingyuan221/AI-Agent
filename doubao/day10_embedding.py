from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import SentenceTransformerEmbeddings

# 1. 加载文档
loader = TextLoader(r"D:\AI_Agent\doubao\text.txt", encoding="utf-8")
documents = loader.load()

# 2. 文本分割
splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)
chunks = splitter.split_documents(documents)

# 3. 嵌入模型（向量化）
embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# 4. 把第一块文本转成向量
vec = embedding.embed_query(chunks[0].page_content)

# 5. 输出
print(f"文档块数：{len(chunks)}")
print(f"向量维度：{len(vec)}")
print("向量前10个数字：")
print(vec[:10])