"""
AIGO 教程系列 - 路线 B·模拟方法创新
ep51-ml-md: 分子动力学新架构

用 numpy 实现简单 Verlet 积分 MD（Lennard-Jones 势）。
展示 ML-MD 耦合概念：用 ML 势函数替代传统力场。
"""
import numpy as np


# ── Lennard-Jones 势 ────────────────────────────────────────
def lj_potential(r, epsilon=1.0, sigma=1.0):
    """Lennard-Jones 势: V(r) = 4*eps*((sig/r)^12 - (sig/r)^6)"""
    return 4 * epsilon * ((sigma / r)**12 - (sigma / r)**6)


def lj_force(r, epsilon=1.0, sigma=1.0):
    """LJ 力的大小: F(r) = -dV/dr"""
    return 24 * epsilon / r * (2 * (sigma / r)**12 - (sigma / r)**6)


def compute_forces(positions, epsilon=1.0, sigma=1.0, rcut=3.0):
    """
    计算所有粒子的受力。
    positions: (N, dim) 数组。
    """
    N = positions.shape[0]
    forces = np.zeros_like(positions)
    total_pe = 0.0

    for i in range(N):
        for j in range(i + 1, N):
            r_vec = positions[j] - positions[i]
            r = np.linalg.norm(r_vec)

            if r < rcut and r > 1e-10:
                f_mag = lj_force(r, epsilon, sigma)
                f_vec = f_mag * r_vec / r
                forces[i] += f_vec
                forces[j] -= f_vec
                total_pe += lj_potential(r, epsilon, sigma)

    return forces, total_pe


def velocity_verlet(positions, velocities, dt=0.01, mass=1.0, n_steps=100):
    """
    Velocity Verlet 积分器。
    返回轨迹和能量历史。
    """
    N = positions.shape[0]
    traj = [positions.copy()]
    ke_history = []
    pe_history = []
    te_history = []

    forces, pe = compute_forces(positions)

    for step in range(n_steps):
        # 动能
        ke = 0.5 * mass * np.sum(velocities**2)

        ke_history.append(ke)
        pe_history.append(pe)
        te_history.append(ke + pe)
        traj.append(positions.copy())

        # Velocity Verlet 步骤
        # 1. 更新位置: r(t+dt) = r(t) + v(t)*dt + 0.5*a(t)*dt^2
        accelerations = forces / mass
        positions += velocities * dt + 0.5 * accelerations * dt**2

        # 2. 计算新力
        old_forces = forces.copy()
        forces, pe = compute_forces(positions)
        new_accelerations = forces / mass

        # 3. 更新速度: v(t+dt) = v(t) + 0.5*(a(t) + a(t+dt))*dt
        velocities += 0.5 * (accelerations + new_accelerations) * dt

    return np.array(traj), ke_history, pe_history, te_history


def initialize_positions(n_particles=8, box_size=6.0):
    """初始化粒子位置（简单网格排列）。"""
    n_side = int(np.ceil(n_particles ** (1/2)))
    positions = []
    spacing = box_size / n_side

    for i in range(n_side):
        for j in range(n_side):
            if len(positions) < n_particles:
                positions.append([i * spacing + spacing/2,
                                  j * spacing + spacing/2])

    return np.array(positions[:n_particles])


def initialize_velocities(n_particles, temperature=1.0, mass=1.0):
    """初始化速度（Maxwell-Boltzmann 分布）。"""
    np.random.seed(42)
    sigma_v = np.sqrt(temperature / mass)
    velocities = np.random.normal(0, sigma_v, size=(n_particles, 2))
    # 去除质心运动
    velocities -= velocities.mean(axis=0)
    return velocities


def main():
    print("=" * 60)
    print("  ep51 - 分子动力学：Verlet 积分 + LJ 势")
    print("=" * 60)

    n_particles = 8
    box_size = 6.0
    dt = 0.005
    n_steps = 200
    temperature = 1.0

    print(f"\n  MD 参数：")
    print(f"  粒子数: {n_particles}")
    print(f"  模拟步长: {dt}")
    print(f"  总步数: {n_steps}")
    print(f"  初始温度: {temperature}")

    # 初始化
    positions = initialize_positions(n_particles, box_size)
    velocities = initialize_velocities(n_particles, temperature)

    print(f"\n  初始构型：")
    for i, pos in enumerate(positions):
        print(f"  粒子 {i}: ({pos[0]:.2f}, {pos[1]:.2f})")

    # 运行 MD
    print(f"\n  运行 Velocity Verlet MD...")
    traj, ke_hist, pe_hist, te_hist = velocity_verlet(
        positions, velocities, dt=dt, n_steps=n_steps
    )

    # 结果分析
    print(f"\n  能量统计（最后 50 步）：")
    ke_avg = np.mean(ke_hist[-50:])
    pe_avg = np.mean(pe_hist[-50:])
    te_avg = np.mean(te_hist[-50:])
    te_std = np.std(te_hist[-50:])

    print(f"  动能 <KE> = {ke_avg:.4f}")
    print(f"  势能 <PE> = {pe_avg:.4f}")
    print(f"  总能 <TE> = {te_avg:.4f} (波动: {te_std:.4f})")

    # 能量守恒检查
    print(f"\n  能量守恒检查（总能量波动）：")
    te_range = max(te_hist) - min(te_hist)
    print(f"  总能最大波动: {te_range:.4f}")
    print(f"  相对波动: {te_range / abs(te_avg) * 100:.2f}%")

    # ML-MD 耦合概念
    print(f"\n  ML-MD 耦合概念：")
    print("  传统 MD: 用解析势函数（如 LJ）计算力 -> 快但精度有限")
    print("  ML-MD:   用 ML 势函数（如 MACE）计算力 -> 接近 DFT 精度")
    print("  工作流:")
    print("    1. 用 MACE 等 ML 模型替代 compute_forces()")
    print("    2. 输入原子坐标 -> ML 模型 -> 输出能量和力")
    print("    3. 力传入 Verlet 积分器 -> 更新轨迹")
    print("    4. 精度接近 DFT，速度接近经验势")


if __name__ == "__main__":
    main()
