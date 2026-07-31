"""
AIGO 教程系列 - 基本任务·文献调研 Agent
ep27-gap-evaluation: Gap 的新颖性与可操作性评估

对发现的 gap 做交叉验证——用 Sciverse 搜索是否真的没人做过。
评估 gap 的"真空白"程度。
"""

import json
import sys
from pathlib import Path

# 导入共享模块
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from sciverse_client import SciverseClient

# ── 待评估的 Gap 列表（模拟从 ep26 输出） ─────────────────────

DISCOVERED_GAPS = [
    {
        "id": 1,
        "title": "LiFePO4 在 -30°C 以下的电化学性能",
        "type": "missing_data",
        "search_query": "LiFePO4 low temperature electrochemistry below -30",
        "description": "现有研究最低只到 -20°C，-30°C 以下无数据",
    },
    {
        "id": 2,
        "title": "LLZO 晶界阻抗的定量贡献",
        "type": "contradiction",
        "search_query": "LLZO grain boundary impedance contribution",
        "description": "不同团队对晶界阻抗占比结论矛盾（10% vs 70%）",
    },
    {
        "id": 3,
        "title": "ML 预测热电材料载流子浓度",
        "type": "cross_domain",
        "search_query": "machine learning thermoelectric carrier concentration",
        "description": "ML 在催化剂中成功但在热电材料中应用极少",
    },
]


def evaluate_gap_novelty(client: SciverseClient, gap: dict) -> dict:
    """
    用 Sciverse 搜索验证 gap 的新颖性。
    搜索结果越少，说明 gap 越"真空白"。
    """
    query = gap["search_query"]
    print(f"\n  搜索验证: \"{query}\"")

    try:
        results = client.search_papers(query, page_size=5)
        papers = results.get("results", [])
        total = results.get("total", len(papers))
    except Exception as e:
        print(f"  搜索失败: {e}")
        return {**gap, "related_count": None, "novelty_score": None, "error": str(e)}

    # 统计相关论文数量
    related_count = total
    print(f"  找到 {related_count} 篇相关论文")

    # 计算新颖性评分（论文越少越新颖，0-10 分）
    if related_count == 0:
        novelty_score = 10.0
    elif related_count <= 3:
        novelty_score = 8.0
    elif related_count <= 10:
        novelty_score = 5.0
    elif related_count <= 50:
        novelty_score = 3.0
    else:
        novelty_score = 1.0

    # 打印最相关的几篇
    for p in papers[:3]:
        title = p.get("title", "N/A")
        year = p.get("publication_published_year", "N/A")
        print(f"    - [{year}] {title}")

    return {
        **gap,
        "related_count": related_count,
        "novelty_score": novelty_score,
    }


def assess_feasibility(gap: dict) -> str:
    """
    简单评估 gap 的可操作性。
    基于 gap 类型给出可行性评级。
    """
    feasibility_map = {
        "missing_data":    "高 — 只需补充实验数据",
        "contradiction":   "中 — 需要设计更严谨的对照实验",
        "unexplored_region": "高 — 系统性实验/计算即可覆盖",
        "method_gap":      "低 — 需要开发新方法，周期长",
        "cross_domain":    "中 — 需要跨学科合作",
    }
    return feasibility_map.get(gap["type"], "未知")


def main():
    print("=" * 55)
    print("  Gap 新颖性与可操作性评估")
    print("=" * 55)

    # 初始化 Sciverse 客户端
    try:
        client = SciverseClient()
    except ValueError as e:
        print(f"\n注意: {e}")
        print("将使用模拟数据演示评估流程。\n")
        client = None

    evaluated_gaps = []

    for gap in DISCOVERED_GAPS:
        print(f"\n{'─' * 55}")
        print(f"Gap {gap['id']}: {gap['title']}")
        print(f"类型: {gap['type']}")

        # 新颖性验证
        if client:
            result = evaluate_gap_novelty(client, gap)
        else:
            # 模拟结果
            result = {**gap, "related_count": 0, "novelty_score": 10.0}
            print(f"  [模拟] 假设搜索结果为空，新颖性评分: 10.0")

        # 可操作性评估
        feasibility = assess_feasibility(gap)
        result["feasibility"] = feasibility
        print(f"  可操作性: {feasibility}")

        evaluated_gaps.append(result)

    # 汇总报告
    print("\n\n" + "=" * 55)
    print("  评估汇总")
    print("=" * 55)
    print(f"{'Gap':<35} {'新颖性':<8} {'相关论文':<8} {'可操作性'}")
    print("-" * 75)
    for g in evaluated_gaps:
        score = f"{g['novelty_score']:.0f}" if g.get("novelty_score") else "N/A"
        count = str(g.get("related_count", "N/A"))
        print(f"{g['title']:<35} {score:<8} {count:<8} {g['feasibility']}")


if __name__ == "__main__":
    main()
