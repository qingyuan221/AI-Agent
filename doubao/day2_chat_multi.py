from openai import OpenAI
client = OpenAI(
    api_key="1bf7ef3239fc4649825b4673e5731211.zamL3TFjqwMb2Tfy",
    base_url="https://open.bigmodel.cn/api/paas/v4"

)
messages = [
    {"role":"system","content":"你是AI智能体学习助手，回答简洁易懂"}
]
print("====开启对话====,输入q退出")
while True:
    user_input = input("你：")
    if user_input.lower() == 'q':
        print("====对话结束====")
        break
#把用户新问题加入对话
    messages.append({"role":"user","content":user_input})
#调用大模型
    res = client.chat.completions.create(
        model="glm-3-turbo",
        messages=messages
)
    ai_reply = res.choices[0].message.content
    print("AI:",ai_reply)
#把AI回复加入历史，形成记忆
    messages.append({"role":"assistant","content":ai_reply})