# splitter.py
import re
from docx import Document

def read_docx(path: str) -> str:
    doc = Document(path)
    lines = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    return "\n".join(lines)

def split_by_sections(text: str) -> list[str]:
    """
    按“一、”、“二、”、“三、”、“四、”、“五、”切分文档。
    注意避开目录部分。
    """
    # 定位正文开始的位置（跳过目录）
    start_match = re.search(r"一、软件权限管理制度", text)
    if not start_match:
        raise ValueError("未找到正文起始位置")
    
    text = text[start_match.start():]
    
    # 匹配以 一、 二、 三、 四、 五、 开头（行首或换行后）
    pattern = re.compile(r"(?=(?:一|二|三|四|五)、)", re.MULTILINE)
    parts = [p.strip() for p in pattern.split(text) if p.strip()]
    
    # 过滤有效段
    segments = [p for p in parts if "目的：" in p or "具体内容：" in p]
    return segments

if __name__ == "__main__":
    from config import INPUT_DOCX
    txt = read_docx(INPUT_DOCX)
    segs = split_by_sections(txt)
    print(f"共切分 {len(segs)} 段")
    for i, s in enumerate(segs, 1):
        print(f"--- 第{i}段标题前30字 ---\n{s[:30]}\n")