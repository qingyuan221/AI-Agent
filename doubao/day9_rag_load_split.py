from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader
# 1.加载文本文件
loader = TextLoader(r"D:\AI_Agent\doubao\text.txt", encoding="utf-8")
doucuments = loader.load()




#2.初始化文本分割器
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 100,
    chunk_overlap = 20,
    length_function = len
)


#3.分割文档
chunks = splitter.split_documents(doucuments)




#4.输出结果
print(f"文档总块数:{len(chunks)}")
print("-"*50)
for i, chunks in enumerate(chunks):
    print(f"第{i+1}快内容：")
    print(chunks.page_content)
    print("-"*50)