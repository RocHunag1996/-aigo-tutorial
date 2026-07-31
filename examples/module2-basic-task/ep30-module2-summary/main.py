"""
AIGO 教程系列 - 基本任务·文献调研 Agent
ep30-module2-summary: 模块二总结

演示完整 pipeline 的运行，对照能力自检要点逐项检查。
打印检查清单。
"""

import json
import sys
from pathlib import Path

# 导入共享模块
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
# ── 模块二各期回顾 ────────────────────────────────────────────

MODULE2_EPISODES = [
    {"ep": 9,  "title": "PDF 解析的挑战",           "skill": "理解 PDF 解析的难点"},
    {"ep": 10, "title": "MinerU 精准 API 实战",      "skill": "使用 MinerU API 解析 PDF"},
    {"ep": 11, "title": "MinerU 批量解析",            "skill": "批量处理多篇论文"},
    {"ep": 12, "title": "解析质量评估",               "skill": "评估解析结果的质量"},
    {"ep": 13, "title": "替代解析方案",               "skill": "了解多种 PDF 解析工具"},
    {"ep": 14, "title": "Sciverse 简介",              "skill": "了解 Sciverse 文献检索平台"},
    {"ep": 15, "title": "Sciverse API 实战",          "skill": "调用 Sciverse API 检索论文"},
    {"ep": 16, "title": "语义检索 vs 关键词检索",     "skill": "理解两种检索策略的差异"},
    {"ep": 17, "title": "高级检索策略",               "skill": "组合过滤、排序、分页"},
    {"ep": 18, "title": "构建检索 Agent",             "skill": "实现自动化文献检索"},
    {"ep": 19, "title": "知识抽取任务定义",           "skill": "定义结构化抽取 Schema"},
    {"ep": 20, "title": "用 LLM 做信息抽取",         "skill": "LLM 驱动的结构化抽取"},
    {"ep": 21, "title": "表格与数据精准抽取",         "skill": "表格识别与单位归一化"},
    {"ep": 22, "title": "实体对齐与消歧",             "skill": "材料名称标准化"},
    {"ep": 23, "title": "构建知识库",                 "skill": "SQLite 存储与多维查询"},
    {"ep": 24, "title": "Research Gap 五种类型",      "skill": "理解并分类 Research Gap"},
    {"ep": 25, "title": "用 LLM 辅助识别 Gap",       "skill": "LLM 驱动的 Gap 发现"},
    {"ep": 26, "title": "基于知识库的自动化 Gap 发现","skill": "统计方法发现覆盖盲区"},
    {"ep": 27, "title": "Gap 的新颖性与可操作性评估", "skill": "交叉验证 Gap 价值"},
    {"ep": 28, "title": "报告生成 Agent",             "skill": "LLM 生成结构化综述"},
    {"ep": 29, "title": "系统整合",                   "skill": "端到端 pipeline 串联"},
    {"ep": 30, "title": "模块二总结",                 "skill": "回顾与检查清单"},
]

# ── 能力自检要点检查清单 ──────────────────────────────────────

CHECKLIST = [
    {
        "item": "文献检索能力",
        "description": "能否通过 Sciverse API 检索相关论文",
        "episodes": [14, 15, 16, 17, 18],
        "status": "done",
    },
    {
        "item": "PDF 解析能力",
        "description": "能否用 MinerU 解析论文 PDF 并提取全文",
        "episodes": [9, 10, 11, 12, 13],
        "status": "done",
    },
    {
        "item": "结构化信息抽取",
        "description": "能否从论文中抽取材料、性能、方法等结构化数据",
        "episodes": [19, 20, 21, 22],
        "status": "done",
    },
    {
        "item": "知识库构建",
        "description": "能否将抽取结果存入数据库并支持多维查询",
        "episodes": [23],
        "status": "done",
    },
    {
        "item": "Research Gap 发现",
        "description": "能否自动发现缺失数据、矛盾结论等 Gap",
        "episodes": [24, 25, 26],
        "status": "done",
    },
    {
        "item": "Gap 评估与验证",
        "description": "能否评估 Gap 的新颖性和可操作性",
        "episodes": [27],
        "status": "done",
    },
    {
        "item": "报告生成",
        "description": "能否自动生成结构化综述报告",
        "episodes": [28],
        "status": "done",
    },
    {
        "item": "端到端 Pipeline",
        "description": "能否串联所有模块实现完整流程",
        "episodes": [29],
        "status": "done",
    },
]


def print_module_overview():
    """打印模块二各期内容概览。"""
    print("=" * 60)
    print("  模块二：基本任务 · 文献调研 Agent — 课程回顾")
    print("=" * 60)

    for ep in MODULE2_EPISODES:
        print(f"  ep{ep['ep']:>2} | {ep['title']:<25} | {ep['skill']}")


def print_checklist():
    """打印能力自检要点检查清单。"""
    print("\n\n" + "=" * 60)
    print("  能力自检要点 — 检查清单")
    print("=" * 60)

    done_count = 0
    for item in CHECKLIST:
        status_icon = "[v]" if item["status"] == "done" else "[ ]"
        eps = ", ".join(f"ep{e}" for e in item["episodes"])
        print(f"\n  {status_icon} {item['item']}")
        print(f"      {item['description']}")
        print(f"      相关期数: {eps}")
        if item["status"] == "done":
            done_count += 1

    total = len(CHECKLIST)
    print(f"\n{'─' * 60}")
    print(f"  完成进度: {done_count}/{total}")
    if done_count == total:
        print("  恭喜！模块二所有评估要点已覆盖。")


def print_pipeline_flow():
    """打印完整 pipeline 流程图。"""
    print("\n\n" + "=" * 60)
    print("  完整 Pipeline 流程")
    print("=" * 60)

    steps = [
        ("ep14-18", "文献检索",   "Sciverse 关键词/语义检索 → 获取论文列表"),
        ("ep9-13",  "PDF 解析",   "MinerU API 解析 PDF → 提取全文 Markdown"),
        ("ep19-20", "信息抽取",   "LLM 结构化抽取 → 材料/性能/方法"),
        ("ep21-22", "数据清洗",   "表格抽取 + 单位归一化 + 实体对齐"),
        ("ep23",    "知识库",     "SQLite 存储 → 多维查询"),
        ("ep24-26", "Gap 发现",  "规则 + LLM → 自动发现 Research Gap"),
        ("ep27",    "Gap 评估",   "Sciverse 交叉验证 → 新颖性评分"),
        ("ep28",    "报告生成",   "LLM 生成结构化综述报告"),
        ("ep29",    "系统整合",   "LiteratureAgent 端到端串联"),
    ]

    for i, (eps, name, desc) in enumerate(steps, 1):
        print(f"\n  步骤 {i}: {name} ({eps})")
        print(f"    {desc}")
        if i < len(steps):
            print(f"    ↓")


def main():
    # 1. 课程回顾
    print_module_overview()

    # 2. 检查清单
    print_checklist()

    # 3. Pipeline 流程
    print_pipeline_flow()

    print("\n\n" + "=" * 60)
    print("  模块二完成！接下来进入模块三：高级任务。")
    print("=" * 60)


if __name__ == "__main__":
    main()
