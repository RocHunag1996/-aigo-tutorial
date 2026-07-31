"""
AIGO 教程系列 - 路线 A·构效关系发现
ep32-materials-project: Materials Project API 数据查询

演示用 requests 调用 MP REST API，查询热电材料数据。
API key 从环境变量 MP_API_KEY 读取。
文档：https://api.materialsproject.org/docs/
"""
import os
import requests

MP_BASE_URL = "https://api.materialsproject.org"


def get_headers():
    """构造请求头，API key 从环境变量读取。"""
    api_key = os.environ.get("MP_API_KEY", "")
    if not api_key:
        print("  [!] 未设置 MP_API_KEY 环境变量，将使用演示数据")
        return None
    return {"X-API-Key": api_key}


def query_thermoelectric_materials(headers, formula="Bi2Te3"):
    """
    查询指定化学式的材料性能数据。
    使用 MP API v2 /materials/summary 端点。
    """
    url = f"{MP_BASE_URL}/materials/summary"
    params = {
        "formula": formula,
        "fields": [
            "material_id", "formula_pretty", "band_gap",
            "formation_energy_per_atom", "elements",
        ]
    }

    print(f"\n  查询化学式: {formula}")
    print(f"  端点: {url}")

    if headers is None:
        return _demo_response(formula)

    resp = requests.get(url, headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def query_by_bandgap(headers, bg_min=0.5, bg_max=1.5, limit=5):
    """
    按带隙范围查询材料 -- 热电材料通常需要窄带隙。
    """
    url = f"{MP_BASE_URL}/materials/summary"
    params = {
        "band_gap": f"{bg_min}..{bg_max}",
        "fields": ["material_id", "formula_pretty", "band_gap",
                    "formation_energy_per_atom"],
        "_limit": limit,
    }

    print(f"\n  按带隙范围 [{bg_min}, {bg_max}] eV 查询（限 {limit} 条）")

    if headers is None:
        return _demo_bandgap_query()

    resp = requests.get(url, headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def _demo_response(formula):
    """无 API key 时的演示数据。"""
    return {
        "data": [
            {
                "material_id": "mp-1782",
                "formula_pretty": formula,
                "band_gap": 0.33,
                "formation_energy_per_atom": -0.18,
                "elements": ["Bi", "Te"],
            }
        ],
        "total_doc_count": 1,
    }


def _demo_bandgap_query():
    """无 API key 时的带隙查询演示数据。"""
    return {
        "data": [
            {"material_id": "mp-1782", "formula_pretty": "Bi2Te3",
             "band_gap": 0.33, "formation_energy_per_atom": -0.18},
            {"material_id": "mp-20671", "formula_pretty": "PbTe",
             "band_gap": 0.80, "formation_energy_per_atom": -0.25},
            {"material_id": "mp-19132", "formula_pretty": "SiGe",
             "band_gap": 0.62, "formation_energy_per_atom": -0.05},
        ],
        "total_doc_count": 3,
    }


def display_results(result):
    """格式化展示查询结果。"""
    docs = result.get("data", [])
    total = result.get("total_doc_count", len(docs))
    print(f"\n  共找到 {total} 条结果，展示前 {len(docs)} 条：")
    print("-" * 60)
    for doc in docs:
        mid = doc.get("material_id", "N/A")
        formula = doc.get("formula_pretty", "N/A")
        bg = doc.get("band_gap", "N/A")
        fe = doc.get("formation_energy_per_atom", "N/A")
        print(f"  {mid:>12s} | {formula:<10s} | 带隙={bg} eV | 形成能={fe} eV/atom")
    print("-" * 60)


def main():
    print("=" * 60)
    print("  ep32 - Materials Project API 数据查询")
    print("=" * 60)

    headers = get_headers()

    # 演示 1：按化学式查询
    result1 = query_thermoelectric_materials(headers, "Bi2Te3")
    display_results(result1)

    # 演示 2：按带隙范围查询
    result2 = query_by_bandgap(headers, bg_min=0.3, bg_max=1.0, limit=5)
    display_results(result2)

    print("\n  提示：")
    print("  - 注册 MP 账号可免费获取 API key: https://materialsproject.org/")
    print("  - 设置环境变量: export MP_API_KEY='your_key_here'")
    print("  - MP API 支持丰富的过滤条件，详见官方文档")


if __name__ == "__main__":
    main()
