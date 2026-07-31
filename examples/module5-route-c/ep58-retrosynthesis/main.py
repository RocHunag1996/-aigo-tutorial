"""
AIGO 教程系列 - 路线 C·合成路线与工艺设计
ep58-retrosynthesis: 逆向合成分析基础
LLM 驱动：从目标产物递归拆解为可用前驱体
"""

import sys
from pathlib import Path
import os
import json

# 导入共享 LLM 模块
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from llm_call import llm_call_json


RETRO_PROMPT = """你是材料化学逆向合成专家。给定目标材料，请进行逆向合成分析。

目标材料：{target}

请拆解为 2-3 种可行的合成路线，每条路线包含：
- 前驱体列表（必须是商业可得的原料）
- 合成方法
- 关键反应条件
- 可能的挑战

以 JSON 返回：
{{
    "target": "{target}",
    "routes": [
        {{
            "route_id": 1,
            "method": "合成方法",
            "precursors": ["前驱体1", "前驱体2"],
            "steps": ["步骤1", "步骤2"],
            "temperature_c": 数字,
            "challenges": ["挑战1"],
            "feasibility": "高/中/低"
        }}
    ]
}}"""


def retrosynthesis_analysis(target: str) -> dict:
    """对目标材料进行逆向合成分析"""
    try:
        result = llm_call_json(
            RETRO_PROMPT.format(target=target),
            system="你是材料化学逆向合成专家，只返回 JSON。"
        )
        return result
    except Exception as e:
        print(f"  [警告] LLM 调用失败: {e}")
        return None


def demo_retrosynthesis():
    """演示逆向合成分析（无需 API key）"""
    target = "Li7La3Zr2O12 (LLZO) 固态电解质"

    print("=" * 60)
    print(f"逆向合成分析目标: {target}")
    print("=" * 60)

    result = retrosynthesis_analysis(target)

    if result:
        print("\nLLM 分析结果：")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 演示模式：展示预期输出结构
        print("\n[演示模式] 预期逆向合成结果：")
        demo_result = {
            "target": target,
            "routes": [
                {
                    "route_id": 1,
                    "method": "固相法",
                    "precursors": ["Li2CO3", "La2O3", "ZrO2"],
                    "steps": [
                        "按化学计量比称量前驱体",
                        "球磨混合 12h",
                        "800°C 预烧 6h",
                        "1100°C 烧结 12h"
                    ],
                    "temperature_c": 1100,
                    "challenges": ["Li 挥发需过量 5-10%", "立方相稳定性控制"],
                    "feasibility": "高"
                },
                {
                    "route_id": 2,
                    "method": "溶胶-凝胶法",
                    "precursors": ["LiNO3", "La(NO3)3", "Zr(O-nBu)4", "柠檬酸"],
                    "steps": [
                        "配制金属盐溶液",
                        "加入柠檬酸络合",
                        "80°C 水浴成凝胶",
                        "120°C 干燥过夜",
                        "750°C 煅烧 6h"
                    ],
                    "temperature_c": 750,
                    "challenges": ["批次一致性", "大规模生产成本高"],
                    "feasibility": "中"
                }
            ]
        }
        print(json.dumps(demo_result, ensure_ascii=False, indent=2))

    return result


def recursive_decompose(target: str, depth: int = 0, max_depth: int = 2):
    """递归拆解目标材料（展示思路，不实际调用 LLM）"""
    indent = "  " * depth
    print(f"{indent}{'└─ ' if depth > 0 else ''}目标: {target}")

    if depth >= max_depth:
        print(f"{indent}   └─ [商业可得前驱体]")
        return

    # 模拟拆解过程
    decompositions = {
        "Li7La3Zr2O12": ["Li2CO3", "La2O3", "ZrO2"],
        "La2O3": ["La(NO3)3", "LaCl3"],
        "ZrO2": ["Zr(O-nBu)4", "ZrCl4"],
    }

    sub_items = decompositions.get(target, [])
    if sub_items:
        for item in sub_items:
            recursive_decompose(item, depth + 1, max_depth)
    else:
        print(f"{indent}   └─ [可直接采购]")


def main():
    print("ep58 - 逆向合成分析基础")
    print("=" * 60)

    # 演示 LLM 逆向合成
    demo_retrosynthesis()

    # 展示递归拆解思路
    print("\n" + "=" * 60)
    print("递归拆解思路演示")
    print("=" * 60)
    recursive_decompose("Li7La3Zr2O12")

    print("\n" + "-" * 40)
    print("逆向合成核心逻辑：")
    print("""
    1. 确定目标材料（产物）
    2. LLM 推理可行的合成路线
    3. 每条路线拆解为：前驱体 + 方法 + 条件
    4. 评估可行性（热力学/动力学/成本）
    5. 与知识库（ep57）交叉验证
    6. 输出最优路线供实验参考
    """)


if __name__ == "__main__":
    main()
