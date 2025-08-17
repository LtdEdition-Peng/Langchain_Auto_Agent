# output_parser.py
"""
自定义输出解析器
"""
from langchain.agents.agent import AgentOutputParser
from langchain.schema import AgentAction, AgentFinish, OutputParserException
import re

class CustomOutputParser(AgentOutputParser):
    def parse(self, text: str):
        import json
        try:
            json_match = re.search(r'(\{[^}]*?(?:\{[^}]*\}[^}]*)*\})', text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                data = json.loads(json_str)
                if "thought" not in data:
                    raise OutputParserException("JSON中必须包含'thought'字段")
                if "action" in data and "action_input" in data and "final_answer" not in data:
                    log_message = f"Thought: {data['thought']}\nAction: {data['action']}\nAction Input: {data['action_input']}"
                    output = AgentAction(
                        tool=data["action"],
                        tool_input=data["action_input"],
                        log=log_message
                    )
                    return output
                elif "final_answer" in data:
                    return AgentFinish(
                        return_values={"output": data["final_answer"]},
                        log=f"Thought: {data['thought']}\nFinal Answer: {data['final_answer']}"
                    )
                else:
                    raise OutputParserException(
                        f"JSON格式不完整！必须包含以下组合之一：\n"
                        f"1. 'action' + 'action_input'（使用工具）\n"
                        f"2. 'final_answer'（最终答案）\n\n"
                        f"你的输出: {data}"
                    )
            else:
                return self._parse_fallback_format(text)
        except json.JSONDecodeError as e:
            try:
                return self._parse_fallback_format(text)
            except:
                raise OutputParserException(
                    f"❌ JSON解析失败！请使用正确的JSON格式：\n\n"
                    f"使用工具格式：\n"
                    f'{"thought": "我需要...", "action": "工具名", "action_input": "参数"}'
                    f"\n\n最终答案格式：\n"
                    f'{"thought": "我已经...", "final_answer": "答案内容"}'
                    f"\n\nJSON错误: {e}\n你的输出: {text}"
                )
    def _parse_fallback_format(self, text: str):
        action_match = re.search(r"Action:\s*(.+?)\nAction Input:\s*(.+?)(?=\n|$)", text, re.DOTALL)
        if action_match:
            action = action_match.group(1).strip()
            action_input = action_match.group(2).strip()
            return AgentAction(tool=action, tool_input=action_input, log=text)
        final_match = re.search(r"Final Answer:\s*(.+)", text, re.DOTALL)
        if final_match:
            return AgentFinish(
                return_values={"output": final_match.group(1).strip()},
                log=text
            )
        raise OutputParserException(
            f"❌ 无法解析输出格式！请使用JSON格式：\n\n"
            f"使用工具：\n"
            f'{"thought": "思考内容", "action": "工具名", "action_input": "参数"}'
            f"\n\n最终答案：\n"
            f'{"thought": "思考内容", "final_answer": "答案"}'
            f"\n\n你的输出: {text}"
        )
