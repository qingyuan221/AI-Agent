from langchain_core.prompts import PromptTemplate,FewShotPromptTemplate
from langchain_community.llms.tongyi import Tongyi

example_template = PromptTemplate.from_template("单词:{word},反义词:{antonym}")


example_date = [
    {"word":"大","antonym":"小"},
    {"word":"上","antonym":"下"}
]




few_shot_prompt_template = FewShotPromptTemplate(
    example_prompt = example_template,    #示例提示词
    examples = example_date,           #示例数据
    prefix = "我给你几个案例，告诉我输入单词的反义词",            #示例之前的提示词
    suffix = "基于前面的案例，告诉我{input_word}的反义词",            #示例之后的提示词
    input_variables = ['input_word'],   #声明变量名

)

example_text = few_shot_prompt_template.invoke(input={"input_word":"左" }).to_string()
#print(example_text)

model = Tongyi(
    model ="qwen-max",
    api_key="sk-9d8f8cb564b74b8b946a3549021a8a65",
)
res = model.invoke(input=example_text)
print(res)