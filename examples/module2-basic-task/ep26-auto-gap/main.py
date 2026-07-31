"""
AIGO 教程系列 - 基本任务·文献调研 Agent
ep26-auto-gap: 基于知识库的自动化 Gap 发现

从 SQLite 知识库中统计数据，找出性能覆盖盲区（如某材料体系缺少某温度
范围的数据）、成分-性能地图空白区。用简单统计方法。
"""

from __future__ import annotations

import sqlite3
import os
import re
from collections import defaultdict
from typing import Optional

DB_PATH = "materials_kb.db"


def create_demo_db():
    """创建带更多数据的演示数据库，用于 Gap 发现。"""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    conn.executescript("""
        CREATE TABLE materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, formula TEXT, category TEXT, source_paper TEXT
        );
        CREATE TABLE properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id INTEGER REFERENCES materials(id),
            property_name TEXT, value REAL, unit TEXT, condition TEXT
        );
        CREATE TABLE methods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id INTEGER REFERENCES materials(id),
            method_name TEXT, parameters TEXT
        );
    """)

    # 插入多种材料在不同条件下的性能数据
    materials = [
        ("LiCoO2", "LiCoO2", "正极", "P1"),
        ("LiCoO2", "LiCoO2", "正极", "P2"),
        ("LiFePO4", "LiFePO4", "正极", "P3"),
        ("LiFePO4", "LiFePO4", "正极", "P4"),
        ("NMC811", "LiNi0.8Mn0.1Co0.1O2", "正极", "P5"),
        ("NMC811", "LiNi0.8Mn0.1Co0.1O2", "正极", "P6"),
        ("LLZO", "Li7La3Zr2O12", "电解质", "P7"),
    ]
    conn.executemany(
        "INSERT INTO materials (name, formula, category, source_paper) VALUES (?,?,?,?)",
        materials,
    )

    # 性能数据：包含温度条件，便于发现温度区间盲区
    properties = [
        # LiCoO2: 只有 25°C 数据
        (1, "比容量", 180, "mAh/g", "25°C, 0.1C"),
        (1, "比容量", 170, "mAh/g", "25°C, 0.5C"),
        (2, "比容量", 175, "mAh/g", "25°C, 1C"),
        # LiFePO4: 有 25°C 和 -10°C 数据
        (3, "比容量", 160, "mAh/g", "25°C, 1C"),
        (4, "比容量", 95,  "mAh/g", "-10°C, 0.5C"),
        (4, "比容量", 140, "mAh/g", "-10°C, 0.2C"),
        # NMC811: 只有高温数据
        (5, "比容量", 200, "mAh/g", "45°C, 1C"),
        (6, "比容量", 195, "mAh/g", "45°C, 0.5C"),
        (6, "循环寿命", 300, "次", "45°C, 80%保持率"),
        # LLZO: 只有室温离子电导率
        (7, "离子电导率", 1.2, "mS/cm", "25°C"),
    ]
    conn.executemany(
        "INSERT INTO properties (material_id, property_name, value, unit, condition) "
        "VALUES (?,?,?,?,?)",
        properties,
    )
    conn.commit()
    conn.close()


def extract_temperature(condition: str) -> Optional[float]:
    """从测试条件字符串中提取温度数值。"""
    match = re.search(r"(-?\d+)\s*°?\s*C", condition)
    return float(match.group(1)) if match else None


def find_temperature_gaps(conn: sqlite3.Connection) -> list[dict]:
    """
    发现温度覆盖盲区：
    对每种材料，统计已有数据的温度范围，找出缺失的温度区间。
    """
    gaps = []
    rows = conn.execute("""
        SELECT m.name, m.formula, p.property_name, p.condition
        FROM properties p JOIN materials m ON p.material_id = m.id
    """).fetchall()

    # 按材料分组，收集温度数据点
    mat_temps: dict[str, list[float]] = defaultdict(list)
    for name, formula, prop_name, condition in rows:
        temp = extract_temperature(condition)
        if temp is not None:
            key = f"{name}({formula})"
            mat_temps[key].append(temp)

    # 定义关注的温度区间
    temp_ranges = {"低温(<0°C)": (-40, 0), "室温(0-40°C)": (0, 40), "高温(>40°C)": (40, 80)}

    for mat, temps in mat_temps.items():
        t_min, t_max = min(temps), max(temps)
        covered = set()
        for range_name, (lo, hi) in temp_ranges.items():
            if any(lo <= t <= hi for t in temps):
                covered.add(range_name)

        missing = set(temp_ranges.keys()) - covered
        if missing:
            gaps.append({
                "material": mat,
                "temp_range": f"{t_min}°C ~ {t_max}°C",
                "covered": list(covered),
                "missing": list(missing),
            })

    return gaps


def find_property_coverage(conn: sqlite3.Connection) -> list[dict]:
    """统计每种材料已测试的性能指标，找出缺失的常见指标。"""
    expected_props = {"比容量", "循环寿命", "离子电导率", "倍率性能", "阻抗"}

    rows = conn.execute("""
        SELECT m.name, m.formula, p.property_name
        FROM properties p JOIN materials m ON p.material_id = m.id
    """).fetchall()

    mat_props: dict[str, set[str]] = defaultdict(set)
    for name, formula, prop_name in rows:
        mat_props[f"{name}({formula})"].add(prop_name)

    gaps = []
    for mat, props in mat_props.items():
        missing = expected_props - props
        if missing:
            gaps.append({
                "material": mat,
                "covered": sorted(props),
                "missing": sorted(missing),
            })
    return gaps


def main():
    # 1. 创建演示数据库
    create_demo_db()
    print(f"演示数据库已创建: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)

    # 2. 温度覆盖盲区
    print("\n" + "=" * 55)
    print("  温度覆盖盲区分析")
    print("=" * 55)
    temp_gaps = find_temperature_gaps(conn)
    for g in temp_gaps:
        print(f"\n  材料: {g['material']}")
        print(f"  已有温度范围: {g['temp_range']}")
        print(f"  已覆盖区间: {', '.join(g['covered'])}")
        print(f"  缺失区间: {', '.join(g['missing'])}")

    # 3. 性能指标覆盖率
    print("\n" + "=" * 55)
    print("  性能指标覆盖率分析")
    print("=" * 55)
    prop_gaps = find_property_coverage(conn)
    for g in prop_gaps:
        print(f"\n  材料: {g['material']}")
        print(f"  已测试: {', '.join(g['covered'])}")
        print(f"  缺失: {', '.join(g['missing'])}")

    conn.close()
    print("\n\n共发现 {} 个温度盲区, {} 个性能指标缺口".format(
        len(temp_gaps), len(prop_gaps)))


if __name__ == "__main__":
    main()
