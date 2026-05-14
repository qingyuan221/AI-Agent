import asyncio
from openai import AsyncOpenAI  # 注意：这里改用了异步客户端

# 1. 异步配置
client = AsyncOpenAI(
    api_key="1bf7ef3239fc4649825b4673e5731211.zamL3TFjqwMb2Tfy", 
    base_url="https://open.bigmodel.cn/api/paas/v4"
)

async def ask_ai_streaming(prompt: str):
    """
    异步流式调用函数
    """
    print("AI 正在思考...", end="\r")
    
    try:
        # 使用 await 发起异步请求
        response = await client.chat.completions.create(
            model="glm-4",
            messages=[{"role": "user", "content": prompt}],
            stream=True  # 开启流式传输，这是 2026 年所有 AI 应用的标配
        )

        print("AI：", end="", flush=True)
        full_reply = ""

        # 异步迭代流式数据
        async for chunk in response:
            content = chunk.choices[0].delta.content or ""
            if content:
                full_reply += content
                print(content, end="", flush=True) # 实现逐字蹦出的效果
        
        print("\n" + "-"*30)
        return full_reply

    except Exception as e:
        print(f"\n❌ 异步调用发生错误: {e}")

async def main():
    while True:
        user_input = input("\n你 (输入 q 退出): ")
        if user_input.lower() == 'q':
            break
        
        # 运行异步任务
        await ask_ai_streaming(user_input)

if __name__ == "__main__":
    # 启动 Python 的异步事件循环
    asyncio.run(main())
