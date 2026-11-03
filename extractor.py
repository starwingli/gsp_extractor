# extractor.py
import json
from openai import OpenAI
from jsonschema import validate

from config import API_KEY, BASE_URL, MODEL, MAX_RETRY
from schema import TOOLS, PARAMETERS_SCHEMA

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

SYSTEM_PROMPT = (
    "你是信息中心制度结构化助手。请从用户提供的文本中提取制度要素，"
    "调用 save_it_management_system 函数。不要输出任何自由文本。"
)

def extract_system(doc_text: str, max_retry: int = MAX_RETRY) -> dict:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "制度原文：\n" + doc_text},
    ]

    for attempt in range(max_retry + 1):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice={"type": "function", "function": {"name": "save_it_management_system"}},
            # DeepSeek V4 默认开启 thinking 模式，该模式不支持强制 tool_choice，
            # 必须显式关闭，否则报 400: Thinking mode does not support this tool_choice
            extra_body={"thinking": {"type": "disabled"}},
        )

        msg = response.choices[0].message
        if not msg.tool_calls:
            if attempt == max_retry:
                raise RuntimeError("模型未返回 tool_calls")
            messages.append({"role": "user", "content": "请务必调用 save_it_management_system 函数。"})
            continue

        tool_call = msg.tool_calls[0]
        raw_args = tool_call.function.arguments

        try:
            data = json.loads(raw_args)
            validate(instance=data, schema=PARAMETERS_SCHEMA)
            return data
        except Exception as e:
            if attempt == max_retry:
                raise RuntimeError(f"抽取失败且重试耗尽：{e}")
            messages.append(msg)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": f"校验失败：{e}。请修正后重新调用。",
            })

    raise RuntimeError("不可达")