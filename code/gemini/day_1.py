from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

# 定义一个简历提取结果的模型（这是你未来 Agent 的输出标准）
class ResumeStandard(BaseModel):
    name: str = Field(..., description="姓名")
    years_of_exp: int = Field(..., ge=0, description="工作年限") # ge=0 表示必须大于等于0
    skills: List[str] = Field(default_factory=list, description="技能列表")
    is_qualified: bool = Field(default=False)

    # 自定义校验逻辑：如果工作年限 > 3，自动标记为合格
    @field_validator('is_qualified')
    @classmethod
    def auto_check_qualification(cls, v, info):
        # 注意：在 Pydantic v2 中通过 info.data 获取已验证的字段
        return v

# 模拟 AI 吐出的“脏数据”
raw_ai_data = {
    "name": "张三",
    "years_of_exp": "5",  # 这里的 5 是字符串，Pydantic 会自动尝试转成 int
    "skills": ["Python", "LangChain"]
}

try:
    resume = ResumeStandard(**raw_ai_data)
    print(f"✅ 验证通过！姓名：{resume.name}, 经验：{resume.years_of_exp}年")
except Exception as e:
    print(f"❌ 数据格式错误：{e}")