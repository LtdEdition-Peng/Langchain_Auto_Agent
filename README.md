[English Document](./README_en.md)


# LangChain Agent 项目说明文档

这是一个基于 LangChain 框架的智能对话代理项目，使用阿里百炼平台的通义千问模型，具有工具调用能力和对话记忆功能

## 如不想使用任何框架纯python实现

- [LtdEdition-Peng/LLM_Auto_Agent (GitHub)](https://github.com/LtdEdition-Peng/LLM_Auto_Agent)
## 环境与配置需求

- **Python 版本**：建议 Python 3.9 及以上
- **推荐环境**：建议使用 conda 虚拟环境（非必须，但agent工具中py代码依赖connda环境,可自行修改）
- **依赖安装**：
  ```bash
  pip install langchain langchain-community
  ```
- **API Key 配置**：
  - 阿里百炼/通义千问：在 `setmodel.py` 填写 `api_key`
  - [百炼api申请（页面左下角）](https://bailian.console.aliyun.com/?tab=model#/model-market)
  - OpenAI/DeepSeek/Gemini：参考 `setmodel.py` 示例填写
- **网络要求**：需要能访问对应 LLM 服务的公网网络

---



## 📁 项目结构

```
Langchain_agent/
├── main.py              # 🎯 主入口文件
├── setmodel.py          # 🤖 LLM模型配置
├── config.py            # ⚙️ 全局配置参数
├── tools.py             # 🔧 工具函数定义
├── prompts.py           # 💭 提示词模板
├── output_parser.py     # 📝 输出解析器
├── callback.py          # 📞 回调处理器
├── agent_executor.py    # 🚀 自定义Agent执行器
├── memory.py            # 🧠 记忆模块（已废弃）
└── README.md            # 📖 本文档
```

## 📋 文件详细说明

### 🎯 main.py - 主入口文件
**功能**: 程序的主要入口，负责用户交互和主循环
**主要内容**:
- 导入所有必要的模块和配置
- 初始化 Agent、记忆、解析器等组件
- 实现用户交互循环
- 处理用户输入（问题、退出、清除记忆等命令）
- 显示执行结果和中间步骤

**使用方式**:
```bash
python main.py
```

### 🤖 setmodel.py - LLM模型配置
**功能**: 配置和初始化大语言模型，默认使用的阿里百炼api

**主要内容**:
- 导入阿里百炼通义千问模型
- 设置模型参数（model_name、top_p、streaming等）
- 配置 API 密钥
- 导出 `llm` 对象供其他模块使用

**配置示例**:
```python
llm = Tongyi(
    model_name="qwen-turbo-2025-07-15",
    top_p=0.8,
    streaming=False,
    api_key="your-api-key-here"
# [English Version (README_en.md)](./README_en.md)
)
```

### ⚙️ config.py - 全局配置参数
**功能**: 集中管理所有配置参数
**主要配置项**:
- `AGENT_CONFIG`: Agent执行器配置
  - `max_iterations`: 最大迭代次数
  - `max_execution_time`: 最大执行时间
  - `handle_parsing_errors`: 解析错误处理
  - `return_intermediate_steps`: 返回中间步骤
- `MEMORY_CONFIG`: 记忆模块配置
  - `memory_key`: 记忆键名
  - `return_messages`: 返回消息格式
  - `output_key`: 输出键（避免警告）
- `SHOW_INTERMEDIATE_STEPS`: 是否显示中间执行步骤

### 🔧 tools.py - 工具函数定义
**功能**: 定义Agent可以调用的工具函数
**当前工具**:
- `@tool calculator`: 数学表达式计算器
  - 支持基本四则运算
  - 包含安全检查，防止恶意代码执行
  - 错误处理（除零、语法错误等）


**工具注册**: 使用 LangChain 的 `@tool` 装饰器自动注册
**导出**: `TOOLS` 列表供 Agent 使用

### 💭 prompts.py - 提示词模板
**功能**: 定义Agent的行为提示词
**主要内容**:
- JSON格式的严格输出要求
- 工具使用指导
- 思考过程要求
- 示例格式展示

**提示词特点**:
- 要求严格的JSON格式输出
- 包含 `thought`（思考过程）字段
- 支持工具调用和最终答案两种模式
- 包含对话历史和工具信息占位符

### 📝 output_parser.py - 输出解析器
**功能**: 解析LLM的JSON格式输出
**主要功能**:
- JSON格式验证和解析
- `AgentAction` 和 `AgentFinish` 对象构建
- 备选格式解析（兼容性）
- 详细的错误提示和处理

**解析逻辑**:
1. 优先解析JSON格式
2. 验证必需字段（`thought`）
3. 根据内容返回 Action 或 Finish
4. 失败时尝试传统格式解析

### 📞 callback.py - 回调处理器
**功能**: 监控Agent执行过程
**回调事件**:
- `on_agent_action`: Agent准备使用工具时
- `on_agent_finish`: Agent完成任务时
- `on_tool_start`: 工具开始执行时
- `on_tool_end`: 工具执行完成时
- `on_tool_error`: 工具执行出错时

### 🚀 agent_executor.py - 自定义Agent执行器
**功能**: 扩展LangChain的AgentExecutor，添加自定义错误处理
**主要特性**:
- 自定义解析错误处理
- 针对不同工具的错误处理策略
- 全局异常捕获
- 执行条件控制（迭代次数、时间限制）

**错误处理**:
- JSON解析错误：提供格式指导
- 工具执行错误：根据工具类型给出具体建议
- 全局异常：统一捕获和日志记录

### 🧠 memory.py - 记忆模块（已废弃）
**状态**: 已废弃，记忆功能现在直接在 `main.py` 中使用 LangChain 内置的 `ConversationBufferMemory`

## 🚀 快速开始

1. **安装依赖**:
```bash
pip install langchain langchain-community
```

2. **配置模型**:
编辑 `setmodel.py`，填入你的阿里百炼 API 密钥

3. **运行程序**:
```bash
python main.py
```

4. **交互命令**:
- 输入问题进行对话
- 输入 `quit`、`exit` 或 `退出` 来结束程序
- 输入 `clear`、`清除` 或 `清除记忆` 来清空对话历史

## ⚙️ 配置说明

### 显示控制
在 `config.py` 中修改 `SHOW_INTERMEDIATE_STEPS` 来控制是否显示中间执行步骤：
```python
SHOW_INTERMEDIATE_STEPS = True   # 显示中间步骤
SHOW_INTERMEDIATE_STEPS = False  # 不显示中间步骤
```

### Agent参数调整
在 `config.py` 的 `AGENT_CONFIG` 中调整：
- `max_iterations`: 最大思考轮数
- `max_execution_time`: 最大执行时间限制
- `verbose`: 是否显示详细执行信息

## 🔧 扩展开发

### 添加新工具
1. 在 `tools.py` 中添加新函数
2. 使用 `@tool` 装饰器注册
3. 函数会自动加入 `TOOLS` 列表

```python
@tool
def new_tool(input_text: str) -> str:
    """新工具的描述"""
    # 工具逻辑
    return "工具执行结果"
```

### 修改提示词
编辑 `prompts.py` 中的 `TEMPLATE` 变量来调整Agent行为

### 自定义错误处理
在 `agent_executor.py` 中的 `_handle_tool_error` 方法添加新的工具错误处理逻辑

## 📝 注意事项

- 确保 API 密钥正确配置
- 工具函数需要包含完整的 docstring（用作工具描述）
- JSON格式输出要求严格，LLM需要严格按照模板格式响应
- 记忆功能会保存完整对话历史，长时间对话可能影响性能

## 🔍 故障排除

### 常见问题
1. **导入错误**: 确保所有文件在同一目录下
2. **API密钥错误**: 检查 `setmodel.py` 中的密钥配置
3. **JSON解析失败**: LLM输出格式不符合要求，检查提示词设置
4. **工具执行失败**: 查看具体错误信息，可能是输入参数问题

### 调试技巧
- 设置 `SHOW_INTERMEDIATE_STEPS = True` 查看执行过程
- 在 `AGENT_CONFIG` 中设置 `verbose = True` 获取详细日志
- 查看终端输出的错误提示信息

