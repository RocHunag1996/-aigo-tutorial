"""
AIGO 教程系列 - 路线 C·合成路线与工艺设计
ep55-route-c-overview: 路线 C 总览
"""

import os


def print_roadmap():
    """打印路线 C 学习路线图"""
    roadmap = """
╔══════════════════════════════════════════════════════════════╗
║           路线 C: 合成路线与工艺设计 (Module 5)              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ep55  路线C总览 ──────────── 本文件，概览与文件索引          ║
║   │                                                          ║
║   ▼                                                          ║
║  ep56  合成文献挖掘 ──────── LLM 提取合成条件               ║
║   │                                                          ║
║   ▼                                                          ║
║  ep57  合成知识库 ────────── SQLite 存储与查询               ║
║   │                                                          ║
║   ▼                                                          ║
║  ep58  逆向合成分析 ──────── LLM 驱动逆合成推理              ║
║   │                                                          ║
║   ▼                                                          ║
║  ep59  路线生成 Agent ────── 多步合成路线自动规划            ║
║   │                                                          ║
║   ▼                                                          ║
║  ep60  工艺优化 ──────────── 贝叶斯优化合成参数              ║
║   │                                                          ║
║   ▼                                                          ║
║  ep61  推理可视化 ────────── 决策流程 ASCII 可视化           ║
║   │                                                          ║
║   ▼                                                          ║
║  ep62  合成验证 ──────────── 三级验证策略                    ║
║   │                                                          ║
║   ▼                                                          ║
║  ep63  评分标准拆解 ──────── 路线C评分维度详解               ║
║   │                                                          ║
║   ▼                                                          ║
║  ep64  模块五总结 ────────── 回顾与展望                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(roadmap)


def print_file_index():
    """打印文件索引与各期核心内容"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(base_dir)

    print("=" * 60)
    print("路线 C 文件索引")
    print("=" * 60)

    episodes = [
        ("ep55-route-c-overview", "路线 C 总览与学习路线图"),
        ("ep56-synthesis-mining", "LLM 从论文中提取合成条件"),
        ("ep57-synthesis-kb", "SQLite 合成知识库构建与查询"),
        ("ep58-retrosynthesis", "LLM 驱动逆向合成分析"),
        ("ep59-route-generator", "多步合成路线生成 Agent"),
        ("ep60-process-optimization", "贝叶斯优化合成工艺参数"),
        ("ep61-visualization", "合成决策流程 ASCII 可视化"),
        ("ep62-validation", "计算/文献/实验三级验证"),
        ("ep63-route-c-scoring", "路线 C 评分标准拆解"),
        ("ep64-module5-summary", "模块五总结与竞赛提交建议"),
    ]

    for i, (folder, desc) in enumerate(episodes, 1):
        path = os.path.join(parent_dir, folder, "main.py")
        exists = "✓" if os.path.exists(path) else "✗"
        print(f"  [{exists}] {folder:30s} | {desc}")

    print()
    print("核心思路：")
    print("  文献 → 提取合成条件 → 构建知识库 → 逆合成推理")
    print("  → 路线生成 → 工艺优化 → 验证 → 评分")
    print()
    print("与路线 A/B 的区别：")
    print("  路线 A 关注 '发现什么材料'，路线 B 关注 '如何模拟'，")
    print("  路线 C 关注 '如何把材料做出来' —— 从论文到实验台。")


def print_key_concepts():
    """打印路线 C 核心概念"""
    concepts = {
        "合成条件挖掘": "从论文文本中用 LLM 提取温度、时间、前驱体等参数",
        "知识库": "结构化存储合成条件，支持按材料体系/方法检索",
        "逆向合成": "从目标产物出发，递归拆解为可用前驱体",
        "路线生成": "Agent 结合知识库与 LLM 推理，规划多步合成路线",
        "工艺优化": "贝叶斯优化处理高成本黑箱实验参数调优",
        "三级验证": "计算验证(热力学) → 文献验证(相似体系) → 实验验证",
    }

    print("=" * 60)
    print("路线 C 核心概念速览")
    print("=" * 60)
    for name, desc in concepts.items():
        print(f"\n  [{name}]")
        print(f"    {desc}")


def main():
    print_roadmap()
    print_file_index()
    print_key_concepts()

    print("\n" + "=" * 60)
    print("开始路线 C 学习之旅！")
    print("下一步：ep56 - 用 LLM 从论文中挖掘合成条件")
    print("=" * 60)


if __name__ == "__main__":
    main()
