from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate
from langchain_core.prompts import ChatPromptTemplate

template = PromptTemplate.from_template("我的邻居是{name},他的爱好是{hobby}")


res1 = template.format(name = "杨明",hobby = "钓鱼")
print(res1,type(res1))

res2 = template.invoke({"name":"杨明","hobby":"钓鱼"})
print(res2,type(res2))