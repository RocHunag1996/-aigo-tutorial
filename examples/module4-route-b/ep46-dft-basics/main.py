"""
AIGO 教程系列 - 路线 B·模拟方法创新
ep46-dft-basics: DFT 计算基础

用 numpy 演示一维势阱中求解 Kohn-Sham 方程的简化版本。
粒子在箱中 + 自洽场循环示意。
"""
import numpy as np


# ── 物理常数（原子单位）─────────────────────────────────────
HBAR = 1.0    # hbar = 1 (原子单位)
MASS = 1.0    # 电子质量 = 1 (原子单位)


def infinite_well_states(L, n_grid=200, n_states=3):
    """
    一维无限深势阱的解析解（作为初始猜测）。
    V(x) = 0 for 0 < x < L, else infinity.
    解析解: psi_n(x) = sqrt(2/L) * sin(n*pi*x/L)
    """
    x = np.linspace(0, L, n_grid)
    states = []
    energies = []

    for n in range(1, n_states + 1):
        psi = np.sqrt(2 / L) * np.sin(n * np.pi * x / L)
        E = n**2 * np.pi**2 * HBAR**2 / (2 * MASS * L**2)
        states.append(psi)
        energies.append(E)

    return x, states, energies


def build_hamiltonian(x, L, V_ext):
    """
    构建一维哈密顿量矩阵 H = T + V。
    动能用有限差分: T = -hbar^2/(2m) * d^2/dx^2
    """
    n_grid = len(x)
    dx = x[1] - x[0]

    # 动能矩阵（三对角）
    T = np.zeros((n_grid, n_grid))
    coeff = -HBAR**2 / (2 * MASS * dx**2)
    for i in range(n_grid):
        T[i, i] = -2 * coeff
        if i > 0:
            T[i, i-1] = coeff
        if i < n_grid - 1:
            T[i, i+1] = coeff

    # 势能矩阵（对角）
    V = np.diag(V_ext)

    return T + V


def solve_scf(L=5.0, n_grid=100, n_electrons=2, n_cycles=10):
    """
    简化版自洽场（SCF）循环演示。
    模拟 Kohn-Sham DFT 的核心思想：
    1. 猜测初始电子密度
    2. 构建有效势 V_eff = V_ext + V_Hartree + V_xc
    3. 求解 H * psi = E * psi
    4. 从 psi 计算新密度
    5. 重复直到收敛
    """
    x = np.linspace(0, L, n_grid)
    dx = x[1] - x[0]

    # 外势：谐振子势
    V_ext = 0.5 * (x - L/2)**2

    # 初始电子密度猜测（高斯分布）
    rho = n_electrons * np.exp(-2 * (x - L/2)**2) / (np.sqrt(np.pi) * L/4)
    rho = rho / np.sum(rho * dx) * n_electrons  # 归一化

    print(f"\n  SCF 参数: L={L}, 网格={n_grid}, 电子数={n_electrons}")
    print(f"\n  {'循环':>4s} | {'总能量':>10s} | {'密度误差':>10s}")
    print("  " + "-" * 35)

    energies_history = []

    for cycle in range(n_cycles):
        # 构建有效势（简化：V_eff = V_ext + alpha * rho）
        alpha = 0.1  # 模拟 Hartree + XC 相互作用
        V_eff = V_ext + alpha * rho

        # 构建并求解哈密顿量
        H = build_hamiltonian(x, L, V_eff)
        eigenvalues, eigenvectors = np.linalg.eigh(H)

        # 从最低能态开始填充电子（每个态 2 个电子，自旋上下）
        rho_new = np.zeros(n_grid)
        n_filled = max(1, n_electrons // 2)
        total_e = 0.0
        for i in range(n_filled):
            psi = eigenvectors[:, i]
            rho_new += 2 * psi**2  # 自旋简并
            total_e += 2 * eigenvalues[i]

        # 归一化密度
        rho_new = rho_new / np.sum(rho_new * dx) * n_electrons

        # 计算收敛指标
        density_error = np.sqrt(np.sum((rho_new - rho)**2) * dx)
        rho = rho_new
        energies_history.append(total_e)

        print(f"  {cycle+1:>4d} | {total_e:>10.4f} | {density_error:>10.6f}")

        if density_error < 1e-6:
            print(f"\n  SCF 在第 {cycle+1} 轮收敛！")
            break

    return x, rho, energies_history


def main():
    print("=" * 60)
    print("  ep46 - DFT 计算基础：一维 Kohn-Sham 方程求解")
    print("=" * 60)

    # 演示 1：无限深势阱解析解
    print("\n  一维无限深势阱解析解：")
    x, states, energies = infinite_well_states(L=5.0, n_states=3)
    for n, E in enumerate(energies, 1):
        print(f"  n={n}: E = {E:.4f} Ha ({E*27.211:.2f} eV)")

    # 演示 2：SCF 自洽场循环
    print("\n  自洽场（SCF）循环演示：")
    x, rho, energies = solve_scf(L=5.0, n_grid=100, n_electrons=2, n_cycles=10)

    print(f"\n  能量收敛历史:")
    for i, E in enumerate(energies):
        bar = "#" * int((E - energies[0]) / (energies[-1] - energies[0] + 1e-10) * 30)
        print(f"  第{i+1}轮: E = {E:.4f} {bar}")

    print(f"\n  核心概念：")
    print("  - Kohn-Sham 方程将多体问题转化为单粒子在有效势中的问题")
    print("  - SCF 循环：猜密度 -> 建势 -> 求解 -> 更新密度 -> 收敛？")
    print("  - 实际 DFT（VASP/QE）在三维周期体系中做同样的事")
    print("  - ML 势函数的目标：用机器学习替代昂贵的 DFT 计算")


if __name__ == "__main__":
    main()
