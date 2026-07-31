"""
AIGO 教程系列 - 基本任务·文献调研 Agent
ep21-table-extraction: 表格与数据的精准抽取

从 MinerU 解析出的 markdown 中识别表格（正则匹配 | 分隔的表格行），
提取数值+单位，做简单的单位归一化（如 GPa → MPa）。
"""

from __future__ import annotations

import re

# ── 模拟 MinerU 解析出的 Markdown 文本 ────────────────────────

SAMPLE_MARKDOWN = """
# 3. Results and Discussion

The mechanical properties of the synthesized samples are summarized below.

| Sample | Young's Modulus (GPa) | Hardness (GPa) | Fracture Toughness (MPa*m^0.5) |
|--------|----------------------|----------------|-------------------------------|
| S1     | 210                  | 12.5           | 3.2                           |
| S2     | 185                  | 10.8           | 4.1                           |
| S3     | 230                  | 14.2           | 2.9                           |

The electrochemical performance is shown in the following table.

| Sample | Capacity (mAh/g) | Cycling (cycles) | Retention (%) |
|--------|------------------|-------------------|---------------|
| S1     | 165              | 200               | 91.3          |
| S2     | 178              | 300               | 88.5          |
| S3     | 152              | 150               | 95.0          |
"""

# ── 单位换算规则 ──────────────────────────────────────────────

# 目标：将所有力学量统一为 MPa
UNIT_CONVERSION_TO_MPA = {
    "GPa": 1000.0,   # 1 GPa = 1000 MPa
    "MPa": 1.0,
    "kPa": 0.001,    # 1 kPa = 0.001 MPa
    "Pa":  1e-6,     # 1 Pa  = 1e-6 MPa
}


def extract_tables(markdown: str) -> list[list[list[str]]]:
    """从 Markdown 文本中识别所有表格，返回表格数据（二维列表的列表）。"""
    lines = markdown.split("\n")
    tables: list[list[list[str]]] = []
    current_table: list[list[str]] = []

    for line in lines:
        stripped = line.strip()
        # 判断是否为表格行（以 | 开头和结尾）
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            # 跳过分隔行（如 |---|---|）
            if all(re.match(r"^[-:]+$", c) for c in cells):
                continue
            current_table.append(cells)
        else:
            if current_table:
                tables.append(current_table)
                current_table = []

    # 末尾的表格
    if current_table:
        tables.append(current_table)
    return tables


def extract_values_with_units(tables: list[list[list[str]]]) -> list[dict]:
    """从表格中提取数值+单位，返回结构化记录列表。"""
    records = []
    for table in tables:
        if len(table) < 2:
            continue
        headers = table[0]
        for row in table[1:]:
            record = {}
            for col_name, cell_value in zip(headers, row):
                # 尝试提取数值和单位
                match = re.match(r"([\d.]+)\s*([a-zA-Z·^/\-]+)?", cell_value)
                if match:
                    num = float(match.group(1))
                    unit = match.group(2) or ""
                    record[col_name] = {"value": num, "unit": unit}
                else:
                    # 非数值列（如样品名）
                    record[col_name] = {"value": cell_value, "unit": None}
            records.append(record)
    return records


def normalize_unit(value: float, unit: str) -> tuple[float, str]:
    """将力学单位统一归一化为 MPa。非力学单位原样返回。"""
    if unit in UNIT_CONVERSION_TO_MPA:
        return value * UNIT_CONVERSION_TO_MPA[unit], "MPa"
    return value, unit


def normalize_records(records: list[dict]) -> list[dict]:
    """对所有记录做单位归一化。"""
    for record in records:
        for key, item in record.items():
            if isinstance(item, dict) and item.get("unit"):
                val, new_unit = normalize_unit(item["value"], item["unit"])
                if new_unit != item["unit"]:
                    print(f"  单位换算: {item['value']} {item['unit']} → {val} {new_unit}")
                item["value"] = val
                item["unit"] = new_unit
    return records


def main():
    print("=" * 55)
    print("  表格识别与数据抽取")
    print("=" * 55)

    # 1. 识别表格
    tables = extract_tables(SAMPLE_MARKDOWN)
    print(f"\n共识别到 {len(tables)} 个表格")
    for i, table in enumerate(tables):
        print(f"  表格 {i+1}: {len(table)} 行 x {len(table[0])} 列")

    # 2. 提取数值+单位
    print("\n--- 抽取数值与单位 ---")
    records = extract_values_with_units(tables)
    for rec in records:
        print(f"  {rec}")

    # 3. 单位归一化
    print("\n--- 单位归一化（力学量 → MPa）---")
    normalized = normalize_records(records)

    # 4. 打印归一化后的结果
    print("\n--- 归一化结果 ---")
    for rec in normalized:
        parts = []
        for key, item in rec.items():
            if isinstance(item, dict):
                parts.append(f"{key}={item['value']} {item['unit'] or ''}".strip())
            else:
                parts.append(f"{key}={item}")
        print(f"  {' | '.join(parts)}")


if __name__ == "__main__":
    main()
