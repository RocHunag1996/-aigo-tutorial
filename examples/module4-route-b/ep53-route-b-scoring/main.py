"""
AIGO 教程系列 - 路线 B·模拟方法创新
ep53-route-b-scoring: 评分标准拆解

打印评分维度，逐项说明代码对应关系。
"""


def print_scoring_dimensions():
    """打印路线 B 评分维度。"""
    dimensions = [
        {
            "name": "模拟方法理解",
            "weight": "20%",
            "criteria": [
                "DFT 基本原理的准确描述",
                "MC/MD 方法的正确实现",
                "物理模型的合理性",
            ],
            "code_mapping": [
                "ep46: 一维 KS 方程 SCF 循环",
                "ep50: 2D Ising Metropolis MC",
                "ep51: LJ 势 Verlet MD",
            ],
        },
        {
            "name": "ML 势函数应用",
            "weight": "25%",
            "criteria": [
                "MLP 选型合理性",
                "数据准备规范性",
                "训练配置的完整性",
            ],
            "code_mapping": [
                "ep47: MACE/NequIP/CHGNet 对比",
                "ep48: MACE 数据准备与配置",
                "ep49: MD17 Benchmark 评估",
            ],
        },
        {
            "name": "模拟创新与加速",
            "weight": "25%",
            "criteria": [
                "ML 加速模拟的创新思路",
                "计算效率的提升",
                "方法的可扩展性",
            ],
            "code_mapping": [
                "ep50: MC 加速思路（向量化/Wolff/ML）",
                "ep51: ML-MD 耦合架构",
                "ep52: 生成式模型替代模拟",
            ],
        },
        {
            "name": "Benchmark 与验证",
            "weight": "15%",
            "criteria": [
                "评估指标的正确使用",
                "对比实验的完整性",
                "误差分析的深入性",
            ],
            "code_mapping": [
                "ep49: MAE/RMSE 评估",
                "ep51: 能量守恒检查",
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
    """打印单个评分维度的详情。"""
    print(f"\n{'='*60}")
    print(f"  {dim['name']}（权重: {dim['weight']}）")
    print(f"{'='*60}")

    print(f"\n  评分标准:")
    for i, c in enumerate(dim["criteria"], 1):
        print(f"  {i}. {c}")

    print(f"\n  对应代码:")
    for c in dim["code_mapping"]:
        print(f"  -> {c}")


def main():
    print("=" * 60)
    print("  ep53 - 路线 B 评分标准拆解")
    print("=" * 60)

    dimensions = print_scoring_dimensions()
    for dim in dimensions:
        print_dimension_detail(dim)

    print(f"\n\n  评分权重可视化：")
    weights = [("模拟理解", 20), ("ML势函数", 25), ("模拟创新", 25),
               ("Benchmark", 15), ("代码质量", 15)]
    for name, w in weights:
        bar = "#" * (w // 2)
        print(f"  {name:<10s} {w:>3d}% {bar}")

    print(f"\n  路线 B 得分关键：")
    print("  1. 不仅要实现模拟方法，还要理解其物理基础")
    print("  2. ML 势函数部分要展示选型逻辑和数据准备能力")
    print("  3. 创新点在于'ML 如何加速/替代传统模拟'")
    print("  4. Benchmark 要严谨，指标计算要正确")


if __name__ == "__main__":
    main()
