"""
AIGO 教程系列 - 路线 A·构效关系发现
ep43-route-a-scoring: 质量清单拆解

打印质量维度，逐项说明代码对应关系。
"""


def print_scoring_dimensions():
    """打印路线 A 质量维度。"""
    dimensions = [
        {
            "name": "数据采集与处理",
            "weight": "20%",
            "criteria": [
                "多源数据整合（MP + OQMD + 文献）",
                "数据清洗与去重",
                "特征工程质量",
            ],
            "code_mapping": [
                "ep32: Materials Project API 查询",
                "ep33: OQMD 数据库对接",
                "ep34: Magpie 特征工程",
            ],
        },
        {
            "name": "搜索与优化算法",
            "weight": "25%",
            "criteria": [
                "算法选择的合理性",
                "搜索效率与收敛性",
                "创新性与改进",
            ],
            "code_mapping": [
                "ep35: 遗传算法",
                "ep36: 贝叶斯优化",
                "ep37: 符号回归",
                "ep39: 搜索空间设计",
            ],
        },
        {
            "name": "LLM 融合能力",
            "weight": "20%",
            "criteria": [
                "LLM 生成候选的质量",
                "搜索结果评估的准确性",
                "闭环迭代的效果",
            ],
            "code_mapping": [
                "ep38: LLM + 搜索融合循环",
                "ep40: 文献证据链",
            ],
        },
        {
            "name": "可解释性与科学发现",
            "weight": "20%",
            "criteria": [
                "构效关系的物理解释",
                "特征重要性分析",
                "是否有新发现",
            ],
            "code_mapping": [
                "ep41: 特征重要性与物理解释",
                "ep42: 实战案例",
            ],
        },
        {
            "name": "代码质量与文档",
            "weight": "15%",
            "criteria": [
                "代码可读性与结构",
                "注释完整度",
                "可复现性",
            ],
            "code_mapping": [
                "所有 ep 文件: 统一代码风格",
                "中文注释 + 模块化设计",
            ],
        },
    ]
    return dimensions


def print_dimension_detail(dim):
    """打印单个质量维度的详情。"""
    print(f"\n{'='*60}")
    print(f"  {dim['name']}（权重: {dim['weight']}）")
    print(f"{'='*60}")

    print(f"\n  质量清单:")
    for i, c in enumerate(dim["criteria"], 1):
        print(f"  {i}. {c}")

    print(f"\n  对应代码:")
    for c in dim["code_mapping"]:
        print(f"  -> {c}")


def print_scoring_tips():
    """打印得分技巧。"""
    print(f"\n\n{'='*60}")
    print("  得分技巧")
    print(f"{'='*60}")

    tips = [
        ("数据多样性", "至少对接 2 个数据库，交叉验证提高可信度"),
        ("特征工程", "不要只做加权平均，加入方差/极差等统计量"),
        ("算法对比", "跑 GA + BO + SR 三种算法并对比效果"),
        ("LLM 闭环", "至少 3 轮迭代，展示搜索方向的演化过程"),
        ("物理解释", "不能只给数字，要解释 WHY（如电负性差异->声子散射）"),
        ("代码规范", "统一风格、中文注释、可直接运行"),
    ]

    for i, (title, tip) in enumerate(tips, 1):
        print(f"\n  {i}. {title}")
        print(f"     {tip}")


def main():
    print("=" * 60)
    print("  ep43 - 路线 A 质量清单拆解")
    print("=" * 60)

    dimensions = print_scoring_dimensions()

    for dim in dimensions:
        print_dimension_detail(dim)

    print_scoring_tips()

    print(f"\n\n  评分权重可视化：")
    weights = [("数据采集", 20), ("搜索优化", 25), ("LLM融合", 20),
               ("可解释性", 20), ("代码质量", 15)]
    for name, w in weights:
        bar = "#" * (w // 2)
        print(f"  {name:<10s} {w:>3d}% {bar}")


if __name__ == "__main__":
    main()
