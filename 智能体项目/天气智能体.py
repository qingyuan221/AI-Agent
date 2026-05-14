import re
import json
import urllib.request
from openai import OpenAI

# --- 1. 配置LLM客户端 ---
API_KEY = "1bf7ef3239fc4649825b4673e5731211.zamL3TFjqwMb2Tfy"
BASE_URL = "https://open.bigmodel.cn/api/paas/v4"
MODEL_ID = "glm-3-turbo"

llm = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

# --- 可用工具定义 ---
def search_weather(city="北京"):
    """查询真实天气 - 使用 Open-Meteo 免费API（无需注册）"""
    # 城市坐标映射
    city_coords = {
        "北京": (39.9042, 116.4074),
        "上海": (31.2304, 121.4737),
        "广州": (23.1291, 113.2644),
        "深圳": (22.5431, 114.0579),
        "杭州": (30.2741, 120.1551),
        "成都": (30.5728, 104.0668),
        "武汉": (30.5928, 114.3055),
        "西安": (34.3416, 108.9398),
        "重庆": (29.4316, 106.9123),
        "南京": (32.0603, 118.7969),
        "天津": (39.3434, 117.3616),
        "苏州": (31.2989, 120.5853),
    }
    
    if city not in city_coords:
        supported = "、".join(city_coords.keys())
        return f"暂不支持查询 {city}，目前支持：{supported}"
    
    lat, lon = city_coords[city]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code,wind_speed_10m&timezone=Asia/Shanghai"
    
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
        
        current = data["current"]
        temp = current["temperature_2m"]
        wind = current["wind_speed_10m"]
        code = current["weather_code"]
        
        # 天气码转中文
        weather_map = {
            0: "晴朗", 1: "大致晴朗", 2: "多云", 3: "阴天",
            45: "雾", 48: "雾凇",
            51: "小毛毛雨", 53: "中毛毛雨", 55: "大毛毛雨",
            61: "小雨", 63: "中雨", 65: "大雨",
            71: "小雪", 73: "中雪", 75: "大雪",
            80: "阵雨", 81: "中阵雨", 82: "大阵雨",
            95: "雷暴", 96: "雷暴加冰雹", 99: "雷暴大冰雹"
        }
        weather = weather_map.get(code, f"代码{code}")
        
        return f"{city}当前天气：{weather}，气温{temp}°C，风速{wind}km/h。天气代码：{code}"
    except Exception as e:
        return f"查询失败：{str(e)}"

def recommend_place(weather_code):
    """根据天气代码推荐地点"""
    sunny = [0, 1]
    cloudy = [2, 3, 45, 48]
    rainy = [51, 53, 55, 61, 63, 65, 80, 81, 82]
    snowy = [71, 73, 75]
    stormy = [95, 96, 99]
    
    places = {
        "sunny": ["故宫", "长城", "天坛", "颐和园"],
        "cloudy": ["国家博物馆", "798艺术区", "三里屯"],
        "rainy": ["国家大剧院", "故宫博物院（室内）", "中国科技馆"],
        "snowy": ["故宫（雪景）", "雍和宫", "什刹海"],
        "stormy": ["建议室内活动", "购物中心", "博物馆"]
    }
    
    if weather_code in sunny:
        return "晴天推荐室外景点：" + "、".join(places["sunny"])
    elif weather_code in cloudy:
        return "多云推荐景点：" + "、".join(places["cloudy"])
    elif weather_code in rainy:
        return "雨天建议室内活动：" + "、".join(places["rainy"])
    elif weather_code in snowy:
        return "雪天推荐雪景：" + "、".join(places["snowy"])
    else:
        return "恶劣天气建议：" + "、".join(places["stormy"])

def calculator(expression):
    """安全计算器"""
    if re.match(r'^[\d\+\-\*\/\.\(\)\s]+$', expression):
        try:
            result = eval(expression)
            return str(result)
        except:
            return "计算错误"
    return "非法表达式"

available_tools = {
    "search_weather": search_weather,
    "recommend_place": recommend_place,
    "calculator": calculator,
}

# --- Agent System Prompt ---
AGENT_SYSTEM_PROMPT = """你是一个智能助手。请严格遵循以下格式回复：

Thought: 分析用户请求，决定下一步行动
Action: 工具名(参数名="参数值")

可用工具：
- search_weather(city="城市名")：查询真实天气，返回格式："城市当前天气：XX，气温XX°C，风速XXkm/h。天气代码：XX"
- recommend_place(weather_code="数字")：根据天气代码推荐景点，天气代码含义：0-1晴天，2-3多云/阴天，51-55毛毛雨，61-65雨，71-75雪，80-82阵雨，95-99雷暴
- calculator(expression="表达式")：执行数学计算

注意：recommend_place 需要传入天气代码（数字），不是天气描述！

当任务完成时，使用：
Action: Finish[最终答案]

示例对话：
用户: 北京天气怎么样？
Thought: 用户想查北京天气，用search_weather工具
Action: search_weather(city="北京")

用户: 根据天气代码3推荐景点
Thought: 天气代码3是多云/阴天，用recommend_place工具
Action: recommend_place(weather_code="3")
"""


# --- 2. 主循环 ---
def run_agent(user_prompt, max_loops=10):
    prompt_history = [f"用户请求: {user_prompt}"]
    print(f"用户输入: {user_prompt}\n" + "="*40)

    for i in range(max_loops):
        print(f"--- 循环 {i+1} ---\n")
        
        full_prompt = "\n".join(prompt_history)

        llm_output = llm.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": AGENT_SYSTEM_PROMPT},
                {"role": "user", "content": full_prompt}
            ]
        ).choices[0].message.content

        # 截断多余的 Thought-Action
        match = re.search(
            r'(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)',
            llm_output, re.DOTALL
        )
        if match:
            truncated = match.group(1).strip()
            if truncated != llm_output.strip():
                llm_output = truncated
                print("已截断多余的 Thought-Action 对")

        print(f"模型输出:\n{llm_output}\n")
        prompt_history.append(llm_output)

        action_match = re.search(r"Action: (.*)", llm_output, re.DOTALL)
        if not action_match:
            observation = "错误: 未能解析到 Action 字段"
            observation_str = f"Observation: {observation}"
            print(f"{observation_str}\n" + "="*40)
            prompt_history.append(observation_str)
            continue

        action_str = action_match.group(1).strip()

        if action_str.startswith("Finish"):
            final_answer = re.match(r"Finish\[(.*)\]", action_str).group(1)
            print(f"✅ 任务完成，最终答案: {final_answer}")
            return final_answer

        tool_name = re.search(r"(\w+)\(", action_str).group(1)
        kwargs = dict(re.findall(r'(\w+)="([^"]*)"', action_str))

        if tool_name in available_tools:
            observation = available_tools[tool_name](**kwargs)
        else:
            observation = f"错误: 未定义的工具 '{tool_name}'"

        observation_str = f"Observation: {observation}"
        print(f"{observation_str}\n" + "="*40)
        prompt_history.append(observation_str)

    return "达到最大循环次数，任务未完成"


# --- 3. 运行 ---
if __name__ == "__main__":
    print("="*50)
    print("🤖 智能助手已启动（输入 'quit' 或 'q' 退出）")
    print("="*50)
    
    while True:
        user_prompt = input("\n👤 你: ").strip()
        
        if user_prompt.lower() in ['quit', 'q', 'exit', '退出']:
            print("👋 再见！")
            break
        
        if not user_prompt:
            continue
            
        run_agent(user_prompt)
