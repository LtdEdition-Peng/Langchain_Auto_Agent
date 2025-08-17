# memory.py
"""
记忆模块初始化
"""
from langchain.memory import ConversationBufferMemory

MEMORY = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)
