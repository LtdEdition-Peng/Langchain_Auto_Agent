from langchain_community.llms import Tongyi
# 初始化阿里百炼LLM
llm = Tongyi(
    model_name="qwen-turbo-2025-07-15",  
    top_p=0.8,
    streaming=False,
    api_key="your-api-key"  # 替换为你的API密钥
)

# ===================== 其他主流 LLM API 接口示例 =====================

# 1. DeepSeek（ds）API 示例
# 依赖：pip install langchain-community
# from langchain_community.llms import DeepSeek
# llm = DeepSeek(
#     model_name="deepseek-chat",
#     api_key="your-deepseek-api-key",
#     temperature=0.7,
#     streaming=False
# )

# 2. OpenAI API 示例
# 依赖：pip install langchain-openai
# from langchain_openai import ChatOpenAI
# llm = ChatOpenAI(
#     model="gpt-3.5-turbo",
#     api_key="your-openai-api-key",
#     temperature=0.7,
#     streaming=False
# )

# 3. Google Gemini API 示例
# 依赖：pip install langchain-google-genai
# from langchain_google_genai import ChatGoogleGenerativeAI
# llm = ChatGoogleGenerativeAI(
#     model="gemini-pro",
#     google_api_key="your-google-api-key",
#     temperature=0.7,
#     streaming=False
# )

# 你可以根据需要取消注释并填写自己的 key，即可切换不同大模型。