
import asyncio
import json
from openai import AsyncOpenAI

# 1. 定义工具库
def get_weather(city: str) -> str:
    """获取指定城市的实时天气。参数: city (str)"""
    weather_data = {"北京": "晴，25度", "上海": "小雨，20度", "深圳": "多云，28度"}
    return weather_data.get(city, f"{city}的天气数据暂未收录")

def get_current_time() -> str:
    """获取系统当前时间。不需要参数。"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 工具映射
TOOLS_MAP = {
    "get_weather": get_weather,
    "get_current_time": get_current_time
}

client = AsyncOpenAI(api_key="", base_url="https://open.bigmodel.cn/api/paas/v4")

async def run_smart_agent(user_query: str):
    # 模拟记忆：存放对话历史，让 AI 知道自己干了什么
    history = [
        {"role": "system", "content": f"""你是一个高级助理。可用工具：{list(TOOLS_MAP.keys())}。
        如果需要工具，请回复 JSON: {{"tool_name": "...", "args": {{...}}}}
        如果信息已齐全，请直接回答。
        注意：如果你发现参数缺失（如查天气没给城市），请直接询问用户。"""}
    ]
    history.append({"role": "user", "content": user_query})

    # 最多允许思考 3 轮，防止死循环
    for i in range(3):
        print(f"\n--- 💡 第 {i+1} 轮思考 ---")
        
        response = await client.chat.completions.create(
            model="glm-4",
            messages=history
        )
        
        ai_reply = response.choices[0].message.content
        history.append({"role": "assistant", "content": ai_reply})

        # 尝试解析是否为工具调用
        try:
            # 简单清洗：防止 AI 吐出 ```json ... ```
            clean_json = ai_reply.replace("```json", "").replace("```", "").strip()
            call_info = json.loads(clean_json)
            
            tool_name = call_info.get("tool_name")
            args = call_info.get("args", {})

            if tool_name in TOOLS_MAP:
                print(f"  执行工具: {tool_name}({args})")
                # 动态调用
                try:
                    observation = TOOLS_MAP[tool_name](**args)
                except TypeError as e:
                    observation = f"错误：参数不匹配。请确认是否遗漏了必要参数。详细描述：{e}"
                
                print(f"  观察结果: {observation}")
                # 将观察到的结果塞回历史，让 AI 进行下一轮判断
                history.append({"role": "system", "content": f"工具执行结果: {observation}"})
            else:
                print(f" AI 直接回答：{ai_reply}")
                break # 退出循环，展示结果

        except json.JSONDecodeError:
            # AI 返回的是自然语言，说明推理结束
            print(f" 最终结论：{ai_reply}")
            break

if __name__ == "__main__":
    # 测试案例 1：多步推理（北京和上海天气对比）
    # 测试案例 2：参数缺失（“帮我查一下天气”，看它是否会反问你哪个城市）
    query = input("请输入指令: ")
    asyncio.run(run_smart_agent(query))
