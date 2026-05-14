
import asyncio
import json
from openai import AsyncOpenAI

# 1. 定义工具函数（注意：详细的文档注释是关键）
def calculate_investment(amount: float, years: int, rate: float = 0.05) -> str:
    """
    计算投资预期收益。
    参数:
    amount: 初始投资金额
    years: 投资年限
    rate: 年化收益率，默认 0.05
    """
    result = amount * (1 + rate) ** years
    return f"预计 {years} 年后的总额为: {result:.2f} 元"

def get_weather(city: str) -> str:
    """
    获取指定城市的实时天气。
    参数:
    city: 城市名称
    """
    # 这里模拟一个 API 返回，实际开发中会用 httpx 请求天气接口
    weather_data = {"北京": "晴，25度", "上海": "小雨，20度", "深圳": "多云，28度"}
    return f"{city} 的当前天气是：{weather_data.get(city, '未知，暂未录入该城市')}"

# 2. 工具映射字典（Agent 的“技能书”）
TOOLS_MAP = {
    "calculate_investment": calculate_investment,
    "get_weather": get_weather
}

# 3. 初始化客户端
client = AsyncOpenAI(
    api_key="", 
    base_url="https://open.bigmodel.cn/api/paas/v4"
)

async def run_agent(user_query: str):
    # 构建 Prompt，告诉 AI 它拥有哪些工具
    system_prompt = f"""你是一个智能助理。你拥有以下工具：
    1. calculate_investment: 计算投资收益
    2. get_weather: 查询天气
    
    如果用户的问题需要用到工具，请严格按照以下 JSON 格式返回，不要有其他文字：
    {{ "tool_name": "工具名", "args": {{ "参数名": "值" }} }}
    
    如果不需要工具，请直接回答用户。
    """

    response = await client.chat.completions.create(
        model="glm-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]
    )

    ai_reply = response.choices[0].message.content
    print(f" AI 的初步思考: {ai_reply}")

    # 4. 逻辑调度：解析 AI 的决定
    try:
        # 尝试解析 JSON
        call_info = json.loads(ai_reply.replace("```json", "").replace("```", "").strip())
        tool_name = call_info.get("tool_name")
        args = call_info.get("args")

        if tool_name in TOOLS_MAP:
            print(f" 正在调用工具: {tool_name}，参数: {args}")
            # 动态调用函数并解包参数
            result = TOOLS_MAP[tool_name](**args)
            print(f" 工具执行结果: {result}")
            
            # 5. 二次总结：将工具结果反馈给 AI 生成自然语言回复
            final_res = await client.chat.completions.create(
                model="glm-4",
                messages=[
                    {"role": "system", "content": "请根据工具提供的数据给用户一个友好的回复。"},
                    {"role": "user", "content": f"用户问题: {user_query}\n工具执行结果: {result}"}
                ]
            )
            print(f" AI 最终回复: {final_res.choices[0].message.content}")
        else:
            print(f" AI 输出了无效的工具名。")
    except json.JSONDecodeError:
        # 如果不是 JSON，说明 AI 直接回答了
        print(f" AI 直接回复: {ai_reply}")

if __name__ == "__main__":
    query = input("有什么可以帮您的？(例如:帮我算算存10万块5年后的收益)\n> ")
    asyncio.run(run_agent(query))