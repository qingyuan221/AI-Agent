from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ----------------------
# 1. 初始化大模型
# ----------------------
llm = ChatOpenAI(
    api_key="1bf7ef3239fc4649825b4673e5731211.zamL3TFjqwMb2Tfy",
    base_url="https://open.bigmodel.cn/api/paas/v4",
    model="glm-3-turbo"
)

# ----------------------
# 2. 自定义工具（新版装饰器 @tool）
# ----------------------
@tool
def calculator(expr: str) -> str:
    """
    用于数学表达式计算，支持加减乘除、括号
    输入示例：1+2*(3+4)
    """
    try:
       result = str(eval(expr))
       return f"计算结果：{result}"
    except Exception as e:
        return f"计算出错：{str(e)}"

@tool
def explain_word(word: str) -> str:
    """
    用于解释专业名词、AI相关术语
    输入：需要解释的单词或术语，例如：RAG、AI智能体
    """
    explain_dict = {
        "RAG": "检索增强生成，把私有文档导入知识库，让大模型基于文档回答，减少幻觉。",
        "AI智能体": "具备思考、规划、调用工具、拥有记忆，能自主完成复杂任务的AI。",
        "LCEL": "LangChain最新表达式语法，用|管道拼接组件，替代老旧废弃chain写法。"
    }
    return explain_dict.get(word, f"暂无{word}的释义，请换其他术语查询。")

# 把工具放进列表
tools = [calculator, explain_word]

# ----------------------
# 3. 搭建带工具调用能力的智能体
# ----------------------
prompt = ChatPromptTemplate.from_template("""
你是一个可以调用工具的AI智能体。
如果用户问题需要计算，调用calculator工具；
如果是专业名词解释，调用explain_word工具；
其他问题直接自行回答。

用户问题：{question}
""")

# LCEL 链式
agent_chain = prompt | llm | StrOutputParser()

# ----------------------
# 4. 测试
# ----------------------
if __name__ == "__main__":
    print("=== 智能体已启动 ===")

    # 测试1：计算
    q1 = "计算 15*8+22"
    print("用户：", q1)
    print("智能体：", calculator.invoke("15*8+22"))
    print("-" * 40)

    # 测试2：名词解释
    q2 = "解释一下RAG"
    print("用户：", q2)
    print("智能体：", explain_word.invoke("RAG"))