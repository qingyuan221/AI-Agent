from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.output_parsers.json import JsonOutputParser
from langchain_core.output_parsers.string import StrOutputParser

model =ChatTongyi(
    api_key="sk-9d8f8cb564b74b8b946a3549021a8a65",
    model = "qwen3-max",
    streaming=True,
)
first_prompt = PromptTemplate.from_template(
    "我姓{lastname},我的孩子是{gender}，"
    "请你给我孩子取个名字，要求封装为json格式,其中key是name，value是你取的名字"

)
second_prompt = PromptTemplate.from_template(
    "姓名{name},请你解析一下含义"
)
jsonparser = JsonOutputParser()
strparser = StrOutputParser()
chain = first_prompt|model|jsonparser|second_prompt|model|strparser
for chunk in chain.stream({"lastname":"张","gender":"女孩"}):
    print(chunk,end="",flush=True)