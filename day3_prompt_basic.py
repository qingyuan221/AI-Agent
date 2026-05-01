from openai import OpenAI
client = OpenAI(
    api_key="",
    base_url="https://open.bigmodel.cn/api/paas/v4"
)
messages = [
    {
        "role":"system",
        "content":"回答必须严格分三点：1.是什么；2.有什么用；3.在什么场景使用"
    }
]
while True:
    user_input = input("你: ")
    if user_input == "q":
        print("====对话结束====")
        break
    messages.append({"role":"user","content":user_input})

    res=client.chat.completions.create(
        model="glm-3-turbo",
        messages=messages

    ) 
    reply = res.choices[0].message.content
    print("AI:",reply)


    messages.append({"role":"assistant","content": reply})