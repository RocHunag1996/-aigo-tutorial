"""
AIGO 教程系列 - 路线 C·合成路线与工艺设计
ep56-synthesis-mining: 合成文献的数据挖掘
用 LLM 从论文文本中提取合成条件（温度、时间、前驱体等）
"""

import sys
from pathlib import Path
import os
import json

# 导入共享 LLM 模块
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from llm_call import llm_call_json


# 合成条件提取的 prompt 模板
EXTRACTION_PROMPT = """请从以下材料科学论文片段中提取合成条件信息。

论文片段：
{text}

请以 JSON 格式返回，包含以下字段（如果文中未提及则填 null）：
{{
    "material_name": "目标材料名称",
    "synthesis_method": "合成方法（如固相法、溶胶-凝胶、水热法等）",
    "precursors": ["前驱体列表"],
    "temperature_c": "煅烧/反应温度（摄氏度，数字）",
    "time_hours": "反应时间（小时，数字）",
    "atmosphere": "反应气氛（如空气、氮气、氩气等）",
    "heating_rate": "升温速率（°C/min）",
    "solvent": "溶剂",
    "ph_value": "pH值",
    "post_treatment": "后处理步骤描述"
}}"""


def extract_synthesis_conditions(text: str) -> dict:
    """调用 LLM 从文本中提取合成条件"""
    try:
        result = llm_call_json(
            EXTRACTION_PROMPT.format(text=text),
            system="你是材料科学合成专家，擅长从论文中提取实验条件。只返回 JSON。"
        )
        return result
    except Exception as e:
        print(f"  [警告] LLM 调用失败: {e}")
        return None


def demo_extraction():
    """演示：用示例文本提取合成条件（无需 API key 时展示流程）"""
    sample_text = """
    We synthesized Li7La3Zr2O12 (LLZO) garnet-type solid electrolyte
    via a sol-gel method. LiNO3, La(NO3)3·6H2O, and Zr(O-nBu)4 were
    used as precursors, with citric acid as the chelating agent.
    The molar ratio of Li:La:Zr was set to 7.15:3:2 (5% excess Li
    to compensate for volatilization). The gel was dried at 120°C
    overnight, then calcined at 750°C for 6 hours in air. The
    resulting powder was pressed into pellets and sintered at
    1100°C for 12 hours with a heating rate of 5°C/min.
    """

    print("=" * 60)
    print("演示：从论文片段提取合成条件")
    print("=" * 60)
    print(f"\n论文片段（摘要）:\n{sample_text.strip()}")
    print("\n" + "-" * 60)

    # 尝试调用 LLM
    result = extract_synthesis_conditions(sample_text)

    if result:
        print("\n提取结果：")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 无 API key 时展示预期输出
        print("\n[演示模式] 预期提取结果：")
        expected = {
            "material_name": "Li7La3Zr2O12 (LLZO)",
            "synthesis_method": "溶胶-凝胶法 (sol-gel)",
            "precursors": ["LiNO3", "La(NO3)3·6H2O", "Zr(O-nBu)4", "柠檬酸"],
            "temperature_c": [750, 1100],
            "time_hours": [6, 12],
            "atmosphere": "空气",
            "heating_rate": "5 °C/min",
            "solvent": None,
            "ph_value": None,
            "post_treatment": "压片后 1100°C 烧结 12h",
        }
        print(json.dumps(expected, ensure_ascii=False, indent=2))

    return result


def batch_extract(papers: list[dict]) -> list[dict]:
    """批量提取多篇论文的合成条件"""
    results = []
    for i, paper in enumerate(papers):
        print(f"\n[{i+1}/{len(papers)}] 正在提取: {paper.get('title', '未知')}")
        extracted = extract_synthesis_conditions(paper.get("text", ""))
        if extracted:
            extracted["source_paper"] = paper.get("title", "未知")
            results.append(extracted)
            print(f"  -> 方法: {extracted.get('synthesis_method', 'N/A')}")
        else:
            print("  -> 提取失败")
    return results


def main():
    print("ep56 - 合成文献的数据挖掘")
    print("=" * 60)

    # 演示单篇提取
    demo_extraction()

    # 展示批量处理流程
    print("\n" + "=" * 60)
    print("批量提取流程说明")
    print("=" * 60)
    print("""
    批量处理步骤：
    1. 准备论文列表（标题 + 全文/摘要文本）
    2. 逐篇调用 LLM 提取合成条件
    3. 结果存入结构化数据库（见 ep57）
    4. 支持按材料体系/合成方法检索

    关键技巧：
    - 分段提取：长论文分段送 LLM，避免超 token 限制
    - 多次提取取交集：同一段落提取多次，保留一致结果
    - 单位归一化：温度统一为 °C，时间统一为小时
    """)


if __name__ == "__main__":
    main()
