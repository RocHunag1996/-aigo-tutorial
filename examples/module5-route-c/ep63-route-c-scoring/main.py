"""
AIGO 教程系列 - 路线 C·合成路线与工艺设计
ep63-route-c-scoring: 路线 C 评分标准拆解
详细解析竞赛路线 C 的各评分维度与得分策略
"""


def print_scoring_overview():
    """打印评分维度总览"""
    print("=" * 60)
    print("路线 C 评分维度总览")
    print("=" * 60)

    dimensions = [
        {
            "name": "合成路线合理性",
            "weight": 0.25,
            "criteria": [
                "路线是否有化学依据（非臆想）",
                "前驱体选择是否合理（商业可得）",
                "反应条件是否在安全范围内",
                "是否考虑了副产物与产率",
            ],
            "code_ref": "ep58-retrosynthesis, ep59-route-generator"
        },
        {
            "name": "知识库完整性",
            "weight": 0.20,
            "criteria": [
                "从文献中提取了多少条合成记录",
                "记录字段是否完整（温度/时间/前驱体等）",
                "是否覆盖目标材料体系",
                "知识库查询功能是否正常",
            ],
            "code_ref": "ep56-synthesis-mining, ep57-synthesis-kb"
        },
        {
            "name": "工艺优化效果",
            "weight": 0.20,
            "criteria": [
                "优化算法是否合理（贝叶斯/遗传算法等）",
                "优化迭代次数是否高效",
                "最终参数是否优于文献报道",
                "是否有收敛曲线展示",
            ],
            "code_ref": "ep60-process-optimization"
        },
        {
            "name": "验证充分性",
            "weight": 0.20,
            "criteria": [
                "是否完成三级验证（计算/文献/实验）",
                "计算验证是否包含热力学分析",
                "文献验证是否找到支撑证据",
                "实验验证方案是否完整",
            ],
            "code_ref": "ep62-validation"
        },
        {
            "name": "可视化与可解释性",
            "weight": 0.15,
            "criteria": [
                "决策流程是否可视化",
                "路线对比是否清晰",
                "参数空间是否展示",
                "推理过程是否可追溯",
            ],
            "code_ref": "ep61-visualization"
        },
    ]

    for dim in dimensions:
        print(f"\n  [{dim['name']}] 权重: {dim['weight']:.0%}")
        print(f"  对应代码: {dim['code_ref']}")
        print("  评分要点:")
        for c in dim["criteria"]:
            print(f"    - {c}")

    return dimensions


def print_scoring_strategy():
    """打印得分策略建议"""
    print("\n" + "=" * 60)
    print("高分策略建议")
    print("=" * 60)

    strategies = [
        {
            "tip": "多路线对比",
            "desc": "不要只给一条路线，至少生成 3 条并对比评分",
            "impact": "合成路线合理性 +15%"
        },
        {
            "tip": "知识库规模",
            "desc": "至少挖掘 50+ 条合成记录，覆盖 3+ 个材料体系",
            "impact": "知识库完整性 +20%"
        },
        {
            "tip": "优化收敛曲线",
            "desc": "展示贝叶斯优化的收敛过程，体现算法效率",
            "impact": "工艺优化效果 +10%"
        },
        {
            "tip": "三级验证全覆盖",
            "desc": "计算验证用 MP API，文献验证用 Sciverse，实验方案详细",
            "impact": "验证充分性 +25%"
        },
        {
            "tip": "完整可视化",
            "desc": "决策流程图 + 路线对比图 + 参数空间热力图",
            "impact": "可视化 +15%"
        },
    ]

    for i, s in enumerate(strategies, 1):
        print(f"\n  {i}. {s['tip']}")
        print(f"     做法: {s['desc']}")
        print(f"     预期提升: {s['impact']}")


def calculate_demo_score():
    """演示评分计算"""
    print("\n" + "=" * 60)
    print("演示评分计算")
    print("=" * 60)

    scores = {
        "合成路线合理性": 82,
        "知识库完整性": 75,
        "工艺优化效果": 88,
        "验证充分性": 70,
        "可视化与可解释性": 90,
    }

    weights = {
        "合成路线合理性": 0.25,
        "知识库完整性": 0.20,
        "工艺优化效果": 0.20,
        "验证充分性": 0.20,
        "可视化与可解释性": 0.15,
    }

    total = 0
    print(f"\n{'维度':20s} | {'得分':>4s} | {'权重':>4s} | {'加权':>6s}")
    print("-" * 50)
    for dim, score in scores.items():
        w = weights[dim]
        weighted = score * w
        total += weighted
        bar = "█" * (score // 5)
        print(f"  {dim:18s} | {score:4d} | {w:.0%} | {weighted:6.1f} {bar}")

    print("-" * 50)
    print(f"  {'总分':18s} |      |      | {total:6.1f}/100")

    # 评级
    if total >= 90:
        grade = "A (优秀)"
    elif total >= 80:
        grade = "B (良好)"
    elif total >= 70:
        grade = "C (中等)"
    else:
        grade = "D (需改进)"
    print(f"\n  评级: {grade}")


def main():
    print("ep63 - 路线 C 评分标准拆解")
    print("=" * 60)

    print_scoring_overview()
    print_scoring_strategy()
    calculate_demo_score()

    print("\n" + "=" * 60)
    print("关键提醒：")
    print("""
    1. 路线 C 的核心是 "从论文到实验台" 的完整闭环
    2. 关键看：路线是否有化学依据（不是瞎编）
    3. 知识库是加分项：体现系统性数据挖掘能力
    4. 工艺优化展示算法思维：不是简单查文献抄条件
    5. 验证策略体现科学素养：不盲目相信 LLM 输出
    """)


if __name__ == "__main__":
    main()
