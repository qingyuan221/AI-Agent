from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import AIMessage,HumanMessage,SystemMessage 
mdoel = ChatTongyi(
    api_key="sk-106e0de807ff42c4a5ff177598b5b3f0",
    model= "qwen3-max",
    streaming=True,
)
messages = [
    SystemMessage(content="你是一个游离在外的的诗人"),
    HumanMessage(content="请写一首唐诗"),
    AIMessage(content="床前明月光，疑是地上霜，举头望明月，低头思故乡"),
    HumanMessage(content="仿照上述古诗，写一首唐诗"),


]
res = mdoel.stream(input=messages)
for a in res:
    print(a.content,end="",flush=True)