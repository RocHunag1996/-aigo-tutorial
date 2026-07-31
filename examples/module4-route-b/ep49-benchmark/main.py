"""
AIGO 教程系列 - 路线 B·模拟方法创新
ep49-benchmark: Benchmark 实战

从 MD17 数据集下载小分子数据（用 requests），计算 MAE/RMSE 评估指标。
用 numpy 实现评估逻辑。
"""
import numpy as np
import requests
import tempfile
import os


MD17_BASE_URL = "http://quantum-machine.org/gdml/data/npz"
# MD17 小分子列表
MD17_MOLECULES = [
    "aspirin", "benzene", "ethanol", "malonaldehyde",
    "naphthalene", "salicylic", "toluene", "uracil",
]


def download_md17_molecule(molecule="aspirin", data_dir=None):
    """
    下载 MD17 数据集的某个分子。
    返回 numpy 数组（含 R, E, F 等）。
    """
    url = f"{MD17_BASE_URL}/{molecule}_dft.npz"
    print(f"\n  下载 MD17 数据: {molecule}")
    print(f"  URL: {url}")

    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()

        # 保存到临时文件并加载
        if data_dir is None:
            data_dir = tempfile.gettempdir()
        filepath = os.path.join(data_dir, f"{molecule}_dft.npz")
        with open(filepath, "wb") as f:
            f.write(resp.content)

        data = np.load(filepath)
        print(f"  下载成功！数据键: {list(data.keys())}")
        return data

    except Exception as e:
        print(f"  [!] 下载失败: {e}，使用模拟数据")
        return _simulate_md17_data(molecule)


def _simulate_md17_data(molecule):
    """模拟 MD17 数据格式。"""
    np.random.seed(42)
    n_atoms = {"aspirin": 21, "benzene": 12, "ethanol": 9}.get(molecule, 12)
    n_configs = 1000

    # 模拟分子构型（坐标）、能量、力
    R = np.random.randn(n_configs, n_atoms, 3) * 2  # 坐标
    E = np.random.randn(n_configs) * 0.5 - 50       # 能量
    F = np.random.randn(n_configs, n_atoms, 3) * 0.1  # 力

    return {"R": R, "E": E, "F": F}


def compute_mae(y_true, y_pred):
    """平均绝对误差 (MAE)。"""
    return np.mean(np.abs(y_true - y_pred))


def compute_rmse(y_true, y_pred):
    """均方根误差 (RMSE)。"""
    return np.sqrt(np.mean((y_true - y_pred) ** 2))


def compute_force_metrics(F_true, F_pred):
    """计算力的评估指标（按原子分量）。"""
    mae = compute_mae(F_true.flatten(), F_pred.flatten())
    rmse = compute_rmse(F_true.flatten(), F_pred.flatten())

    # 按原子计算力的大小误差
    F_true_norm = np.linalg.norm(F_true, axis=-1)
    F_pred_norm = np.linalg.norm(F_pred, axis=-1)
    magnitude_mae = compute_mae(F_true_norm, F_pred_norm)

    return {"mae": mae, "rmse": rmse, "magnitude_mae": magnitude_mae}


def simulate_ml_predictions(data, noise_level=0.02):
    """
    模拟 ML 模型的预测结果。
    在真实数据上加噪声，模拟 ML 势函数的预测误差。
    """
    E_true = data["E"]
    F_true = data["F"]

    # 模拟预测：真实值 + 噪声
    np.random.seed(123)
    E_pred = E_true + np.random.normal(0, noise_level * np.std(E_true), len(E_true))
    F_pred = F_true + np.random.normal(0, noise_level, F_true.shape)

    return E_pred, F_pred


def evaluate_model(data, molecule_name):
    """评估模型性能。"""
    E_pred, F_pred = simulate_ml_predictions(data)

    # 能量指标
    e_mae = compute_mae(data["E"], E_pred)
    e_rmse = compute_rmse(data["E"], E_pred)

    # 力指标
    f_metrics = compute_force_metrics(data["F"], F_pred)

    print(f"\n  {molecule_name} 评估结果：")
    print(f"  " + "-" * 45)
    print(f"  能量 MAE:  {e_mae*1000:.2f} meV")
    print(f"  能量 RMSE: {e_rmse*1000:.2f} meV")
    print(f"  力的 MAE:  {f_metrics['mae']*1000:.2f} meV/A")
    print(f"  力的 RMSE: {f_metrics['rmse']*1000:.2f} meV/A")
    print(f"  力大小 MAE: {f_metrics['magnitude_mae']*1000:.2f} meV/A")

    return {"energy_mae": e_mae, "force_mae": f_metrics["mae"]}


def main():
    print("=" * 60)
    print("  ep49 - Benchmark 实战：MD17 数据集评估")
    print("=" * 60)

    print(f"\n  MD17 数据集: {len(MD17_MOLECULES)} 个小分子")
    print(f"  分子列表: {MD17_MOLECULES}")

    # 下载/模拟数据
    molecule = "aspirin"
    data = download_md17_molecule(molecule)

    # 检查数据
    print(f"\n  数据形状：")
    for key in data.keys():
        print(f"    {key}: {data[key].shape}")

    # 评估
    results = evaluate_model(data, molecule)

    # 对比多个分子
    print(f"\n  多分子 Benchmark（模拟数据）：")
    print(f"  {'分子':<15s} {'能量MAE(meV)':<15s} {'力MAE(meV/A)':<15s}")
    print("  " + "-" * 45)
    for mol in ["aspirin", "benzene", "ethanol"]:
        sim_data = _simulate_md17_data(mol)
        res = evaluate_model(sim_data, mol)

    print(f"\n  Benchmark 要点：")
    print("  - MAE 和 RMSE 是最常用的评估指标")
    print("  - MD17 是 ML 势函数的标准 Benchmark")
    print("  - 能量精度目标 < 1 meV/atom，力精度 < 10 meV/A")
    print("  - 注意训练集/测试集划分，避免数据泄漏")


if __name__ == "__main__":
    main()
