from langchain_community.llms.tongyi import Tongyi
model = Tongyi(
    api_key="sk-9d8f8cb564b74b8b946a3549021a8a65",
    model = "qwen-max"
)
res = model.stream(input = "你是谁能干什么")
for chunk in res:
    print(chunk,end="",flush=True)