from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.string import StrOutputParser

#1.初始化模型
llm = ChatOpenAI(
    api_key="1bf7ef3239fc4649825b4673e5731211.zamL3TFjqwMb2Tfy",
    base_url="https://open.bigmodel.cn/api/paas/v4",
    model="glm-3-turbo",
    streaming=True,
    model_kwargs={"stream": True}
)
#2.定义提示词
prompt = ChatPromptTemplate.from_template("""
你现在是一个基础AI智能体，具备理解问题、简单思考和自然回答的能力。
请先思考用户问题，再给出清晰完整的回答。

用户问题：{question}
""")
strparser = StrOutputParser()

chain = prompt|llm|strparser

  # 只打印一次
for chunk in chain.stream({"question": "解释一下什么是AI智能体，和普通聊天机器人有什么区别？"}):
    print(chunk, end="", flush=True)       # 只打字，不打标题