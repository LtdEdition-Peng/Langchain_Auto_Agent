# config.py
"""
全局配置参数
"""

# Agent 配置
AGENT_CONFIG = {
    "max_iterations": 10,                    # 最大迭代次数
    "max_execution_time": 120,              # 最大执行时间（秒）
    "early_stopping_method": "force",       # 早停方法: "force" 或 "generate"
    "handle_parsing_errors": True,          # 启用解析错误处理
    "return_intermediate_steps": True,      # 返回中间步骤
    "verbose": False,                       # 显示详细信息
    "tags": ["custom-agent", "demo"],       # 标签
    "metadata": {"version": "1.0", "type": "demo"}  # 元数据
}

# 记忆配置
MEMORY_CONFIG = {
    "memory_key": "chat_history",
    "return_messages": True,
    "output_key": "output"  # 明确指定使用哪个输出键保存到记忆
}


# 显示配置
SHOW_INTERMEDIATE_STEPS = False  # 是否显示中间步骤
