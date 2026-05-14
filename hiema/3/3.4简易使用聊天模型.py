from langchain_community.chat_models.tongyi import ChatTongyi

model = ChatTongyi(
    api_key="sk-106e0de807ff42c4a5ff177598b5b3f0",
    model= "qwen3-max",
    streaming=True,
)
messages = [
    ("system","你是一个游离在外的的诗人"),
    ("human","请写一首唐诗"),
    ("ai","床前明月光，疑是地上霜，举头望明月，低头思故乡"),
    ("human","请仿照上述古诗，写一首唐诗")
]
res = model.stream(input=messages)
for chunk in res:
    print(chunk.content,end="",flush=True)