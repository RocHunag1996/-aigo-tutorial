"""
AIGO 教程系列 - 基本任务·文献调研 Agent
ep28-report-agent: 报告生成 Agent

从 gap 清单出发，用 LLM 生成结构化综述报告。
设计报告模板（引言、方法对比、gap 分析、展望），自动填充内容。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# 导入共享模块
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from llm_call import llm_call

# ── 报告模板 ──────────────────────────────────────────────────

REPORT_TEMPLATE = """# {title}

## 1. 引言

{introduction}

## 2. 研究现状与方法对比

{method_comparison}

## 3. Research Gap 分析

{gap_analysis}

## 4. 未来展望与建议

{outlook}

## 5. 参考文献

{references}
"""

# ── 输入数据：Gap 清单与论文信息 ──────────────────────────────

GAP_LIST = [
    {
        "title": "LiFePO4 在 -30°C 以下的电化学性能数据缺失",
        "type": "缺失数据型",
        "novelty_score": 9,
        "description": "现有研究最低只到 -20°C，极低温下的性能数据几乎空白。",
    },
    {
        "title": "LLZO 晶界阻抗的定量贡献存在矛盾",
        "type": "矛盾结论型",
        "novelty_score": 7,
        "description": "不同团队对晶界阻抗占总阻抗的比例结论差异巨大（10% vs 70%）。",
    },
    {
        "title": "机器学习方法尚未迁移到热电材料载流子优化",
        "type": "跨领域连接缺失型",
        "novelty_score": 8,
        "description": "ML 在催化剂活性位点预测中成功，但热电材料领域鲜有应用。",
    },
]

PAPER_SUMMARIES = [
    {"title": "Paper A", "year": 2023, "finding": "LFP 在 -10°C 容量为 95 mAh/g"},
    {"title": "Paper B", "year": 2024, "finding": "醚类电解质使 LFP 在 -20°C 达 140 mAh/g"},
    {"title": "Paper C", "year": 2024, "finding": "低温瓶颈为界面电荷转移而非离子扩散"},
]


# ── 各章节生成函数 ────────────────────────────────────────────

def generate_introduction(topic: str) -> str:
    """用 LLM 生成引言部分。"""
    prompt = (
        f"请为以下主题写一段 200 字左右的学术综述引言：\n"
        f"主题：{topic}\n"
        f"要求：介绍研究背景、重要性、当前挑战。语言简洁专业。"
    )
    return llm_call(prompt, system="你是一位材料科学领域的学术写作专家。", temperature=0.7)


def generate_method_comparison(papers: list[dict]) -> str:
    """用 LLM 生成方法对比部分。"""
    paper_text = "\n".join(
        f"- {p['title']}({p['year']}): {p['finding']}" for p in papers
    )
    prompt = (
        f"根据以下论文发现，写一段方法对比分析（200 字左右）：\n{paper_text}\n"
        f"要求：对比不同方法的优劣、适用条件。"
    )
    return llm_call(prompt, system="你是一位材料科学领域的学术写作专家。", temperature=0.7)


def generate_gap_analysis(gaps: list[dict]) -> str:
    """用 LLM 生成 Gap 分析部分。"""
    gap_text = "\n".join(
        f"- [{g['type']}] {g['title']}: {g['description']}" for g in gaps
    )
    prompt = (
        f"根据以下 Research Gap 清单，写一段分析（300 字左右）：\n{gap_text}\n"
        f"要求：分析每个 gap 的成因、影响和研究价值。"
    )
    return llm_call(prompt, system="你是一位材料科学领域的学术写作专家。", temperature=0.7)


def generate_outlook(gaps: list[dict]) -> str:
    """用 LLM 生成展望部分。"""
    gap_titles = "\n".join(f"- {g['title']}" for g in gaps)
    prompt = (
        f"针对以下 Research Gap，写一段未来研究展望（200 字左右）：\n{gap_titles}\n"
        f"要求：提出具体可行的研究方向和建议。"
    )
    return llm_call(prompt, system="你是一位材料科学领域的学术写作专家。", temperature=0.7)


def generate_references(papers: list[dict]) -> str:
    """生成参考文献列表。"""
    lines = []
    for i, p in enumerate(papers, 1):
        lines.append(f"[{i}] {p['title']}, {p['year']}. {p['finding']}.")
    return "\n".join(lines)


def main():
    topic = "锂电池正极材料低温性能研究进展"

    print("=" * 55)
    print("  自动生成综述报告")
    print("=" * 55)
    print(f"\n主题: {topic}")
    print(f"输入: {len(PAPER_SUMMARIES)} 篇论文, {len(GAP_LIST)} 个 Gap\n")

    # 逐章节生成
    print("正在生成各章节...")
    sections = {
        "title": topic,
        "introduction": generate_introduction(topic),
        "method_comparison": generate_method_comparison(PAPER_SUMMARIES),
        "gap_analysis": generate_gap_analysis(GAP_LIST),
        "outlook": generate_outlook(GAP_LIST),
        "references": generate_references(PAPER_SUMMARIES),
    }

    # 填充模板
    report = REPORT_TEMPLATE.format(**sections)

    # 输出报告
    print("\n" + "=" * 55)
    print("  生成的综述报告")
    print("=" * 55)
    print(report)

    # 保存报告
    report_path = "review_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n报告已保存至: {report_path}")


if __name__ == "__main__":
    main()
