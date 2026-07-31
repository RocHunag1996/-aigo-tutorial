"""
AIGO 教程系列 - 基本任务·文献调研 Agent
ep24-gap-types: Research Gap 五种类型

用示例数据演示五种 Gap 类型（缺失数据、矛盾结论、未探索区间、
方法空白、跨领域连接缺失）。每种类型给出材料科学的具体例子。
"""

import json

# ── 五种 Research Gap 类型定义 ─────────────────────────────────

GAP_TYPES = {
    "missing_data": {
        "name": "缺失数据型 Gap",
        "description": "某材料体系的某个关键性能指标尚无实验数据",
        "example": {
            "context": "LiFePO4 正极材料在低温（-20°C）下的倍率性能",
            "gap": "现有文献集中在 25°C 以上，-20°C 以下的数据几乎空白",
            "impact": "限制了 LFP 电池在极寒地区的应用",
        },
    },
    "contradiction": {
        "name": "矛盾结论型 Gap",
        "description": "不同研究团队对同一问题得出相互矛盾的结论",
        "example": {
            "context": "LLZO 固态电解质的晶界阻抗对总阻抗的贡献",
            "gap": "团队 A 认为晶界阻抗占总阻抗 70%；团队 B 发现仅占 10%",
            "impact": "无法确定优化方向是改善晶界还是体相",
        },
    },
    "unexplored_region": {
        "name": "未探索区间型 Gap",
        "description": "成分-性能空间中某些区域尚未被实验覆盖",
        "example": {
            "context": "NMC 三元材料中 Ni/Mn/Co 比例的系统研究",
            "gap": "高锰区域（Mn > 50%）的电化学性能数据稀缺",
            "impact": "可能遗漏低成本、高安全性的成分组合",
        },
    },
    "method_gap": {
        "name": "方法空白型 Gap",
        "description": "某类问题尚无合适的研究/表征方法",
        "example": {
            "context": "固态电池充放电过程中锂枝晶的原位观测",
            "gap": "现有 TEM/SEM 方法难以在工况下实时观测固态电解质中的枝晶生长",
            "impact": "无法理解枝晶形成机制，阻碍解决方案的开发",
        },
    },
    "cross_domain": {
        "name": "跨领域连接缺失型 Gap",
        "description": "两个相关领域之间缺乏知识迁移和方法借鉴",
        "example": {
            "context": "机器学习在催化剂设计中的应用 vs 热电材料优化",
            "gap": "ML 已成功预测催化剂活性位点，但很少用于热电材料的载流子浓度优化",
            "impact": "热电材料的组分优化仍依赖试错法，效率低下",
        },
    },
}


def print_gap_types():
    """打印五种 Gap 类型的详细说明和示例。"""
    print("=" * 60)
    print("  Research Gap 五种类型")
    print("=" * 60)

    for i, (key, gap) in enumerate(GAP_TYPES.items(), 1):
        print(f"\n{'─' * 60}")
        print(f"类型 {i}: {gap['name']}")
        print(f"{'─' * 60}")
        print(f"  定义: {gap['description']}")
        ex = gap["example"]
        print(f"  背景: {ex['context']}")
        print(f"  Gap:  {ex['gap']}")
        print(f"  影响: {ex['impact']}")


def show_gap_comparison():
    """以表格形式对比五种 Gap 类型。"""
    print("\n\n" + "=" * 60)
    print("  Gap 类型对比表")
    print("=" * 60)
    header = f"{'类型':<8} {'名称':<20} {'核心特征'}"
    print(f"\n{header}")
    print("-" * 60)

    features = {
        "missing_data":     "有材料、缺数据",
        "contradiction":    "有数据、但矛盾",
        "unexplored_region": "有框架、缺覆盖",
        "method_gap":       "有问题、缺工具",
        "cross_domain":     "有方法、缺迁移",
    }
    for i, (key, gap) in enumerate(GAP_TYPES.items(), 1):
        print(f"  {i:<6} {gap['name']:<20} {features[key]}")


def main():
    # 1. 详细展示每种 Gap 类型
    print_gap_types()

    # 2. 对比表格
    show_gap_comparison()

    # 3. 导出 Gap 类型定义
    gap_path = "gap_types.json"
    with open(gap_path, "w", encoding="utf-8") as f:
        json.dump(GAP_TYPES, f, ensure_ascii=False, indent=2)
    print(f"\n\nGap 类型定义已导出至: {gap_path}")


if __name__ == "__main__":
    main()
