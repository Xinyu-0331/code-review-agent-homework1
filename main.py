from dotenv import load_dotenv
import os
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import SystemMessage
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# 导入自定义工具
from read_code_tool import tools

# ==========1.加载环境变量==========
load_dotenv()
api_key = os.getenv("DASHSCOPE_API_KEY")

if not api_key:
    raise ValueError("没有读取到DASHSCOPE_API_KEY，请检查.env文件配置！")

# ==========2.初始化大模型LLM==========
llm = ChatTongyi(
    dashscope_api_key=api_key,
    model="qwen-turbo"
)

# ==========3.系统提示词Prompt设计，定义Agent角色==========
system_prompt = """
你是专业的代码审查Agent，你的工作是对Python代码进行代码审查。
任务：对代码做审查，找出潜在Bug、安全问题、代码坏味道，给出修改建议。
你拥有工具 read_local_code_file，可以读取本地代码文件。
当用户提供文件路径，你优先调用工具读取文件，拿到代码内容再分析；
如果用户直接粘贴代码文本，直接做审查，不用调用工具。

输出结果严格按照下面格式输出：
【潜在Bug】
列出代码中会引发崩溃、异常的风险点

【代码质量问题】
可读性、命名、注释、代码规范方面问题

【改进建议】
逐条说明如何修改，附上修复后的完整示例代码
"""

# ==========4.组装Agent Prompt模板==========
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# ==========5.创建Agent与执行器==========
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# ==========6.对话记忆==========
memory_store = {}

def get_session_history(session_id: str):
    if session_id not in memory_store:
        memory_store[session_id] = ChatMessageHistory()
    return memory_store[session_id]

agent_with_history = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)

# ==========7.命令行交互入口==========
def cli_run():
    print("=" * 40)
    print("Homework 1 代码审查Agent")
    print("=" * 40)
    print("使用方法：")
    print("1. 输入文件路径，例如：请审查 ./demo_code.py")
    print("2. 直接粘贴代码文本，让Agent审查")
    print("3. 输入 exit 退出程序\n")

    session_id = "session_01"
    while True:
        user_input = input("请输入你的请求：")
        user_input = user_input.strip()
        if user_input.lower() == "exit":
            print("程序结束。")
            break
        try:
            result = agent_with_history.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": session_id}}
            )
            print("\n----------审查结果----------")
            print(result["output"])
            print("-"*50 + "\n")
        except Exception as err:
            print(f"\n程序异常：{err}\n")


if __name__ == "__main__":
    cli_run()
