from langchain_community.llms.tongyi import Tongyi
model = Tongyi(
    api_key="",
    model="qwen-max",
)
res = model.invoke("你是谁能干什么")
print (res)