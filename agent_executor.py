# agent_executor.py
"""
自定义 AgentExecutor 类
"""
from langchain.agents import AgentExecutor
from langchain.schema import AgentAction

class CustomAgentExecutor(AgentExecutor):
    def _handle_parsing_error(self, error_message: str) -> str:
        print(f"🚨 解析错误: {error_message}")
        return f"""
🔥 JSON格式错误提醒：

你的输出格式不正确！请严格使用JSON格式：

📋 使用工具格式：
{{
    "thought": "我需要思考的内容...",
    "action": "Calculator",
    "action_input": "2+3*4"
}}

📋 最终答案格式：
{{
    "thought": "我已经获得了足够的信息...",
    "final_answer": "基于以上信息，答案是..."
}}

⚠️ 重要提醒：
1. 必须包含 "thought" 字段
2. 使用工具时需要 "action" 和 "action_input"
3. 给出最终答案时使用 "final_answer"
4. 严格遵循JSON语法，注意引号和逗号

错误详情: {error_message}

请重新按JSON格式输出。
"""
    def _handle_tool_error(self, error: Exception, action: AgentAction) -> str:
        print(f"🚨 工具执行错误: {action.tool} - {error}")
        if action.tool == "Calculator":
            return f"""
⚠️ 计算器工具执行失败！

错误: {error}
工具: {action.tool}
输入: {action.tool_input}

💡 建议：
1. 检查数学表达式语法是否正确
2. 确保只包含基本数学运算符 (+, -, *, /, (), 数字)
3. 避免使用复杂函数或变量

请重新尝试或使用其他方法。
"""
        elif action.tool == "Search":
            return f"""
⚠️ 搜索工具执行失败！

错误: {error}
工具: {action.tool}
输入: {action.tool_input}

💡 建议：
1. 简化搜索关键词
2. 检查网络连接
3. 尝试使用不同的搜索词

请重新尝试或换个方式描述问题。
"""
        else:
            return f"""
⚠️ 工具 '{action.tool}' 执行失败！

错误: {error}
输入: {action.tool_input}

请检查工具名称和输入参数是否正确，或尝试其他方法。
"""
    def _call(self, inputs, run_manager=None):
        try:
            return super()._call(inputs, run_manager)
        except Exception as e:
            print(f"🚨 Agent 执行过程中发生错误: {e}")
            raise
    def _should_continue(self, iterations: int, time_elapsed: float) -> bool:
        if iterations > self.max_iterations:
            print(f"⚠️  达到最大迭代次数: {iterations}")
            return False
        if self.max_execution_time and time_elapsed > self.max_execution_time:
            print(f"⚠️  达到最大执行时间: {time_elapsed:.1f}s")
            return False
        return True
