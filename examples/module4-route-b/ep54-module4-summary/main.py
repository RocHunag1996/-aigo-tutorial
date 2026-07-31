"""
AIGO 教程系列 - 路线 B·模拟方法创新
ep54-module4-summary: 模块四总结

汇总路线 B 的关键代码和常见翻车点。
"""


def print_pipeline_summary():
    """打印路线 B 完整 pipeline 总结。"""
    steps = [
        ("ep46", "DFT 基础",
         "一维 KS 方程 + SCF 自洽场循环",
         "numpy 矩阵对角化 + 有限差分"),
        ("ep47", "MLP 全景",
         "MACE/NequIP/CHGNet/M3GNet 对比",
         "架构分析 + 选型指南"),
        ("ep48", "MACE 上手",
         "数据准备(extxyz) + 训练配置",
         "ASE 数据结构 + YAML 配置"),
        ("ep49", "Benchmark",
         "MD17 数据集下载 + MAE/RMSE 评估",
         "requests 下载 + numpy 指标计算"),
        ("ep50", "蒙特卡洛",
         "2D Ising 模型 + Metropolis 算法",
         "numpy 随机 + 周期性边界"),
        ("ep51", "分子动力学",
         "LJ 势 + Velocity Verlet 积分",
         "力计算 + 能量守恒验证"),
        ("ep52", "生成模型",
         "VAE 思路生成材料特征",
         "编码器-解码器 + 潜空间采样"),
    ]

    print("\n  路线 B Pipeline 总结：")
    print("=" * 70)
    for ep, name, desc, tech in steps:
        print(f"\n  [{ep}] {name}")
        print(f"    内容: {desc}")
        print(f"    技术: {tech}")
    print("\n" + "=" * 70)


def print_common_pitfalls():
    """打印常见翻车点。"""
    pitfalls = [
        {
            "title": "SCF 不收敛",
            "symptom": "能量振荡或发散",
            "cause": "混合参数太大或初始猜测太差",
            "fix": "减小混合系数 alpha，增加网格密度",
        },
        {
            "title": "MC 模拟临界慢化",
            "symptom": "接近 Tc 时关联时间极长",
            "cause": "单自旋翻转在临界点效率极低",
            "fix": "使用 Wolff 簇翻转算法",
        },
        {
            "title": "MD 能量不守恒",
            "symptom": "总能量持续上升或下降",
            "cause": "步长 dt 太大或截断半径处理不当",
            "fix": "减小 dt，检查长程力修正",
        },
        {
            "title": "MACE 训练数据不足",
            "symptom": "模型在测试集上误差大",
            "cause": "训练构型不够多样或 DFT 精度不够",
            "fix": "增加 MD 采样构型，使用高精度 DFT 设置",
        },
        {
            "title": "Benchmark 数据泄漏",
            "symptom": "测试误差异常低",
            "cause": "训练集和测试集包含相同/相似构型",
            "fix": "按分子/温度严格划分数据集",
        },
    ]

    print("\n  常见翻车点：")
    print("=" * 65)
    for i, p in enumerate(pitfalls, 1):
        print(f"\n  {i}. {p['title']}")
        print(f"     症状: {p['symptom']}")
        print(f"     原因: {p['cause']}")
        print(f"     修复: {p['fix']}")
    print("\n" + "=" * 65)


def main():
    print("=" * 65)
    print("  ep54 - 模块四总结：路线 B 关键代码与常见翻车点")
    print("=" * 65)

    print_pipeline_summary()
    print_common_pitfalls()

    print("\n  核心收获：")
    takeaways = [
        "DFT 是'第一性原理'的基石，ML 势函数是其高效替代",
        "MC 和 MD 是两种互补的统计力学模拟方法",
        "Benchmark 是检验 ML 方法的金标准",
        "生成式模型是未来方向，但目前还不能完全替代物理模拟",
        "路线 B 的核心竞争力：理解物理 + 掌握 ML + 工程实现",
    ]
    for i, t in enumerate(takeaways, 1):
        print(f"  {i}. {t}")

    print("\n  模块四学习完成！")
    print("  下一步: 进入模块五 - 路线 C - 合成路线与工艺设计")


if __name__ == "__main__":
    main()
