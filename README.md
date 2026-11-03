# gsp_extractor

从 Word 制度文档中抽取结构化要素，并导出为 JSON / Excel。

输入一份「信息中心管理制度」类 `.docx`，程序会按「一、二、三……」切分成多段子制度，
再调用大模型（DeepSeek，OpenAI 兼容接口）逐段抽取制度要素，最后输出结构化 JSON 和便于
筛选的 Excel 明细表。

## 处理流程

```
input/*.docx
   │  splitter.read_docx          读取段落文本
   │  splitter.split_by_sections  按「一、二、三…」切分，跳过目录
   ▼
extractor.extract_system          逐段调用模型 + JSON Schema 校验 + 失败重试
   │  （强制 tool_calls，关闭 thinking 模式）
   ▼
pipeline.business_check           业务规则校验（制度名称 / 具体要求非空）
   ▼
output/*.json                     原始结构化记录
output/*.xlsx                     Excel 明细（每个要求条款一行）
```

## 目录结构

| 文件 | 作用 |
| --- | --- |
| `config.py` | 模型、接口地址、输入输出路径等配置（密钥从环境变量读取） |
| `schema.py` | 函数调用（tools）定义与参数的 JSON Schema |
| `splitter.py` | 读取 docx、按章节切分正文 |
| `extractor.py` | 调用模型抽取单个子制度，带 Schema 校验与重试 |
| `excel_writer.py` | 把抽取结果写成带样式、冻结表头的 Excel |
| `pipeline.py` | 串起整个流程的入口 |

## 环境准备

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

## 配置密钥

密钥不会写进仓库，请用环境变量注入：

```powershell
# Windows PowerShell
$env:OPENAI_API_KEY = "sk-..."
```

```bash
# Linux / macOS
export OPENAI_API_KEY='sk-...'
```

可选变量：`OPENAI_BASE_URL`（默认 `https://api.deepseek.com`）、`OPENAI_MODEL`（默认 `deepseek-v4-flash`）。
也可以复制 `.env.example` 为 `.env` 自行管理（`.env` 已被忽略）。

## 运行

```bash
python pipeline.py
```

输出文件路径由 `config.py` 中的 `INPUT_DOCX` / `OUTPUT_JSON` / `OUTPUT_XLSX` 指定。

## Excel 输出说明

每个「要求条款」占一行，制度级字段（名称、起草/执行/监督部门、目的、适用范围、流程示意）
在每一行重复，方便按业务分类筛选；若某制度没有任何要求条款，则该制度单独占一行。

## 注意

- `input/` 与 `output/` 默认不纳入版本管理（内部文档与生成结果）。
- `extractor.py` 中显式设置了 `extra_body={"thinking": {"type": "disabled"}}`，
  因为 DeepSeek V4 默认开启 thinking 模式且不支持强制 `tool_choice`，不关闭会返回 400。
- `deepseek-chat` / `deepseek-reasoner` 已于 2026-07-24 退役，请使用 `deepseek-v4-flash` 或 `deepseek-v4-pro`。
