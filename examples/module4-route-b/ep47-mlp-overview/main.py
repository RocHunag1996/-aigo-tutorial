"""
AIGO 教程系列 - 路线 B·模拟方法创新
ep47-mlp-overview: 机器学习势函数全景

对比 MACE/NequIP/CHGNet 的特点（打印对比表格）。
不实际训练，侧重理解和选型。
"""


def print_mlp_landscape():
    """打印机器学习势函数全景概览。"""
    print("\n  机器学习势函数（MLP）发展脉络：")
    print("  " + "-" * 60)
    print("""
    传统经验势        机器学习势函数             第一性原理
    (LJ, EAM, ...)    (MACE, NequIP, ...)       (DFT, CCSD(T))
       |                    |                       |
    快但不准           <-- 精度逼近 DFT           准但很慢
    参数少             <-- 自动学习               无参数拟合
    体系特异性         <-- 通用预训练模型          精确基准
  """)


def print_comparison_table():
    """打印主流 MLP 对比表格。"""
    models = [
        {
            "name": "MACE",
            "year": 2022,
            "arch": "等变消息传递 + 多体展开",
            "features": "原子类型, 坐标, 晶格",
            "accuracy": "~1 meV/atom (MD17)",
            "speed": "~1000x faster than DFT",
            "pretrained": "Foundation 模型 (MACE-MP)",
            "pros": "精度高, 预训练模型可用, 社区活跃",
            "cons": "训练数据要求高, GPU 必需",
        },
        {
            "name": "NequIP",
            "year": 2022,
            "arch": "等变图神经网络 (E(3)-equivariant)",
            "features": "原子类型, 坐标",
            "accuracy": "~1 meV/atom (小分子)",
            "speed": "~500x faster than DFT",
            "pretrained": "无通用预训练",
            "pros": "理论基础扎实, 等变性好",
            "cons": "已被 MACE 超越, 社区缩小",
        },
        {
            "name": "CHGNet",
            "year": 2023,
            "arch": "图网络 + 电荷信息",
            "features": "原子类型, 坐标, 磁矩",
            "accuracy": "~5 meV/atom (Materials Project)",
            "speed": "~500x faster than DFT",
            "pretrained": "MP 数据集预训练",
            "pros": "覆盖全 MP 数据, 含电荷/磁矩",
            "cons": "精度略低于 MACE",
        },
        {
            "name": "M3GNet",
            "year": 2022,
            "arch": "方向性消息传递网络",
            "features": "原子类型, 坐标, 键角",
            "accuracy": "~10 meV/atom",
            "speed": "~200x faster than DFT",
            "pretrained": "MP 数据集预训练",
            "pros": "集成在 pymatgen 生态",
            "cons": "精度和速度均非最优",
        },
    ]

    print("\n  主流机器学习势函数对比：")
    print("=" * 70)
    print(f"  {'模型':<10s} {'年份':<6s} {'精度':<20s} {'速度':<20s}")
    print("-" * 70)
    for m in models:
        print(f"  {m['name']:<10s} {m['year']:<6d} {m['accuracy']:<20s} {m['speed']:<20s}")
    print("-" * 70)

    # 详细对比
    print("\n  详细特性对比：")
    for m in models:
        print(f"\n  [{m['name']}] ({m['year']})")
        print(f"    架构: {m['arch']}")
        print(f"    输入: {m['features']}")
        print(f"    预训练: {m['pretrained']}")
        print(f"    优势: {m['pros']}")
        print(f"    局限: {m['cons']}")


def print_selection_guide():
    """打印选型建议。"""
    print("\n\n  MLP 选型建议：")
    print("=" * 60)

    scenarios = [
        ("快速原型验证", "M3GNet / CHGNet", "用预训练模型，几行代码即可开始"),
        ("高精度材料模拟", "MACE-MP", "Foundation 模型 + 微调，精度最优"),
        ("等变性要求严格", "MACE / NequIP", "物理对称性保证，泛化性好"),
        ("需要电荷/磁矩", "CHGNet", "唯一内置电荷和磁矩预测的模型"),
        ("资源有限（CPU）", "M3GNet", "对硬件要求最低"),
    ]

    for i, (scenario, model, reason) in enumerate(scenarios, 1):
        print(f"\n  {i}. 场景: {scenario}")
        print(f"     推荐: {model}")
        print(f"     原因: {reason}")


def main():
    print("=" * 70)
    print("  ep47 - 机器学习势函数全景")
    print("=" * 70)

    print_mlp_landscape()
    print_comparison_table()
    print_selection_guide()

    print(f"\n\n  趋势总结：")
    print("  - MLP 正在从'训练特定体系'走向'通用 Foundation 模型'")
    print("  - MACE-MP 是当前最通用的预训练势函数")
    print("  - 等变性（Equivariance）是核心设计原则")
    print("  - 下一期 ep48 将演示 MACE 的数据准备和训练配置")


if __name__ == "__main__":
    main()
