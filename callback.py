# callback.py
"""
自定义回调处理器
"""
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentAction, AgentFinish

class CustomCallbackHandler(BaseCallbackHandler):
    def on_agent_action(self, action: AgentAction, **kwargs) -> None:
        print(f"🔧 准备使用工具: {action.tool}")
        print(f"📝 工具输入: {action.tool_input}")
    def on_agent_finish(self, finish: AgentFinish, **kwargs) -> None:
        print(f"✅ Agent 完成任务")
    def on_tool_start(self, serialized: dict, input_str: str, **kwargs) -> None:
        tool_name = serialized.get('name', '未知工具')
        print(f"⚙️  {tool_name} 开始执行...")
    def on_tool_end(self, output: str, **kwargs) -> None:
        print(f"📤 工具输出: {output}")
    def on_tool_error(self, error: Exception, **kwargs) -> None:
        print(f"❌ 工具执行错误: {error}")
