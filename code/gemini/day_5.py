import asyncio
import httpx
from openai import AsyncOpenAI
from typing import List, Dict

# 1. 基础配置
client = AsyncOpenAI(
    api_key="",
    base_url="https://open.bigmodel.cn/api/paas/v4"
)

async def fetch_news(topic: str) -> str:
    """
    使用 HTTP 请求从新闻接口获取数据
    """
    print(f"🌐 正在联网搜索关于 '{topic}' 的最新消息...")
    
    # 这里我们使用一个示例 API。实际开发中，你可以对接聚合数据、百度搜索等 API。
    # 为了演示，我们模拟一个 HTTP 请求过程
    async with httpx.AsyncClient() as http_client:
        try:
            # 模拟请求一个新闻聚合接口
            # response = await http_client.get(f"https://api.example.com/news?q={topic}")
            # news_data = response.json()
            
            # 模拟返回的 JSON 结构
            await asyncio.sleep(1) # 模拟网络延迟
            mock_news = [
                {"title": "2026年AI Agent市场规模突破千亿", "source": "科技日报"},
                {"title": "深度求索(DeepSeek)发布全新多模态模型", "source": "AI观察家"}
            ]
            
            # 将复杂的 JSON 转换成简单的文本字符串，方便喂给 AI
            news_text = "\n".join([f"- {n['title']} ({n['source']})" for n in mock_news])
            return news_text
        except Exception as e:
            return f"无法获取新闻数据: {e}"

async def news_summary_agent(topic: str):
    # 步骤 1: 联网获取原始数据
    raw_news = await fetch_news(topic)
    
    # 步骤 2: 将数据喂给 AI 进行分析总结
    prompt = f"""
    以下是从网络获取的关于 '{topic}' 的原始新闻列表：
    {raw_news}
    
    请根据以上内容，为我写一段 100 字左右的今日简报，要求语言生动且专业。
    """
    
    print("✍️  AI 正在处理数据并撰写简报...")
    response = await client.chat.completions.create(
        model="glm-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    result = response.choices[0].message.content
    print("\n" + "="*30)
    print(f"📰 【{topic}】今日简报：")
    print(result)
    print("="*30)

if __name__ == "__main__":
    topic = input("你想了解什么领域的最新消息？(如：人工智能)\n> ")
    asyncio.run(news_summary_agent(topic))