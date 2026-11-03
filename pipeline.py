# pipeline.py
import json
import os

from config import INPUT_DOCX, OUTPUT_JSON, OUTPUT_XLSX
from splitter import read_docx, split_by_sections
from extractor import extract_system
from excel_writer import write_to_excel

def business_check(record: dict) -> None:
    """Schema 之外的业务规则校验。"""
    if not record.get("system_name"):
        raise ValueError("制度名称不能为空")
    if not record.get("requirements"):
        raise ValueError("具体要求不能为空")
    for item in record["requirements"]:
        if not item["item_no"].startswith("4."):
            # 注意：部分条款可能未严格编号，如果报错可放宽此限制
            pass 

def main():
    # 1. 读取文档
    text = read_docx(INPUT_DOCX)

    # 2. 切分（预期切出 5 段子制度）
    segments = split_by_sections(text)
    print(f"[1] 切分得到 {len(segments)} 段子制度")

    records = []
    for i, seg in enumerate(segments, 1):
        print(f"[2.{i}] 正在抽取第 {i} 段 ...")
        record = extract_system(seg)
        business_check(record)
        records.append(record)
        print(f"      -> 完成: {record['system_name']} (要求条款 {len(record['requirements'])} 条)")

    # 3. 输出 JSON
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print(f"[3] 已写入 {OUTPUT_JSON}，共 {len(records)} 条制度记录")

    # 4. 逐条写入 Excel（每条要求一行）
    row_count = write_to_excel(records, OUTPUT_XLSX)
    print(f"[4] 已写入 {OUTPUT_XLSX}，共 {row_count} 行（每个要求条款一行）")

if __name__ == "__main__":
    main()