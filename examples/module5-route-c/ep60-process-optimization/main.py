"""
AIGO 教程系列 - 路线 C·合成路线与工艺设计
ep60-process-optimization: 工艺优化
用贝叶斯优化调优合成工艺参数（温度、时间、配比等）
"""

import numpy as np


def simulate_yield(temperature: float, time_h: float, li_ratio: float) -> float:
    """
    模拟合成产率（黑箱函数）
    实际场景中这是实验结果，这里用经验公式模拟
    """
    # 最优区间：温度 1050-1100°C，时间 10-14h，Li 过量 5-8%
    temp_score = np.exp(-0.5 * ((temperature - 1075) / 75) ** 2)
    time_score = np.exp(-0.5 * ((time_h - 12) / 4) ** 2)
    ratio_score = np.exp(-0.5 * ((li_ratio - 6.5) / 1.5) ** 2)

    # 综合产率 + 噪声
    base_yield = 0.92 * temp_score * time_score * ratio_score
    noise = np.random.normal(0, 0.02)
    return np.clip(base_yield + noise, 0, 1)


class BayesianProcessOptimizer:
    """贝叶斯工艺优化器（简化版）"""

    def __init__(self, bounds: dict):
        """
        bounds: 参数边界，如 {"temperature": (900, 1200), "time": (4, 20)}
        """
        self.bounds = bounds
        self.param_names = list(bounds.keys())
        self.n_params = len(bounds)
        self.observed_X = []
        self.observed_y = []

    def _normalize(self, x: np.ndarray) -> np.ndarray:
        """将参数归一化到 [0, 1]"""
        normed = np.zeros_like(x)
        for i, name in enumerate(self.param_names):
            lo, hi = self.bounds[name]
            normed[i] = (x[i] - lo) / (hi - lo)
        return normed

    def _rbf_kernel(self, x1: np.ndarray, x2: np.ndarray, length_scale: float = 0.3) -> float:
        """RBF 核函数"""
        diff = x1 - x2
        return np.exp(-0.5 * np.sum(diff ** 2) / length_scale ** 2)

    def _build_kernel_matrix(self, X: np.ndarray) -> np.ndarray:
        """构建核矩阵"""
        n = len(X)
        K = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                K[i, j] = self._rbf_kernel(X[i], X[j])
        return K + 1e-6 * np.eye(n)  # 数值稳定性

    def _predict(self, x_new: np.ndarray) -> tuple:
        """高斯过程预测（均值和方差）"""
        if len(self.observed_X) == 0:
            return 0.5, 0.25

        X_obs = np.array([self._normalize(x) for x in self.observed_X])
        y_obs = np.array(self.observed_y)
        x_new_norm = self._normalize(x_new)

        K = self._build_kernel_matrix(X_obs)
        k_star = np.array([self._rbf_kernel(X_obs[i], x_new_norm) for i in range(len(X_obs))])
        k_ss = self._rbf_kernel(x_new_norm, x_new_norm)

        # 求解线性系统
        try:
            alpha = np.linalg.solve(K, y_obs - np.mean(y_obs))
            mu = np.dot(k_star, alpha) + np.mean(y_obs)
            v = np.linalg.solve(K, k_star)
            var = k_ss - np.dot(k_star, v)
            var = max(var, 1e-6)
        except np.linalg.LinAlgError:
            mu = np.mean(y_obs)
            var = 0.1

        return mu, var

    def _acquisition(self, x: np.ndarray, xi: float = 0.01) -> float:
        """Expected Improvement 采集函数"""
        mu, var = self._predict(x)
        sigma = np.sqrt(var)
        if sigma < 1e-8:
            return 0.0

        best_y = max(self.observed_y) if self.observed_y else 0
        z = (mu - best_y - xi) / sigma
        # 标准正态分布 PDF 和 CDF 近似
        from math import exp, sqrt, erf
        phi = exp(-0.5 * z ** 2) / sqrt(2 * np.pi)
        Phi = 0.5 * (1 + erf(z / sqrt(2)))
        return sigma * (z * Phi + phi)

    def suggest_next(self, n_candidates: int = 100) -> np.ndarray:
        """建议下一个实验点"""
        best_acq = -1
        best_x = None

        for _ in range(n_candidates):
            # 随机采样候选点
            x = np.array([
                np.random.uniform(lo, hi)
                for lo, hi in [self.bounds[n] for n in self.param_names]
            ])
            acq = self._acquisition(x)
            if acq > best_acq:
                best_acq = acq
                best_x = x

        return best_x

    def observe(self, x: np.ndarray, y: float):
        """记录实验结果"""
        self.observed_X.append(x.tolist())
        self.observed_y.append(y)

    def run_optimization(self, n_iterations: int = 15, eval_fn=None):
        """运行优化循环"""
        if eval_fn is None:
            eval_fn = lambda x: simulate_yield(x[0], x[1], x[2])

        print("\n贝叶斯工艺优化")
        print("=" * 60)
        print(f"{'迭代':>4s} | {'温度°C':>8s} | {'时间h':>6s} | {'Li过量':>6s} | {'产率':>6s} | {'状态':>4s}")
        print("-" * 60)

        # 初始随机采样 3 个点
        for i in range(3):
            x = np.array([
                np.random.uniform(lo, hi)
                for lo, hi in [self.bounds[n] for n in self.param_names]
            ])
            y = eval_fn(x)
            self.observe(x, y)
            print(f"  init | {x[0]:8.1f} | {x[1]:6.1f} | {x[2]:6.2f} | {y:6.3f} | 随机")

        # 贝叶斯优化迭代
        best_y = max(self.observed_y)
        for i in range(n_iterations):
            x_next = self.suggest_next()
            y_next = eval_fn(x_next)
            self.observe(x_next, y_next)

            improved = "↑" if y_next > best_y else ""
            if y_next > best_y:
                best_y = y_next

            print(f"  {i+1:4d} | {x_next[0]:8.1f} | {x_next[1]:6.1f} | {x_next[2]:6.2f} | {y_next:6.3f} | {improved}")

        print("-" * 60)
        best_idx = np.argmax(self.observed_y)
        best_x = self.observed_X[best_idx]
        print(f"\n最优工艺参数：")
        for j, name in enumerate(self.param_names):
            print(f"  {name}: {best_x[j]:.2f}")
        print(f"  最优产率: {self.observed_y[best_idx]:.4f}")

        return best_x, self.observed_y[best_idx]


def main():
    print("ep60 - 工艺优化（贝叶斯优化合成参数）")
    print("=" * 60)

    np.random.seed(42)

    # 定义参数边界
    bounds = {
        "temperature": (900, 1200),   # °C
        "time": (4, 20),              # 小时
        "li_excess": (3.0, 10.0),     # Li 过量百分比
    }

    optimizer = BayesianProcessOptimizer(bounds)
    best_x, best_y = optimizer.run_optimization(n_iterations=12)

    print("\n" + "=" * 60)
    print("工艺优化要点：")
    print("""
    1. 贝叶斯优化适合高成本实验（每次实验耗时数天）
    2. 采集函数平衡探索（高不确定性）和利用（高预测值）
    3. 通常 15-30 次迭代即可找到近最优条件
    4. 可加入约束（如温度上限、安全限制）
    5. 与知识库结合：用历史数据初始化 GP 先验
    """)


if __name__ == "__main__":
    main()
