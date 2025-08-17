import sys
import os

# 添加项目根目录到 sys.path（为了导入 setmodel）
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from langchain.memory import ConversationBufferMemory
from langchain.agents import create_react_agent

from tools import TOOLS
from prompts import PROMPT
from config import AGENT_CONFIG, MEMORY_CONFIG, SHOW_INTERMEDIATE_STEPS
from setmodel import llm
from output_parser import CustomOutputParser
from callback import CustomCallbackHandler
from agent_executor import CustomAgentExecutor


def main():
    print("=== LangChain Agent 基础版本（使用阿里百炼平台）===")

    # 创建记忆实例
    memory = ConversationBufferMemory(**MEMORY_CONFIG)
    
    # 创建自定义解析器实例
    custom_parser = CustomOutputParser()
    # 创建回调处理器
    callback_handler = CustomCallbackHandler()
    # 创建 ReAct Agent（使用自定义解析器）
    agent = create_react_agent(llm, TOOLS, PROMPT, output_parser=custom_parser)
    # 创建完全自定义的 AgentExecutor
    agent_executor = CustomAgentExecutor(
        agent=agent,
        tools=TOOLS,
        memory=memory,
        **AGENT_CONFIG
    )

    while True:
        user_input = input("\Question: ").strip()
        if user_input.lower() in ['quit', 'exit', '退出']:
            print("再见!")
            break
        if user_input.lower() in ['clear', '清除', '清除记忆']:
            memory.clear()
            print("✅ 记忆已清除")
            continue
        if not user_input:
            continue
        try:
            result = agent_executor.invoke({"input": user_input})
            if SHOW_INTERMEDIATE_STEPS and "intermediate_steps" in result and result["intermediate_steps"]:
                print("\n中间步骤:")
                for i, (action, observation) in enumerate(result["intermediate_steps"], 1):
                    print(f"步骤 {i}:")
                    print(f"  动作: {action.tool}")
                    print(f"  输入: {action.tool_input}")
                    print(f"  输出: {observation}")
                print(f"\n🧠 记忆状态: 已记录 {len(memory.chat_memory.messages)} 条消息")
            print("Answerr:", result["output"])  
        except Exception as e:
            print(f"执行错误: {e}")

if __name__ == "__main__":
    main()
