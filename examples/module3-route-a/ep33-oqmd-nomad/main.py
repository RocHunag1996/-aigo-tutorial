"""
AIGO 教程系列 - 路线 A·构效关系发现
ep33-oqmd-nomad: OQMD 与 NOMAD 数据库 REST API 查询

演示用 requests 调用 OQMD REST API 查询材料数据。
OQMD (Open Quantum Materials Database): http://oqmd.org/
"""
import requests

OQMD_BASE_URL = "http://oqmd.org/api"


def query_oqmd_by_formula(formula="Bi2Te3", limit=5):
    """
    通过化学式查询 OQMD 数据库。
    OQMD REST API 提供材料计算结果（形成能、带隙、结构等）。
    """
    url = f"{OQMD_BASE_URL}/entry"
    params = {
        "composition": formula,
        "limit": limit,
        "fields": "name,prototype,formation_energy,band_gap,spacegroup",
    }

    print(f"\n  OQMD 查询: 化学式 = {formula}")
    print(f"  端点: {url}")

    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        return data
    except requests.exceptions.Timeout:
        print("  [!] OQMD 服务响应超时（该数据库有时较慢）")
        return _demo_oqmd_data(formula)
    except requests.exceptions.ConnectionError:
        print("  [!] 无法连接 OQMD 服务，使用演示数据")
        return _demo_oqmd_data(formula)
    except Exception as e:
        print(f"  [!] 查询异常: {e}，使用演示数据")
        return _demo_oqmd_data(formula)


def query_oqmd_by_formation_energy(energy_max=-0.1, limit=5):
    """
    按形成能筛选稳定材料。
    形成能越负 -> 热力学越稳定。
    """
    url = f"{OQMD_BASE_URL}/entry"
    params = {
        "formation_energy__lt": energy_max,
        "limit": limit,
        "fields": "name,composition,formation_energy,band_gap",
    }

    print(f"\n  OQMD 查询: 形成能 < {energy_max} eV/atom")

    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        print("  [!] 连接异常，使用演示数据")
        return _demo_stable_materials()


def _demo_oqmd_data(formula):
    """演示数据：模拟 OQMD 返回格式。"""
    return {
        "entries": [
            {
                "name": f"{formula} (demo)",
                "prototype": "R-3m",
                "formation_energy": -0.18,
                "band_gap": 0.33,
                "spacegroup": 166,
            }
        ],
        "total_count": 1,
    }


def _demo_stable_materials():
    """演示数据：稳定材料列表。"""
    return {
        "entries": [
            {"name": "Bi2Te3", "composition": "Bi2Te3",
             "formation_energy": -0.18, "band_gap": 0.33},
            {"name": "PbTe", "composition": "PbTe",
             "formation_energy": -0.25, "band_gap": 0.80},
            {"name": "CoSb3", "composition": "CoSb3",
             "formation_energy": -0.32, "band_gap": 0.52},
            {"name": "Half-Heusler TiNiSn", "composition": "TiNiSn",
             "formation_energy": -0.41, "band_gap": 0.95},
        ],
        "total_count": 4,
    }


def display_oqmd_results(data):
    """格式化展示 OQMD 查询结果。"""
    entries = data.get("entries", [])
    total = data.get("total_count", len(entries))
    print(f"\n  共 {total} 条结果：")
    print("-" * 60)
    print(f"  {'材料名':<25s} {'形成能(eV)':<12s} {'带隙(eV)':<10s}")
    print("-" * 60)
    for entry in entries:
        name = entry.get("name", entry.get("composition", "N/A"))
        fe = entry.get("formation_energy", "N/A")
        bg = entry.get("band_gap", "N/A")
        fe_str = f"{fe:.3f}" if isinstance(fe, (int, float)) else str(fe)
        bg_str = f"{bg:.2f}" if isinstance(bg, (int, float)) else str(bg)
        print(f"  {name:<25s} {fe_str:<12s} {bg_str:<10s}")
    print("-" * 60)


def main():
    print("=" * 60)
    print("  ep33 - OQMD 与 NOMAD 数据库 REST API 查询")
    print("=" * 60)

    print("\n  OQMD (Open Quantum Materials Database)")
    print("  包含 >40 万条 DFT 计算结果，覆盖多种材料体系")

    # 演示 1：按化学式查询
    result1 = query_oqmd_by_formula("Bi2Te3")
    display_oqmd_results(result1)

    # 演示 2：按形成能筛选
    result2 = query_oqmd_by_formation_energy(energy_max=-0.1)
    display_oqmd_results(result2)

    print("\n  对比 MP 与 OQMD：")
    print("  - Materials Project: 更全面的材料属性，社区活跃")
    print("  - OQMD: 专注热力学稳定性，适合高通量筛选")
    print("  - NOMAD: 原始计算数据存档，适合方法复现")
    print("  - 实际项目建议多库交叉验证，提高数据可靠性")


if __name__ == "__main__":
    main()
