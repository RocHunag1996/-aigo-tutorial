"""
AIGO 教程系列 - 基本任务·文献调研 Agent
ep25-gap-prompt: 用 LLM 辅助识别 Gap

给 LLM 多篇论文的摘要，让它对比分析找出矛盾和缺失。
设计 prompt 让 LLM 输出结构化的 gap 列表（JSON 格式）。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# 导入共享模块
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from llm_call import llm_call_json

# ── 模拟多篇论文摘要 ──────────────────────────────────────────

PAPER_ABSTRACTS = [
    {
        "title": "Paper A: High-rate performance of LFP cathodes",
        "abstract": (
            "LiFePO4 cathodes were synthesized via carbon coating. "
            "At 25 deg C, the specific capacity reaches 160 mAh/g at 1C rate. "
            "At -10 deg C, the capacity drops to 95 mAh/g at 0.5C."
        ),
    },
    {
        "title": "Paper B: Low-temperature LFP with electrolyte optimization",
        "abstract": (
            "Using a novel ether-based electrolyte, LiFePO4 achieves "
            "140 mAh/g at -20 deg C and 0.2C rate. The improvement is "
            "attributed to the low viscosity of the electrolyte at low temperature."
        ),
    },
    {
        "title": "Paper C: Contradictory findings on LFP low-temp performance",
        "abstract": (
            "We find that the rate-limiting step at low temperature for LFP "
            "is charge transfer at the electrode-electrolyte interface, not "
            "ion diffusion. Carbon coating shows negligible improvement below -20 deg C."
        ),
    },
    {
        "title": "Paper D: Machine learning for battery materials",
        "abstract": (
            "A graph neural network model predicts the voltage profile of "
            "cathode materials with 50 meV accuracy. The model is trained on "
            "DFT data from the Materials Project database."
        ),
    },
]

# ── Gap 识别 Prompt ──────────────────────────────────────────

GAP_SYSTEM = """你是一位材料科学研究分析专家。请对比分析多篇论文摘要，找出以下类型的 Research Gap：
1. 缺失数据型：某材料/体系的关键性能数据尚缺
2. 矛盾结论型：不同论文得出相互矛盾的结论
3. 未探索区间型：成分/条件/参数空间中尚未覆盖的区域
4. 方法空白型：缺乏合适的研究/表征手段
5. 跨领域连接缺失型：一个领域的方法未迁移到另一个相关领域

请严格按以下 JSON 格式输出：
{
  "gaps": [
    {
      "type": "gap 类型（英文：missing_data/contradiction/unexplored_region/method_gap/cross_domain）",
      "title": "简短标题",
      "description": "详细描述",
      "related_papers": ["相关论文标题"],
      "potential_impact": "该 Gap 的影响和研究价值"
    }
  ]
}
只输出 JSON，不要额外解释。"""


def identify_gaps(papers: list[dict]) -> dict:
    """调用 LLM 对比分析论文，识别 Research Gap。"""
    # 拼接所有论文摘要
    paper_text = ""
    for i, p in enumerate(papers, 1):
        paper_text += f"\n[{i}] {p['title']}\n    {p['abstract']}\n"

    prompt = (
        f"以下是 {len(papers)} 篇关于锂电池材料的论文摘要，"
        f"请对比分析并找出 Research Gap：\n{paper_text}"
    )
    result = llm_call_json(prompt, system=GAP_SYSTEM, temperature=0.3)
    return result


def print_gaps(result: dict):
    """格式化打印识别出的 Gap 列表。"""
    gaps = result.get("gaps", [])
    print("=" * 55)
    print(f"  共识别到 {len(gaps)} 个 Research Gap")
    print("=" * 55)

    for i, gap in enumerate(gaps, 1):
        print(f"\n{'─' * 55}")
        print(f"Gap {i}: [{gap.get('type', 'N/A')}] {gap.get('title', 'N/A')}")
        print(f"  描述: {gap.get('description', 'N/A')}")
        related = gap.get("related_papers", [])
        if related:
            print(f"  相关论文: {', '.join(related)}")
        print(f"  影响: {gap.get('potential_impact', 'N/A')}")


def main():
    print("输入论文摘要:")
    for i, p in enumerate(PAPER_ABSTRACTS, 1):
        print(f"  [{i}] {p['title']}")

    # 调用 LLM 识别 Gap
    result = identify_gaps(PAPER_ABSTRACTS)

    # 打印结果
    print_gaps(result)

    # 输出原始 JSON
    print(f"\n\n原始 JSON:\n{json.dumps(result, ensure_ascii=False, indent=2)}")


if __name__ == "__main__":
    main()
