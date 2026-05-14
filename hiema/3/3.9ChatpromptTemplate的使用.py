from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi


chat_prompt_template = ChatPromptTemplate(
    [
        ("system","你是一个诗人"),
        MessagesPlaceholder("history"),
        ("human","再写一首唐诗"),
    ]
)
history_date = [
    ("human","你来写一首唐诗"),
    ("ai","床前明月光，疑是地上霜，举头望明月，低头思故乡"),
    ("human","好诗好诗，再来一首"),
    ("ai","锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦"),
]
prompt_text = chat_prompt_template.invoke({"history":history_date}).to_string()

#print(prompt_text)
model = ChatTongyi(
    api_key="sk-9d8f8cb564b74b8b946a3549021a8a65",
    model = "qwen3-max",
)
res = model.invoke(input=prompt_text)
print(res.content)