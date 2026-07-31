"""
AIGO 教程系列 - 基本任务·文献调研 Agent
ep19-extraction-schema: 知识抽取任务定义

定义抽取 Schema（JSON 格式），包含材料成分、结构参数、性能指标、合成条件。
打印 schema 示例，演示什么是结构化抽取。
"""

import json

# ── 定义抽取 Schema ─────────────────────────────────────────

EXTRACTION_SCHEMA = {
    "title": "材料科学文献知识抽取 Schema",
    "description": "从论文中抽取结构化知识，用于构建材料科学领域知识库",
    "fields": {
        "material": {
            "description": "材料成分与名称",
            "example": "LiCoO2",
            "sub_fields": {
                "name": "材料通用名称",
                "formula": "化学式（标准格式）",
                "category": "材料类别（正极/负极/电解质/催化剂等）",
            },
        },
        "structure": {
            "description": "结构参数",
            "example": {"crystal_system": "六方", "space_group": "R-3m", "lattice_a": "2.82 A"},
            "sub_fields": {
                "crystal_system": "晶系",
                "space_group": "空间群",
                "lattice_parameters": "晶格参数（a, b, c, α, β, γ）",
                "morphology": "形貌（纳米线/薄膜/颗粒等）",
            },
        },
        "property": {
            "description": "性能指标",
            "example": {
                "property_name": "比容量", "value": 180,
                "unit": "mAh/g", "condition": "0.1C, 25°C",
            },
            "sub_fields": {
                "property_name": "性能名称（比容量/电导率/循环寿命等）",
                "value": "数值",
                "unit": "单位",
                "condition": "测试条件（温度/倍率/电压范围等）",
            },
        },
        "synthesis": {
            "description": "合成条件",
            "example": {
                "method": "溶胶-凝胶法", "temperature": "700°C",
                "time": "12 h", "atmosphere": "空气",
            },
            "sub_fields": {
                "method": "合成方法",
                "temperature": "合成温度",
                "time": "合成时间",
                "atmosphere": "气氛",
                "precursors": "前驱体",
            },
        },
    },
}


def print_schema_overview():
    """打印 Schema 概览，帮助理解结构化抽取的目标。"""
    print("=" * 60)
    print("  材料科学文献知识抽取 Schema")
    print("=" * 60)

    for field_name, field_info in EXTRACTION_SCHEMA["fields"].items():
        print(f"\n【{field_name}】{field_info['description']}")
        print(f"  示例: {json.dumps(field_info['example'], ensure_ascii=False)}")
        print("  子字段:")
        for sub_key, sub_desc in field_info["sub_fields"].items():
            print(f"    - {sub_key}: {sub_desc}")


def show_extraction_example():
    """展示一段文本 → 结构化结果的示例，说明什么是结构化抽取。"""
    # 模拟一段论文摘要
    raw_text = (
        "本文采用溶胶-凝胶法合成了纳米级 LiCoO2 正极材料。"
        "在 700°C 空气气氛中烧结 12 小时后，"
        "所得材料在 0.1C 倍率、25°C 条件下展现出 180 mAh/g 的比容量，"
        "循环 100 次后容量保持率为 92%。"
    )

    # 期望抽取出的结构化结果
    expected_result = {
        "material": {
            "name": "钴酸锂",
            "formula": "LiCoO2",
            "category": "正极材料",
        },
        "structure": {
            "morphology": "纳米颗粒",
        },
        "property": [
            {"property_name": "比容量", "value": 180, "unit": "mAh/g",
             "condition": "0.1C, 25°C"},
            {"property_name": "容量保持率", "value": 92, "unit": "%",
             "condition": "100 次循环"},
        ],
        "synthesis": {
            "method": "溶胶-凝胶法",
            "temperature": "700°C",
            "time": "12 h",
            "atmosphere": "空气",
        },
    }

    print("\n" + "=" * 60)
    print("  结构化抽取示例")
    print("=" * 60)
    print(f"\n原始文本:\n  {raw_text}")
    print(f"\n抽取结果:\n{json.dumps(expected_result, ensure_ascii=False, indent=2)}")


def main():
    # 1. 打印 Schema 概览
    print_schema_overview()

    # 2. 展示抽取示例
    show_extraction_example()

    # 3. 导出 Schema 为 JSON 文件（便于后续使用）
    schema_path = "extraction_schema.json"
    with open(schema_path, "w", encoding="utf-8") as f:
        json.dump(EXTRACTION_SCHEMA, f, ensure_ascii=False, indent=2)
    print(f"\n\nSchema 已导出至: {schema_path}")


if __name__ == "__main__":
    main()
