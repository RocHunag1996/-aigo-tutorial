"""
AIGO 教程系列 - 路线 A·构效关系发现
ep36-bayesian-optimization: 贝叶斯优化催化剂成分

实现简化版贝叶斯优化（BO），用 numpy 模拟高斯过程。
目标：优化催化剂成分以最大化反应活性。
"""
import numpy as np
from math import exp, sqrt, erf

# ── 催化剂成分空间定义 ──────────────────────────────────────
COMPONENTS = ["Pt", "Ni", "Co", "Cu"]
N_COMP = len(COMPONENTS)


def true_objective(x):
    """
    真实的催化剂活性目标函数（模拟）。
    x: 各组分摩尔分数（和为 1）。
    返回活性值（越高越好）。
    """
    # Pt-Ni 双金属协同效应
    synergy_pt_ni = 3.0 * x[0] * x[1]
    synergy_pt_co = 1.5 * x[0] * x[2]
    penalty_cu = -2.0 * x[3] ** 2
    base = 1.5 * x[0] + 0.8 * x[1] + 0.5 * x[2] + 0.2 * x[3]
    noise = np.random.normal(0, 0.05)
    return base + synergy_pt_ni + synergy_pt_co + penalty_cu + noise


class SimpleGaussianProcess:
    """
    极简高斯过程（纯 numpy 实现，仅用于教学演示）。
    使用 RBF 核，通过已有数据点做加权插值预测。
    """

    def __init__(self, length_scale=0.3, noise=0.1):
        self.length_scale = length_scale
        self.noise = noise
        self.X_train = None
        self.y_train = None

    def rbf_kernel(self, x1, x2):
        """RBF（平方指数）核函数。"""
        dist = np.sum((x1 - x2) ** 2)
        return np.exp(-0.5 * dist / self.length_scale ** 2)

    def fit(self, X, y):
        """存储训练数据。"""
        self.X_train = np.array(X)
        self.y_train = np.array(y)

    def predict(self, x):
        """预测均值和不确定性（标准差）。"""
        if self.X_train is None:
            return 0.0, 1.0  # 无数据时返回先验

        k_star = np.array([self.rbf_kernel(x, xi) for xi in self.X_train])
        K = np.array([
            [self.rbf_kernel(xi, xj) for xj in self.X_train]
            for xi in self.X_train
        ])
        K += self.noise ** 2 * np.eye(len(self.X_train))

        try:
            alpha = np.linalg.solve(K, self.y_train)
        except np.linalg.LinAlgError:
            alpha = self.y_train / (np.diag(K) + 1e-6)

        # 预测均值
        mu = k_star @ alpha

        # 预测不确定性（简化版）
        k_ss = self.rbf_kernel(x, x)
        var = k_ss - k_star @ np.linalg.solve(K, k_star)
        sigma = np.sqrt(max(var, 1e-6))

        return mu, sigma


def expected_improvement(mu, sigma, best_y, xi=0.01):
    """采集函数：Expected Improvement (EI)。"""
    if sigma < 1e-8:
        return 0.0
    z = (mu - best_y - xi) / sigma
    phi = exp(-0.5 * z ** 2) / sqrt(2 * np.pi)
    Phi = 0.5 * (1 + erf(z / sqrt(2)))
    return sigma * (z * Phi + phi)


def suggest_next_point(gp, n_candidates=500):
    """通过随机采样 + EI 采集函数建议下一个实验点。"""
    candidates = np.random.dirichlet(np.ones(N_COMP), size=n_candidates)
    best_y = gp.y_train.max() if gp.y_train is not None else -np.inf
    ei_values = []

    for c in candidates:
        mu, sigma = gp.predict(c)
        ei = expected_improvement(mu, sigma, best_y)
        ei_values.append(ei)

    best_idx = np.argmax(ei_values)
    return candidates[best_idx], ei_values[best_idx]


def run_bo(n_initial=5, n_iterations=20):
    """运行贝叶斯优化主循环。"""
    print(f"\n  贝叶斯优化参数：初始 {n_initial} 个随机点，迭代 {n_iterations} 轮")

    # 初始随机采样
    X_init = np.random.dirichlet(np.ones(N_COMP), size=n_initial)
    y_init = np.array([true_objective(x) for x in X_init])

    gp = SimpleGaussianProcess()
    gp.fit(X_init, y_init)

    best_so_far = y_init.max()

    print(f"\n  {'轮次':>4s} | {'活性值':>8s} | {'最优值':>8s} | 建议成分")
    print("  " + "-" * 60)

    for i in range(n_initial):
        x, y = X_init[i], y_init[i]
        comp_str = " ".join(f"{c}:{v:.2f}" for c, v in zip(COMPONENTS, x))
        print(f"  初始{i+1:>2d} | {y:>8.3f} | {best_so_far:>8.3f} | {comp_str} <- 初始")

    # BO 迭代
    for iteration in range(n_iterations):
        next_x, ei = suggest_next_point(gp)
        next_y = true_objective(next_x)

        # 更新 GP
        X_all = np.vstack([gp.X_train, next_x])
        y_all = np.append(gp.y_train, next_y)
        gp.fit(X_all, y_all)

        if next_y > best_so_far:
            best_so_far = next_y

        comp_str = " ".join(f"{c}:{v:.2f}" for c, v in zip(COMPONENTS, next_x))
        marker = " *" if next_y >= best_so_far - 0.01 else ""
        print(f"  {iteration+1:>4d} | {next_y:>8.3f} | {best_so_far:>8.3f} | {comp_str}{marker}")

    return gp, best_so_far


def main():
    print("=" * 60)
    print("  ep36 - 贝叶斯优化催化剂成分")
    print("=" * 60)

    print(f"\n  催化剂组分空间: {COMPONENTS}")
    print("  目标: 最大化催化活性（模拟函数含协同效应）")

    np.random.seed(42)
    gp, best_y = run_bo(n_initial=5, n_iterations=15)

    # 最优成分
    best_idx = np.argmax(gp.y_train)
    best_x = gp.X_train[best_idx]
    print(f"\n  最优催化剂成分：")
    for comp, frac in zip(COMPONENTS, best_x):
        bar = "#" * int(frac * 30)
        print(f"  {comp}: {frac:.3f} {bar}")
    print(f"  最优活性值: {best_y:.3f}")

    print("\n  贝叶斯优化 vs 遗传算法：")
    print("  - BO 用概率模型（GP）建模目标函数，减少实验次数")
    print("  - 适合昂贵评估场景（如 DFT 计算、实验合成）")
    print("  - 采集函数平衡探索（不确定性高）与开发（预测值高）")


if __name__ == "__main__":
    main()
