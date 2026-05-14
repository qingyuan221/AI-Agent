from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter

# 测试文本
content = """
人工智能是一门新兴技术，大模型在RAG检索增强生成中应用广泛。
通过文本分割，可以把长文档切成小块，方便后续向量化存入向量数据库。
"""

# 文本分割器
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=30
)

# 执行分割
chunks = text_splitter.split_text(content)

# 输出结果
print("分割完成！")
for i, chunk in enumerate(chunks):
    print(f"\n第{i+1}块：{chunk}")

