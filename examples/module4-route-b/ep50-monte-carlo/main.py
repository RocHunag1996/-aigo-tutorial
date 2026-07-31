"""
AIGO 教程系列 - 路线 B·模拟方法创新
ep50-monte-carlo: 蒙特卡洛模拟

用 numpy 实现 Metropolis MC 模拟（2D Ising 模型）。
演示相变观测和加速思路。
"""
import numpy as np


def initialize_lattice(L, random=True):
    """初始化 L x L 的 2D Ising 自旋格子。"""
    if random:
        return np.random.choice([-1, 1], size=(L, L))
    else:
        return np.ones((L, L))


def compute_energy(lattice, J=1.0):
    """
    计算 Ising 模型总能量。
    H = -J * sum(s_i * s_j)，对最近邻求和。
    """
    L = lattice.shape[0]
    energy = 0.0
    for i in range(L):
        for j in range(L):
            s = lattice[i, j]
            # 四个最近邻（周期性边界）
            neighbors = (
                lattice[(i+1) % L, j] +
                lattice[(i-1) % L, j] +
                lattice[i, (j+1) % L] +
                lattice[i, (j-1) % L]
            )
            energy += -J * s * neighbors
    return energy / 2  # 避免重复计数


def delta_energy(lattice, i, j, J=1.0):
    """计算翻转自旋 (i,j) 的能量变化（避免全量重算）。"""
    L = lattice.shape[0]
    s = lattice[i, j]
    neighbors = (
        lattice[(i+1) % L, j] +
        lattice[(i-1) % L, j] +
        lattice[i, (j+1) % L] +
        lattice[i, (j-1) % L]
    )
    return 2 * J * s * neighbors


def metropolis_step(lattice, temperature, J=1.0):
    """
    单步 Metropolis 算法。
    随机选一个自旋，按 Boltzmann 概率决定是否翻转。
    """
    L = lattice.shape[0]
    i = np.random.randint(0, L)
    j = np.random.randint(0, L)

    dE = delta_energy(lattice, i, j, J)

    # Metropolis 判据
    if dE <= 0 or np.random.random() < np.exp(-dE / temperature):
        lattice[i, j] *= -1
        return True  # 接受
    return False  # 拒绝


def run_mc_simulation(L=20, n_steps=5000, temperatures=None):
    """
    运行 Metropolis MC 模拟，扫描温度。
    观测磁化强度和能量随温度的变化。
    """
    if temperatures is None:
        temperatures = np.linspace(1.0, 5.0, 20)

    print(f"\n  MC 模拟参数: L={L}, 每温度步数={n_steps}")
    print(f"  温度范围: [{temperatures[0]:.1f}, {temperatures[-1]:.1f}]")
    print(f"\n  {'温度':>6s} | {'能量/N':>10s} | {'|磁化|/N':>10s} | {'接受率':>8s}")
    print("  " + "-" * 50)

    results = []

    for T in temperatures:
        lattice = initialize_lattice(L, random=True)
        n_accepted = 0

        # 热平衡阶段（丢弃）
        for _ in range(n_steps // 4):
            if metropolis_step(lattice, T):
                n_accepted += 1

        # 采样阶段
        n_accepted = 0
        energy_samples = []
        magnetization_samples = []

        for step in range(n_steps):
            if metropolis_step(lattice, T):
                n_accepted += 1

            if step % 10 == 0:  # 每隔几步采样（减少关联）
                E = compute_energy(lattice)
                M = np.abs(np.sum(lattice))
                energy_samples.append(E)
                magnetization_samples.append(M)

        # 统计
        E_avg = np.mean(energy_samples) / (L * L)
        M_avg = np.mean(magnetization_samples) / (L * L)
        accept_rate = n_accepted / n_steps

        results.append({"T": T, "E": E_avg, "M": M_avg})
        print(f"  {T:>6.2f} | {E_avg:>10.4f} | {M_avg:>10.4f} | {accept_rate:>8.1%}")

    return results


def print_phase_transition(results):
    """可视化相变行为（ASCII 图）。"""
    print("\n  磁化强度 vs 温度（ASCII 图）：")
    print("  " + "-" * 50)
    max_M = max(r["M"] for r in results) if results else 1.0

    for r in results:
        bar_len = int(r["M"] / max_M * 30) if max_M > 0 else 0
        bar = "#" * bar_len
        phase = "铁磁" if r["M"] > 0.3 else "顺磁"
        print(f"  T={r['T']:.2f} | {bar:<30s} | M={r['M']:.3f} ({phase})")

    print("\n  相变温度（居里温度）约在 T_c ~ 2.27（二维 Ising 精确解）")


def main():
    print("=" * 60)
    print("  ep50 - 蒙特卡洛模拟：2D Ising 模型")
    print("=" * 60)

    print("\n  Ising 模型: H = -J * sum(s_i * s_j)")
    print("  每个格点 s_i = +/-1，与最近邻相互作用")
    print("  二维 Ising 模型有精确解，居里温度 T_c = 2J/ln(1+sqrt(2))")

    np.random.seed(42)
    results = run_mc_simulation(L=20, n_steps=2000)

    print_phase_transition(results)

    print(f"\n  加速思路：")
    print("  - 向量化: 用 numpy 批量计算能量变化，避免 Python 循环")
    print("  - Wolff 算法: 簇翻转，大幅减少临界慢化")
    print("  - ML 加速: 用神经网络学习自旋构型，跳过部分 MC 步")
    print("  - 并行: 不同温度点可完全并行（embarrassingly parallel）")


if __name__ == "__main__":
    main()
