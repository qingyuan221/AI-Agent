from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi


prompt_template = PromptTemplate.from_template(
    "我的姓是{lastname},孩子是{gender},请你帮我取个名字,简单回答"
)
#prompt_text = prompt_template.format(lastname="张", gender="女")


model = Tongyi(
    model ="qwen-max",
    api_key="sk-9d8f8cb564b74b8b946a3549021a8a65",
)

#res = model.invoke(input=prompt_text)
#print(res)

chain = prompt_template |model
res = chain.invoke(input={"lastname":"张","gender":"女"})
print(res)
