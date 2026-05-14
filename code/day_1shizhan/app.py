import json
from openai import OpenAI
from models import MovieInfo  # 导入刚才定义的模型

# 1. 初始化配置 (建议使用你的密钥)
client = OpenAI(
    api_key="",
    base_url="https://open.bigmodel.cn/api/paas/v4"
)

def get_movie_agent(movie_name: str):
    # 2. 构造 Prompt：核心是要求返回 JSON
    prompt = f"""你是一个电影数据分析员。
请搜索并分析电影《{movie_name}》的信息。
必须以 JSON 格式返回，严禁包含任何解释性文字。
JSON 结构如下：
{{
    "title": "电影名",
    "director": "导演",
    "rating": 评分数字,
    "tags": ["标签1", "标签2"],
    "summary": "不少于10个字的简介"
}}"""

    # 3. 调用模型
    response = client.chat.completions.create(
        model="glm-4", # 建议使用更强的模型确保JSON格式正确
        messages=[{"role": "user", "content": prompt}]
    )

    raw_content = response.choices[0].message.content
    
    # 4. 核心挑战：解析与校验
    try:
        # 去掉可能存在的 Markdown 代码块标记 ```json ... ```
        clean_json = raw_content.replace("```json", "").replace("```", "").strip()
        
        # 验证 JSON 并转换为 Pydantic 对象
        movie_data = MovieInfo.model_validate_json(clean_json)
        
        print("✅ 成功提取结构化数据：")
        print(f"电影：{movie_data.title} | 导演：{movie_data.director}")
        print(f"标签：{' / '.join(movie_data.tags)}")
        print(f"简介：{movie_data.summary}")
        
    except Exception as e:
        print(f"❌ 数据解析失败！AI 返回了非规范格式。")
        print(f"原始返回内容：{raw_content}")
        print(f"错误原因：{e}")

if __name__ == "__main__":
    name = input("请输入你想查询的电影名：")
    get_movie_agent(name)