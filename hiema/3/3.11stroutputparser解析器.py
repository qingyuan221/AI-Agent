from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
model = ChatTongyi(
    api_key="sk-9d8f8cb564b74b8b946a3549021a8a65",
    model = "qwen3-max",

)
parser = StrOutputParser()
prompt_template = PromptTemplate.from_template("我姓{lastname},我的孩子是{gender},请你给我的孩子取一个名字，只需要名字就好")
chain = prompt_template|model|parser |model|parser
res = chain.invoke({"lastname":"张","gender":"女生"})
print(res,type(res))