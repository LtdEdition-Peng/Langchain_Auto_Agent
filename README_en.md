
[中文文档 (README.md)](./README.md)



# LangChain Agent Project Documentation



This is an intelligent conversational agent project based on the LangChain framework, using Alibaba Bailian (Tongyi Qianwen) LLM, with tool-calling and conversation memory capabilities.

## If you want a pure Python agent without any framework

- [LtdEdition-Peng/LLM_Auto_Agent (GitHub)](https://github.com/LtdEdition-Peng/LLM_Auto_Agent)

## 📁 Project Structure

```
Langchain_agent/
├── main.py              # 🎯 Main entry point
├── setmodel.py          # 🤖 LLM model configuration
├── config.py            # ⚙️ Global configuration
├── tools.py             # 🔧 Tool function definitions
├── prompts.py           # 💭 Prompt templates
├── output_parser.py     # 📝 Output parser
├── callback.py          # 📞 Callback handler
├── agent_executor.py    # 🚀 Custom AgentExecutor
├── memory.py            # 🧠 Memory module (deprecated)
└── README.md            # 📖 This documentation
```



## Environment & Configuration Requirements

- **Python Version**: Python 3.9 or above recommended
- **Recommended Environment**: Use a conda virtual environment (not strictly required, but some agent tool code assumes conda, you can modify as needed)
- **Dependency Installation**:
  ```bash
  pip install langchain langchain-community
  ```
- **API Key Configuration**:
  - Alibaba Bailian/Tongyi Qianwen: Fill `api_key` in `setmodel.py`
  - [Bailian API application (bottom left of page)](https://bailian.console.aliyun.com/?tab=model#/model-market)
  - OpenAI/DeepSeek/Gemini: See `setmodel.py` for examples
- **Network**: Requires public network access to the LLM service

---

# Pure Python LLM Agent Recommendation

If you want a fully hand-written, framework-free LLM Agent, see:

- [LtdEdition-Peng/LLM_Auto_Agent (GitHub)](https://github.com/LtdEdition-Peng/LLM_Auto_Agent)

**Features:**
- All core logic in pure Python, no AI framework dependencies
- Great for learning LLM reasoning, toolchains, and agent mechanisms
- Minimal code, easy for secondary development and teaching

**Use Cases:**
- Developers who want to deeply understand LLM Agent principles
- Projects needing full control and no black-box dependencies
- Customizing reasoning chains, tool calls, etc.

---

## 📋 File Descriptions

### 🎯 main.py - Main Entry
**Function**: Main program entry, user interaction loop
**Key Points**:
- Imports all necessary modules and configs
- Initializes agent, memory, parser, etc.
- Implements user interaction loop
- Handles user input (questions, exit, clear memory)
- Displays results and intermediate steps

**Usage**:
```bash
python main.py
```

### 🤖 setmodel.py - LLM Model Config
**Function**: Configure and initialize LLM (default: Alibaba Qwen)
**Key Points**:
- Import Alibaba Qwen model
- Set model parameters (model_name, top_p, streaming, etc.)
- Configure API key
- Export `llm` object for other modules

**Example**:
```python
llm = Tongyi(
    model_name="qwen-turbo-2025-07-15",
    top_p=0.8,
    streaming=False,
    api_key="your-api-key-here"
)
```

### ⚙️ config.py - Global Config
**Function**: Centralized config management
**Key Items**:
- `AGENT_CONFIG`: AgentExecutor config
  - `max_iterations`: Max iterations
  - `max_execution_time`: Max execution time
  - `handle_parsing_errors`: Parsing error handling
  - `return_intermediate_steps`: Return intermediate steps
- `MEMORY_CONFIG`: Memory config
  - `memory_key`: Memory key
  - `return_messages`: Return message format
  - `output_key`: Output key (avoid warnings)
- `SHOW_INTERMEDIATE_STEPS`: Show intermediate steps

### 🔧 tools.py - Tool Functions
**Function**: Define agent-callable tools
**Current Tools**:
- `@tool calculator`: Math expression calculator
  - Supports basic arithmetic
  - Security checks to prevent code injection
  - Error handling (zero division, syntax, etc.)
- `@tool search_tool`: Simulated search tool
  - Simulates web search
  - Random failure for error handling tests

**Tool Registration**: Uses LangChain `@tool` decorator
**Export**: `TOOLS` list for agent use

### 💭 prompts.py - Prompt Templates
**Function**: Define agent prompt templates
**Key Points**:
- Strict JSON output requirements
- Tool usage guidance
- Thought process requirements
- Example formats

**Prompt Features**:
- Strict JSON output
- Must include `thought` field
- Supports tool use and final answer
- Includes chat history and tool info placeholders

### 📝 output_parser.py - Output Parser
**Function**: Parse LLM JSON output
**Key Points**:
- JSON validation and parsing
- Build `AgentAction` and `AgentFinish`
- Fallback format parsing (compatibility)
- Detailed error messages

**Parsing Logic**:
1. Try JSON first
2. Validate required fields (`thought`)
3. Return Action or Finish
4. Fallback to legacy format if needed

### 📞 callback.py - Callback Handler
**Function**: Monitor agent execution
**Events**:
- `on_agent_action`: Before tool use
- `on_agent_finish`: On finish
- `on_tool_start`: Tool starts
- `on_tool_end`: Tool ends
- `on_tool_error`: Tool error

### 🚀 agent_executor.py - Custom AgentExecutor
**Function**: Extend LangChain AgentExecutor with custom error handling
**Key Features**:
- Custom parsing error handling
- Tool-specific error strategies
- Global exception catch
- Execution control (iterations, time)

**Error Handling**:
- JSON parsing: format guidance
- Tool errors: tool-specific advice
- Global: unified catch/log

### 🧠 memory.py - Memory Module (Deprecated)
**Status**: Deprecated, now use LangChain's built-in `ConversationBufferMemory` in `main.py`

## 🚀 Quick Start

1. **Install dependencies**:
```bash
pip install langchain langchain-community
```

2. **Configure model**:
Edit `setmodel.py` and fill in your API key

3. **Run the program**:
```bash
python main.py
```

4. **Commands**:
- Enter questions to chat
- Enter `quit`, `exit`, or `退出` to exit
- Enter `clear`, `清除`, or `清除记忆` to clear memory

## ⚙️ Config Guide

### Display Control
Edit `SHOW_INTERMEDIATE_STEPS` in `config.py`:
```python
SHOW_INTERMEDIATE_STEPS = True   # Show intermediate steps
SHOW_INTERMEDIATE_STEPS = False  # Hide intermediate steps
```

### Agent Parameters
Edit `AGENT_CONFIG` in `config.py`:
- `max_iterations`: Max reasoning rounds
- `max_execution_time`: Max execution time
- `verbose`: Show detailed logs

## 🔧 Extending

### Add New Tool
1. Add a function in `tools.py`
2. Decorate with `@tool`
3. It will be auto-added to `TOOLS`

```python
@tool
def new_tool(input_text: str) -> str:
    """Description of the new tool"""
    # Tool logic
    return "Tool result"
```

### Modify Prompts
Edit `TEMPLATE` in `prompts.py` to change agent behavior

### Custom Error Handling
Add new logic in `_handle_tool_error` in `agent_executor.py`

## 📝 Notes

- Ensure API keys are set correctly
- Tool functions need full docstrings (for descriptions)
- LLM must output strict JSON as per template
- Memory saves full chat history; long sessions may affect performance

## 🔍 Troubleshooting

### Common Issues
1. **Import errors**: Ensure all files are in the same directory
2. **API key errors**: Check `setmodel.py` config
3. **JSON parsing errors**: LLM output format issue, check prompt
4. **Tool errors**: See error message, may be input problem

### Debug Tips
- Set `SHOW_INTERMEDIATE_STEPS = True` to see process
- Set `verbose = True` in `AGENT_CONFIG` for detailed logs
- Check terminal error messages
