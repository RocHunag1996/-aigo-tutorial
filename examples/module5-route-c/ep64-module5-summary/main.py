"""
AIGO 教程系列 - 路线 C·合成路线与工艺设计
ep64-module5-summary: 模块五总结
回顾路线 C 全流程，总结关键技能与项目化交付建议
"""

import os


def print_pipeline_summary():
    """打印路线 C 全流程回顾"""
    print("=" * 60)
    print("路线 C 全流程回顾")
    print("=" * 60)

    pipeline = """
    ┌─────────────────────────────────────────────────────────┐
    │                    路线 C 完整流程                       │
    ├─────────────────────────────────────────────────────────┤
    │                                                         │
    │  ep56 文献挖掘 ──▶ ep57 知识库构建                      │
    │       │                    │                            │
    │       ▼                    ▼                            │
    │  ep58 逆向合成 ◀── 知识库支撑                           │
    │       │                                                 │
    │       ▼                                                 │
    │  ep59 路线生成 Agent                                    │
    │       │                                                 │
    │       ├──▶ ep60 工艺优化（贝叶斯）                      │
    │       │                                                 │
    │       └──▶ ep61 推理可视化                              │
    │                                                         │
    │  ep62 三级验证（计算 → 文献 → 实验）                    │
    │       │                                                 │
    │       ▼                                                 │
    │  ep63 质量清单拆解 ──▶ 针对性优化                       │
    │                                                         │
    └─────────────────────────────────────────────────────────┘
    """
    print(pipeline)


def print_key_skills():
    """打印本模块培养的核心技能"""
    skills = {
        "LLM 信息提取": {
            "desc": "从非结构化文本中提取结构化合成条件",
            "files": ["ep56", "ep58"],
            "value": "体现 LLM 在材料科学中的 NLP 应用"
        },
        "知识库工程": {
            "desc": "设计数据库结构，支持高效检索与交叉引用",
            "files": ["ep57"],
            "value": "展示系统性数据管理能力"
        },
        "Agent 设计": {
            "desc": "构建多步骤推理的合成路线生成 Agent",
            "files": ["ep59"],
            "value": "核心亮点：自主规划能力"
        },
        "贝叶斯优化": {
            "desc": "用代理模型优化高成本实验参数",
            "files": ["ep60"],
            "value": "展示算法思维与工程优化能力"
        },
        "科学验证": {
            "desc": "三级递进验证策略，不盲目信任 AI 输出",
            "files": ["ep62"],
            "value": "体现科学素养与批判性思维"
        },
    }

    print("\n核心技能矩阵")
    print("=" * 60)
    for name, info in skills.items():
        print(f"\n  [{name}]")
        print(f"    描述: {info['desc']}")
        print(f"    对应期数: {', '.join(info['files'])}")
        print(f"    实用价值: {info['value']}")


def print_common_pitfalls():
    """打印常见陷阱"""
    print("\n常见陷阱与规避")
    print("=" * 60)

    pitfalls = [
        {
            "trap": "LLM 幻觉合成条件",
            "risk": "LLM 可能编造不存在的反应条件",
            "fix": "必须与知识库/文献交叉验证，标注置信度"
        },
        {
            "trap": "忽略安全约束",
            "risk": "生成的路线可能涉及危险操作",
            "fix": "加入安全检查模块，排除易燃易爆前驱体组合"
        },
        {
            "trap": "过度优化单一指标",
            "risk": "只优化产率，忽略成本/可重复性/安全性",
            "fix": "多目标优化，加权综合评分"
        },
        {
            "trap": "知识库覆盖不足",
            "risk": "只收集了几条记录就声称构建了知识库",
            "fix": "至少 50+ 条记录，覆盖 3+ 个材料体系"
        },
        {
            "trap": "验证流于形式",
            "risk": "三级验证只做了计算验证就声称完成",
            "fix": "每级验证都需实际执行，给出具体证据"
        },
    ]

    for i, p in enumerate(pitfalls, 1):
        print(f"\n  陷阱 {i}: {p['trap']}")
        print(f"    风险: {p['risk']}")
        print(f"    规避: {p['fix']}")


def print_submission_checklist():
    """打印项目质量自检清单"""
    print("\n项目质量自检清单")
    print("=" * 60)

    checklist = [
        "代码可运行（python main.py 无报错）",
        "合成路线有化学依据（非 LLM 臆想）",
        "知识库包含 50+ 条合成记录",
        "至少对比 3 条合成路线",
        "工艺优化有收敛曲线",
        "三级验证全部执行",
        "可视化图表至少 3 种",
        "README 说明运行环境与依赖",
        "结果可复现（固定随机种子）",
        "代码有中文注释",
    ]

    for i, item in enumerate(checklist, 1):
        print(f"  [ ] {i:2d}. {item}")

    print(f"\n  共 {len(checklist)} 项，建议逐项检查后再发布/交付。")


def print_farewell():
    """打印结课寄语"""
    print("\n" + "=" * 60)
    print("模块五完成！路线 C 学习之旅结束。")
    print("=" * 60)
    print("""
    回顾整个 AIGO 教程系列：

    模块一/二 (ep01-30): 基础任务 —— 文献调研 Agent
      - LLM 调用、文献搜索、信息提取、报告生成

    模块三 (ep31-44): 路线 A —— 构效关系发现
      - 数据库查询、特征工程、搜索算法、证据链

    模块四 (ep45-54): 路线 B —— 模拟方法创新
      - DFT、机器学习势、蒙特卡洛、分子动力学

    模块五 (ep55-64): 路线 C —— 合成路线设计
      - 文献挖掘、知识库、逆合成、工艺优化、验证

    三条路线覆盖了材料科学研究的完整链条：
    发现 → 理解 → 模拟 → 合成

    愿你把它接上真实数据、用到自己的研究里，做出属于你的东西！
    """)


def main():
    print("ep64 - 模块五总结")
    print("=" * 60)

    print_pipeline_summary()
    print_key_skills()
    print_common_pitfalls()
    print_submission_checklist()
    print_farewell()


if __name__ == "__main__":
    main()
