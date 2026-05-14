from langchain_community.embeddings import DashScopeEmbeddings

model = DashScopeEmbeddings(
    dashscope_api_key="",
)

print(model.embed_query("你爱我"))
print(model.embed_documents("你爱我，我爱你，蜜雪冰城甜蜜蜜"))

