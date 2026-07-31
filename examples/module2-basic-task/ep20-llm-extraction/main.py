"""
AIGO 教程系列 - 基本任务·文献调研 Agent
ep20-llm-extraction: 用 LLM 做信息抽取

给一段论文摘要文本，用 llm_call_json 抽取结构化数据（材料名、性能值、方法）。
设计抽取 prompt，解析 JSON 输出。
"""

import json
import sys
from pathlib import Path

# 导入共享模块
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from llm_call import llm_call_json

# ── 待抽取的论文摘要（示例） ─────────────────────────────────

SAMPLE_ABSTRACT = """
We report a high-performance solid-state lithium-ion battery using a
Li7La3Zr2O12 (LLZO) garnet-type solid electrolyte. The LLZO pellets were
synthesized via a conventional solid-state reaction at 1100 deg C for 6 hours
in air. The ionic conductivity of the optimized LLZO electrolyte reaches
1.2 mS/cm at 25 deg C. A LiFePO4 cathode with a specific capacity of 155 mAh/g
was achieved at 0.5C. The full cell demonstrated excellent cycling stability
with 89% capacity retention after 500 cycles at room temperature.
""".strip()

# ── 设计抽取 Prompt ──────────────────────────────────────────

EXTRACTION_SYSTEM = """你是一个材料科学文献信息抽取专家。
请从用户提供的论文摘要中抽取结构化信息，严格按以下 JSON 格式输出：
{
  "materials": [
    {
      "name": "材料名称",
      "formula": "化学式",
      "role": "在电池中的角色（如正极/负极/电解质等）"
    }
  ],
  "properties": [
    {
      "property_name": "性能指标名称",
      "value": 数值,
      "unit": "单位",
      "condition": "测试条件"
    }
  ],
  "methods": [
    {
      "method_name": "方法名称",
      "material": "所用材料",
      "parameters": "关键参数"
    }
  ]
}
只输出 JSON，不要任何解释。如某字段在文本中未提及，填 null。"""


def extract_from_abstract(text: str) -> dict:
    """调用 LLM 从摘要中抽取结构化信息。"""
    prompt = f"请从以下论文摘要中抽取结构化信息：\n\n{text}"
    result = llm_call_json(prompt, system=EXTRACTION_SYSTEM, temperature=0.1)
    return result


def print_extraction_result(result: dict):
    """格式化打印抽取结果。"""
    print("=" * 50)
    print("  LLM 信息抽取结果")
    print("=" * 50)

    # 材料列表
    print("\n【材料】")
    for mat in result.get("materials", []):
        print(f"  - {mat.get('name', 'N/A')} ({mat.get('formula', 'N/A')}) "
              f"— 角色: {mat.get('role', 'N/A')}")

    # 性能指标
    print("\n【性能指标】")
    for prop in result.get("properties", []):
        print(f"  - {prop.get('property_name', 'N/A')}: "
              f"{prop.get('value', 'N/A')} {prop.get('unit', '')} "
              f"[{prop.get('condition', 'N/A')}]")

    # 合成/测试方法
    print("\n【方法】")
    for method in result.get("methods", []):
        print(f"  - {method.get('method_name', 'N/A')} "
              f"(材料: {method.get('material', 'N/A')}, "
              f"参数: {method.get('parameters', 'N/A')})")


def main():
    print("原文摘要:")
    print(f"  {SAMPLE_ABSTRACT}\n")

    # 调用 LLM 进行结构化抽取
    result = extract_from_abstract(SAMPLE_ABSTRACT)

    # 打印结果
    print_extraction_result(result)

    # 同时输出原始 JSON 便于查看
    print(f"\n\n原始 JSON 输出:\n{json.dumps(result, ensure_ascii=False, indent=2)}")


if __name__ == "__main__":
    main()
