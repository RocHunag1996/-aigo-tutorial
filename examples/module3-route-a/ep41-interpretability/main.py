"""
AIGO 教程系列 - 路线 A·构效关系发现
ep41-interpretability: 可解释性分析

计算特征重要性（相关性分析 + 排序），给构效关系一个物理解释。
用 numpy 实现，不依赖 sklearn 等重型库。
"""
import numpy as np


# ── 模拟数据集 ──────────────────────────────────────────────
FEATURE_NAMES = [
    "原子半径(加权平均)", "电负性(加权平均)", "原子质量(加权平均)",
    "价电子数(加权平均)", "熔点(加权平均)",
    "原子半径(方差)", "电负性(方差)",
    "原子半径(极差)", "电负性(极差)",
    "空间群编号", "晶胞原子数",
]

np.random.seed(42)
N_SAMPLES = 80
N_FEATURES = len(FEATURE_NAMES)

# 模拟特征矩阵
X = np.random.randn(N_SAMPLES, N_FEATURES)

# 模拟目标变量 ZT（与部分特征有真实关系）
ZT = (
    0.5 * X[:, 1]      # 电负性正相关
    - 0.3 * X[:, 4]    # 熔点负相关
    + 0.8 * X[:, 6]    # 电负性方差正相关
    + 0.2 * X[:, 9]    # 空间群弱正相关
    + np.random.normal(0, 0.3, N_SAMPLES)
)


def pearson_correlation(x, y):
    """计算 Pearson 相关系数。"""
    x_c = x - x.mean()
    y_c = y - y.mean()
    num = np.sum(x_c * y_c)
    den = np.sqrt(np.sum(x_c**2) * np.sum(y_c**2))
    return num / den if den > 1e-10 else 0.0


def compute_feature_importance(X, y, feature_names):
    """计算特征重要性：基于 |Pearson 相关系数| 排序。"""
    importances = []
    for i, name in enumerate(feature_names):
        r = pearson_correlation(X[:, i], y)
        importances.append({
            "feature": name,
            "correlation": r,
            "abs_correlation": abs(r),
        })
    importances.sort(key=lambda x: x["abs_correlation"], reverse=True)
    return importances


def compute_mutual_information_proxy(X, y, feature_names, n_bins=10):
    """互信息的简化近似：将连续值离散化后计算。"""
    mi_scores = []
    for i, name in enumerate(feature_names):
        x = X[:, i]
        x_bins = np.digitize(x, np.linspace(x.min(), x.max(), n_bins))
        y_bins = np.digitize(y, np.linspace(y.min(), y.max(), n_bins))

        joint = np.zeros((n_bins + 1, n_bins + 1))
        for xi, yi in zip(x_bins, y_bins):
            joint[xi, yi] += 1
        joint /= joint.sum()

        px = joint.sum(axis=1)
        py = joint.sum(axis=0)

        mi = 0.0
        for xi in range(joint.shape[0]):
            for yi in range(joint.shape[1]):
                if joint[xi, yi] > 0 and px[xi] > 0 and py[yi] > 0:
                    mi += joint[xi, yi] * np.log(joint[xi, yi] / (px[xi] * py[yi]))

        mi_scores.append({"feature": name, "mi_proxy": mi})

    mi_scores.sort(key=lambda x: x["mi_proxy"], reverse=True)
    return mi_scores


def print_importance_bar(importances, top_n=8):
    """用 ASCII 条形图展示特征重要性。"""
    max_val = max(d["abs_correlation"] for d in importances[:top_n])
    print(f"\n  {'特征':<25s} {'相关系数':>8s} | 重要性")
    print("-" * 60)
    for d in importances[:top_n]:
        bar_len = int(d["abs_correlation"] / max_val * 25) if max_val > 0 else 0
        bar = "#" * bar_len
        sign = "+" if d["correlation"] > 0 else "-"
        print(f"  {d['feature']:<23s} {sign}{d['abs_correlation']:.3f}   | {bar}")


def physical_interpretation(importances):
    """基于排序结果给出物理解释。"""
    print("\n  物理解释：")
    print("-" * 55)

    for d in importances[:3]:
        name = d["feature"]
        r = d["correlation"]
        direction = "正相关" if r > 0 else "负相关"

        if "电负性" in name and "方差" in name:
            print(f"  * {name} ({direction})")
            print(f"    -> 元素间电负性差异大 -> 声子散射增强 -> 热导率降低 -> ZT 提升")
        elif "电负性" in name:
            print(f"  * {name} ({direction})")
            print(f"    -> 电负性影响能带结构和载流子浓度")
        elif "熔点" in name:
            print(f"  * {name} ({direction})")
            print(f"    -> 低熔点元素常对应弱键合 -> 低声子频率 -> 低热导率")
        else:
            print(f"  * {name} ({direction})")
            print(f"    -> 该特征对热电性能有显著影响，值得深入研究")


def main():
    print("=" * 60)
    print("  ep41 - 可解释性分析：特征重要性与物理解释")
    print("=" * 60)

    print(f"\n  数据集: {N_SAMPLES} 个样本, {N_FEATURES} 个特征")
    print(f"  目标变量: 热电优值 ZT")

    # 1. Pearson 相关性分析
    print("\n  Step 1: Pearson 相关性分析")
    importances = compute_feature_importance(X, ZT, FEATURE_NAMES)
    print_importance_bar(importances)

    # 2. 互信息近似
    print("\n\n  Step 2: 互信息近似（捕捉非线性关系）")
    mi_scores = compute_mutual_information_proxy(X, ZT, FEATURE_NAMES)
    print(f"\n  {'特征':<25s} {'互信息':>8s}")
    print("  " + "-" * 40)
    for d in mi_scores[:8]:
        bar = "#" * int(d["mi_proxy"] * 50)
        print(f"  {d['feature']:<25s} {d['mi_proxy']:.4f}  {bar}")

    # 3. 物理解释
    physical_interpretation(importances)

    print(f"\n  可解释性分析要点：")
    print("  - Pearson 相关只能捕捉线性关系，互信息可捕捉非线性")
    print("  - 特征重要性排序帮助聚焦关键因素")
    print("  - 最终需要领域知识将统计关系转化为物理解释")
    print("  - 相关性不等于因果性，需要进一步实验验证")


if __name__ == "__main__":
    main()
