"""
AIGO 教程系列 - 路线 B·模拟方法创新
ep48-mace-tutorial: 上手 MACE

演示 MACE 训练数据准备格式、数据结构示例、训练配置。
不实际训练（太重），展示数据准备和配置流程。
"""
import json
import numpy as np


def demo_atoms_structure():
    """
    演示 ASE Atoms 数据结构（MACE 的输入格式）。
    实际项目中用 ASE 库，这里用 dict 模拟。
    """
    # Bi2Te3 晶体结构示例
    atoms_data = {
        "symbols": ["Bi", "Bi", "Te", "Te", "Te"],
        "positions": [
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 3.0],
            [0.0, 0.0, 1.5],
            [0.0, 0.0, 4.5],
            [2.0, 0.0, 2.5],
        ],
        "cell": [[4.3, 0.0, 0.0], [0.0, 4.3, 0.0], [0.0, 0.0, 30.0]],
        "pbc": [True, True, True],  # 周期性边界条件
    }

    print("  ASE Atoms 数据结构示例（Bi2Te3）：")
    print(f"  化学式: {''.join(atoms_data['symbols'])}")
    print(f"  原子数: {len(atoms_data['symbols'])}")
    print(f"  晶格常数: a={atoms_data['cell'][0][0]}, c={atoms_data['cell'][2][2]}")
    print(f"  周期性: {atoms_data['pbc']}")
    print(f"  原子坐标:")
    for sym, pos in zip(atoms_data["symbols"], atoms_data["positions"]):
        print(f"    {sym}: [{pos[0]:.1f}, {pos[1]:.1f}, {pos[2]:.1f}]")

    return atoms_data


def generate_training_data(n_configs=5):
    """
    生成模拟训练数据（MACE 格式）。
    真实数据应从 DFT 计算（VASP/Quantum ESPRESSO）获取。
    """
    print(f"\n  生成 {n_configs} 个训练构型（模拟数据）...")

    training_set = []
    np.random.seed(42)

    for i in range(n_configs):
        # 模拟不同晶格畸变下的能量和力
        strain = np.random.uniform(-0.05, 0.05, size=3)
        energy = -15.0 + 0.5 * np.sum(strain**2) + np.random.normal(0, 0.01)
        forces = np.random.normal(0, 0.1, size=(5, 3))  # 5 个原子

        config = {
            "config_id": f"config_{i+1}",
            "atomic_numbers": [83, 83, 52, 52, 52],  # Bi=83, Te=52
            "positions": (np.array([
                [0.0, 0.0, 0.0], [0.0, 0.0, 3.0],
                [0.0, 0.0, 1.5], [0.0, 0.0, 4.5],
                [2.0, 0.0, 2.5],
            ]) * (1 + strain[:, None])).tolist(),
            "cell": [[4.3*(1+strain[0]), 0, 0],
                     [0, 4.3*(1+strain[1]), 0],
                     [0, 0, 30.0*(1+strain[2])]],
            "energy": round(energy, 4),
            "forces": forces.round(4).tolist(),
            "stress": (np.random.normal(0, 0.01, 6)).round(4).tolist(),
        }
        training_set.append(config)
        print(f"    构型 {i+1}: E={energy:.4f} eV, |F|max={np.abs(forces).max():.4f} eV/A")

    return training_set


def print_mace_config():
    """打印 MACE 训练配置示例。"""
    config = {
        "model": "MACE",
        "r_max": 5.0,           # 截断半径
        "num_bessel": 8,        # Bessel 基函数数量
        "num_polynomials": 5,   # 多项式截断函数阶数
        "max_ell": 3,           # 球谐函数最大角动量
        "correlation": 3,       # 消息传递阶数
        "num_interactions": 2,  # 相互作用层数
        "hidden_irreps": "128x0e + 128x1o",  # 隐藏层表示
        "MLP_irreps": "16x0e",  # 读出 MLP
        "training": {
            "lr": 0.01,
            "batch_size": 10,
            "max_num_epochs": 200,
            "patience": 20,      # 早停耐心值
            "ema_decay": 0.99,
            "scheduler": "ReduceLROnPlateau",
        },
        "data": {
            "train_file": "train.xyz",
            "valid_file": "valid.xyz",
            "energy_key": "DFT_energy",
            "forces_key": "DFT_forces",
            "stress_key": "DFT_stress",
        },
    }

    print("\n  MACE 训练配置示例：")
    print("=" * 55)
    print(json.dumps(config, indent=2, ensure_ascii=False))
    print("=" * 55)


def print_data_pipeline():
    """打印数据准备流水线。"""
    print("\n  MACE 数据准备流水线：")
    print("  " + "-" * 55)
    steps = [
        ("1. 结构生成", "DFT 优化 + 扰动/MD 采样 -> 多种构型"),
        ("2. DFT 计算", "VASP/QE 计算能量、力、应力"),
        ("3. 格式转换", "VASP OUTCAR -> extxyz 格式（ASE 工具）"),
        ("4. 数据划分", "训练集 80% / 验证集 10% / 测试集 10%"),
        ("5. 训练 MACE", "mace_run_train --config config.yaml"),
        ("6. 验证部署", "对比 DFT vs MACE 预测，部署到 MD 模拟"),
    ]
    for step, desc in steps:
        print(f"  {step}: {desc}")


def main():
    print("=" * 60)
    print("  ep48 - 上手 MACE：数据准备与训练配置")
    print("=" * 60)

    # 1. 演示原子结构
    print("\n  Step 1: 理解输入数据结构")
    demo_atoms_structure()

    # 2. 生成训练数据
    print("\n  Step 2: 准备训练数据")
    training_data = generate_training_data(n_configs=5)

    # 3. 训练配置
    print("\n  Step 3: 训练配置")
    print_mace_config()

    # 4. 数据流水线
    print_data_pipeline()

    print(f"\n  注意事项：")
    print("  - 训练数据质量决定模型质量（垃圾进垃圾出）")
    print("  - 建议至少 1000 个构型，覆盖目标温度/压力范围")
    print("  - 预训练 MACE-MP 可大幅减少所需训练数据")
    print("  - GPU 训练，单次训练约需数小时到数天")


if __name__ == "__main__":
    main()
