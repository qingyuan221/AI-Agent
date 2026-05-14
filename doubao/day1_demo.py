from openai import OpenAI

# 填入你自己申请的API密钥
client = OpenAI(
    api_key="",
    base_url="https://open.bigmodel.cn/api/paas/v4"
)

# 单轮大模型基础调用
response = client.chat.completions.create(
    model="glm-4",
    messages=[
        {"role":"system","content":"你是通俗易懂的老师，用大白话解释"},
        {"role":"user","content":"讲解一下想要通过智能体开发找到工作，需要具备哪些技能？"
        ""}
    ]
)

# 打印输出结果
print(response.choices[0].message.content)
print(response)