from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi


chat_prompt_temolate = ChatPromptTemplate([
    ("system","你是一个诗人"),
    MessagesPlaceholder("history"),
    ("human","请做一首唐诗"),
]
)

history_data = [
    ("human","你来写一首唐诗"),
    ("ai","床前明月光，疑是地上霜，举头望明月，低头思故乡"),
    ("human","好诗好诗，再来一首"),
    ("ai","锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦"),
]

#text = chat_prompt_temolate.invoke({"history":history_data}).to_string
#print(text)
model = ChatTongyi(
    api_key="sk-9d8f8cb564b74b8b946a3549021a8a65",
    model = "qwen3-max",
    streaming=True
)
chain = chat_prompt_temolate| model 
#res = chain.invoke({"history":history_data})
#print(res.content)
for chunk in chain.stream({"history":history_data}):
    print(chunk.content,end="",flush=True)