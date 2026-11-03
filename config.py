# config.py
import os

# ↓↓↓ DeepSeek 配置 ↓↓↓
# base_url 必须指向 DeepSeek 的 OpenAI 兼容端点
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com")
# 模型名：deepseek-v4-flash（通用/便宜）或 deepseek-v4-pro（推理强）
# 注意：deepseek-chat / deepseek-reasoner 已于 2026-07-24 退役，用它们会直接报错
MODEL = os.getenv("OPENAI_MODEL", "deepseek-v4-flash")
# 安全提示：密钥只从环境变量读取，不要写死在本文件里（本文件会提交到 git）。
#   Windows(PowerShell):  $env:OPENAI_API_KEY = '你的key'
#   Linux/macOS:          export OPENAI_API_KEY='你的key'
API_KEY = os.getenv("OPENAI_API_KEY", "")

if not API_KEY:
    raise RuntimeError(
        "未设置 API Key。请设置环境变量 OPENAI_API_KEY，或在 config.py 中写死 API_KEY。"
    )

INPUT_DOCX = "input/信息中心管理制度.docx"
OUTPUT_JSON = "output/信息中心管理制度.json"
OUTPUT_XLSX = "output/信息中心管理制度.xlsx"
MAX_RETRY = 1