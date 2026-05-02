from openai import OpenAI
client = OpenAI(
    api_key="1bf7ef3239fc4649825b4673e5731211.zamL3TFjqwMb2Tfy",
    base_url="https://open.bigmodel.cn/api/paas/v4/"

)
messages = [
    {
        "role":"system",
        "content":"你只要输出标准json字符串，不要解释，不要多余解释，不要markdown"
        "固定三个字段：title、definition、application"

    }

]
while True:
    user_input = input("你:")
    if user_input == "q":
        print("对话结束")
        break
    messages.append({"role":"user","content":user_input})
    res = client.chat.completions.create(
        model = "glm-3-turbo",
        messages = messages
    )
    reply = res.choices[0].message.content
    print("AI:",reply)
    messages.append({"role":"assistant","content":reply})

