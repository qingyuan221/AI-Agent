from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
#1. 初始化模型
llm = ChatOpenAI(
    api_key="",
    base_url="https://open.bigmodel.cn/api/paas/v4",
    model="glm-3-turbo"
)
#2.定义提示词模板
template = """
你是资深技术讲师，请用大白话讲解{subject}，控制在三句话以内
"""
prompt = PromptTemplate(
    input_variables=["subject"],
    template=template
)
# 3. 构建链式：模板 → 模型 → 解析输出
chain = prompt | llm | StrOutputParser()
# 4. 直接传参数调用链
result = chain.invoke({"subject":"多轮对话的实现原理"})
print(result)