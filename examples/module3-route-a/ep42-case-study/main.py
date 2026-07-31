"""
AIGO 教程系列 - 路线 A·构效关系发现
ep42-case-study: Heusler 合金热电体系实战案例

从头跑通完整 pipeline（简化版）：
数据采集 -> 特征工程 -> 搜索优化 -> 可解释性分析
"""
import numpy as np
import sys
from pathlib import Path
import os
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
# ── Step 1: 模拟数据采集 ────────────────────────────────────
def collect_data():
    """模拟 Heusler 合金（XYZ 型）数据集。"""
    x_elements = ["Ti", "Ni", "Co", "Fe", "Mn"]
    y_elements = ["Ni", "Co", "Fe", "Cu", "Mn"]
    z_elements = ["Sn", "Sb", "Bi", "Ge", "Si"]

    np.random.seed(42)
    data = []

    for _ in range(50):
        x = np.random.choice(x_elements)
        y = np.random.choice(y_elements)
        z = np.random.choice(z_elements)

        # Ti/Ni/Sn 基 Half-Heusler 通常 ZT ~ 0.5-1.0
        base_zt = 0.5
        if x == "Ti" and y == "Ni":
            base_zt += 0.3
        if z == "Sn":
            base_zt += 0.2
        zt = base_zt + np.random.normal(0, 0.15)
        zt = max(0.1, min(zt, 2.0))

        band_gap = 0.5 + np.random.normal(0, 0.2)
        formation_energy = -0.3 + np.random.normal(0, 0.1)

        data.append({
            "formula": f"{x}{y}{z}",
            "x_elem": x, "y_elem": y, "z_elem": z,
            "band_gap": round(band_gap, 2),
            "formation_energy": round(formation_energy, 2),
            "zt": round(zt, 2),
        })

    return data


# ── Step 2: 特征工程 ────────────────────────────────────────
ELEM_PROPS = {
    "Ti": [1.45, 1.54, 47.9], "Ni": [1.25, 1.91, 58.7],
    "Co": [1.25, 1.88, 58.9], "Fe": [1.25, 1.83, 55.8],
    "Mn": [1.25, 1.55, 54.9], "Cu": [1.30, 1.90, 63.5],
    "Sn": [1.40, 1.96, 118.7], "Sb": [1.40, 2.05, 121.8],
    "Bi": [1.60, 2.02, 209.0], "Ge": [1.25, 2.01, 72.6],
    "Si": [1.10, 1.90, 28.1],
}


def featurize(data):
    """为每条数据计算特征向量。"""
    feature_names = ["半径_avg", "电负性_avg", "质量_avg",
                     "半径_var", "电负性_var", "带隙", "形成能"]
    X, y = [], []

    for d in data:
        elems = [d["x_elem"], d["y_elem"], d["z_elem"]]
        props = np.array([ELEM_PROPS[e] for e in elems])

        avg = props.mean(axis=0)
        var = props.var(axis=0)

        features = list(avg) + list(var) + [d["band_gap"], d["formation_energy"]]
        X.append(features)
        y.append(d["zt"])

    return np.array(X), np.array(y), feature_names


# ── Step 3: 简单搜索优化 ────────────────────────────────────
def greedy_search(X, y, feature_names):
    """基于相关性的贪心特征选择。"""
    correlations = np.array([
        np.abs(np.corrcoef(X[:, i], y)[0, 1])
        for i in range(X.shape[1])
    ])
    top_features = np.argsort(correlations)[-3:]
    print(f"\n  关键特征: {[feature_names[i] for i in top_features]}")
    return top_features, correlations


# ── Step 4: 结果分析 ────────────────────────────────────────
def analyze_results(data, correlations, feature_names):
    """分析并打印结果。"""
    sorted_data = sorted(data, key=lambda d: d["zt"], reverse=True)

    print(f"\n  Top-5 高 ZT Heusler 合金：")
    for i, d in enumerate(sorted_data[:5]):
        print(f"  {i+1}. {d['formula']:<12s} ZT={d['zt']:.2f}  "
              f"带隙={d['band_gap']:.2f}eV  形成能={d['formation_energy']:.2f}eV")

    print(f"\n  特征重要性排序：")
    sorted_idx = np.argsort(correlations)[::-1]
    for i in sorted_idx:
        bar = "#" * int(correlations[i] * 30)
        print(f"  {feature_names[i]:<15s} {correlations[i]:.3f} {bar}")


def main():
    print("=" * 60)
    print("  ep42 - 实战案例：Heusler 合金热电体系")
    print("=" * 60)

    # Step 1: 数据采集
    print("\n  Step 1: 数据采集（模拟 Heusler 合金数据集）")
    data = collect_data()
    print(f"  采集到 {len(data)} 条数据")
    print(f"  示例: {data[0]['formula']} (ZT={data[0]['zt']})")

    # Step 2: 特征工程
    print("\n  Step 2: 特征工程")
    X, y, feature_names = featurize(data)
    print(f"  特征矩阵: {X.shape}")
    print(f"  ZT 范围: [{y.min():.2f}, {y.max():.2f}], 均值: {y.mean():.2f}")

    # Step 3: 搜索优化
    print("\n  Step 3: 特征选择与搜索")
    top_features, correlations = greedy_search(X, y, feature_names)

    # Step 4: 结果分析
    print("\n  Step 4: 结果分析")
    analyze_results(data, correlations, feature_names)

    # 总结
    print(f"\n{'='*60}")
    print("  Pipeline 完成！")
    print(f"{'='*60}")
    print("\n  完整 pipeline 回顾：")
    print("  1. 数据采集: MP/OQMD -> 结构化数据")
    print("  2. 特征工程: 成分 -> Magpie 特征 + 结构描述符")
    print("  3. 搜索优化: 相关性分析 -> 关键特征识别")
    print("  4. 结果分析: Top-K 候选 + 物理解释")
    print("\n  实际项目中每步都更复杂，但核心逻辑一致。")


if __name__ == "__main__":
    main()
