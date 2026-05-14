from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
#初始化大模型
llm = ChatOpenAI(
    api_key="",
    base_url="https://open.bigmodel.cn/api/paas/v4/",
    model="glm-3-turbo"
)
#1.定义提示词模板，用变量名占位
template = """你是专业的{job},用通俗易懂的语言讲解{topic}，控制在三句话以内"""

#2.创建模板对象
prompt = PromptTemplate(
    input_variables=["job","topic"],
    template=template
)
#3.传入实际变量，拼接完成完整的prompt
fill_prompt = prompt.format(job="AI智能体讲师", topic="RAG是什么")
#4.调用大模型
res=llm.invoke(fill_prompt)
print(res.content)