from langchain_openai import ChatOpenAI
llm = ChatOpenAI(
    api_key="",
    base_url="https://open.bigmodel.cn/api/paas/v4",
    model="glm-3-turbo"
)
res = llm.invoke("学习AI智能体要按照什么顺序来学？")
print(res.content)