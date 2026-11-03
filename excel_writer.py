# excel_writer.py
"""把抽取结果逐条写入 Excel。

设计：每行 = 一条「要求条款」(requirements 里的 item)；
制度级字段（名称/部门/目的等）在每条上重复，方便后续按分类筛选。
若某制度没有任何要求条款，则整条制度单独写一行（条款相关列留空）。
"""
import os
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill

# 列定义：(中文表头, 取值函数(record, item))
# item 为 None 时表示「仅制度概览」行（无要求条款）
COLUMNS = [
    ("制度名称",  lambda r, it: r.get("system_name", "")),
    ("起草部门",  lambda r, it: r.get("drafting_department", "")),
    ("执行部门",  lambda r, it: r.get("executing_department", "")),
    ("监督部门",  lambda r, it: r.get("supervising_department") or ""),
    ("目的",      lambda r, it: r.get("purpose", "")),
    ("适用范围",  lambda r, it: r.get("applicable_scope", "")),
    ("流程示意",  lambda r, it: r.get("process_flow") or ""),
    ("条款编号",  lambda r, it: it.get("item_no", "") if it else ""),
    ("条款内容",  lambda r, it: it.get("content", "") if it else ""),
    ("业务分类",  lambda r, it: it.get("category", "") if it else ""),
    ("原文片段",  lambda r, it: r.get("source_text", "")),
]


def write_to_excel(records: list, output_path: str) -> int:
    """逐条写入 Excel。

    Args:
        records: extract_system 返回的记录列表
        output_path: 输出 .xlsx 路径
    Returns:
        写入的数据行数（不含表头）
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "要求明细"

    # ---- 表头 ----
    headers = [name for name, _ in COLUMNS]
    ws.append(headers)

    header_fill = PatternFill("solid", fgColor="4472C4")
    header_font = Font(bold=True, color="FFFFFF", size=11)
    for col_idx in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    # ---- 逐条写入：每个制度下的每条要求写一行 ----
    row_count = 0
    for record in records:
        items = record.get("requirements") or []
        if items:
            for item in items:
                ws.append([fn(record, item) for _, fn in COLUMNS])
                row_count += 1
        else:
            # 没有要求条款时，整条制度也写一行
            ws.append([fn(record, None) for _, fn in COLUMNS])
            row_count += 1

    # ---- 样式：自动列宽 + 文本换行 + 冻结表头 ----
    for col_cells in ws.columns:
        col_letter = col_cells[0].column_letter
        max_len = 0
        for cell in col_cells:
            val = cell.value
            if val is not None:
                # 中文/全角按 2 个字符宽度估算
                length = sum(2 if ord(ch) > 127 else 1 for ch in str(val))
                max_len = max(max_len, length)
        ws.column_dimensions[col_letter].width = min(max(max_len + 2, 10), 60)

    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, max_col=len(headers)):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)

    ws.freeze_panes = "A2"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    wb.save(output_path)
    return row_count
