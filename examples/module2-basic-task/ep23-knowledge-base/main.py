"""
AIGO 教程系列 - 基本任务·文献调研 Agent
ep23-knowledge-base: 构建知识库

把抽取结果存入 SQLite 数据库。建表（materials, properties, methods），
插入数据，演示按材料/性能/方法多维查询。用 sqlite3 标准库。
"""

import sqlite3
import json

DB_PATH = "materials_kb.db"


def create_tables(conn: sqlite3.Connection):
    """创建知识库所需的三张表。"""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS materials (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            formula TEXT,
            category TEXT,
            source_paper TEXT
        );
        CREATE TABLE IF NOT EXISTS properties (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id   INTEGER REFERENCES materials(id),
            property_name TEXT NOT NULL,
            value         REAL,
            unit          TEXT,
            condition     TEXT
        );
        CREATE TABLE IF NOT EXISTS methods (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id INTEGER REFERENCES materials(id),
            method_name TEXT NOT NULL,
            parameters  TEXT
        );
    """)
    conn.commit()


def insert_sample_data(conn: sqlite3.Connection):
    """插入示例数据，模拟从论文中抽取的知识。"""
    # 材料数据
    materials = [
        ("LiCoO2", "LiCoO2", "正极材料", "Paper_A"),
        ("LiFePO4", "LiFePO4", "正极材料", "Paper_A"),
        ("LLZO", "Li7La3Zr2O12", "固态电解质", "Paper_B"),
        ("石墨", "C", "负极材料", "Paper_C"),
    ]
    conn.executemany(
        "INSERT INTO materials (name, formula, category, source_paper) VALUES (?, ?, ?, ?)",
        materials,
    )

    # 性能数据
    properties = [
        (1, "比容量", 180.0, "mAh/g", "0.1C, 25°C"),
        (1, "循环寿命", 500.0, "次", "80% 保持率"),
        (2, "比容量", 155.0, "mAh/g", "0.5C, 25°C"),
        (3, "离子电导率", 1.2, "mS/cm", "25°C"),
        (4, "比容量", 350.0, "mAh/g", "0.1C"),
    ]
    conn.executemany(
        "INSERT INTO properties (material_id, property_name, value, unit, condition) "
        "VALUES (?, ?, ?, ?, ?)",
        properties,
    )

    # 方法数据
    methods = [
        (1, "溶胶-凝胶法", "700°C, 12h, 空气"),
        (2, "固相反应法", "700°C, 24h, 氮气"),
        (3, "固相反应法", "1100°C, 6h, 空气"),
        (4, "化学气相沉积", "900°C, 低压"),
    ]
    conn.executemany(
        "INSERT INTO methods (material_id, method_name, parameters) VALUES (?, ?, ?)",
        methods,
    )
    conn.commit()


def query_by_material(conn: sqlite3.Connection, name: str):
    """按材料名查询所有相关性能和合成方法。"""
    print(f"\n--- 按材料查询: {name} ---")
    row = conn.execute(
        "SELECT id, formula, category FROM materials WHERE name LIKE ?",
        (f"%{name}%",),
    ).fetchone()
    if not row:
        print("  未找到该材料")
        return

    mat_id, formula, category = row
    print(f"  材料: {name} ({formula}), 类别: {category}")

    # 查询性能
    props = conn.execute(
        "SELECT property_name, value, unit, condition FROM properties WHERE material_id = ?",
        (mat_id,),
    ).fetchall()
    print("  性能指标:")
    for p in props:
        print(f"    - {p[0]}: {p[1]} {p[2]} [{p[3]}]")

    # 查询方法
    meths = conn.execute(
        "SELECT method_name, parameters FROM methods WHERE material_id = ?",
        (mat_id,),
    ).fetchall()
    print("  合成方法:")
    for m in meths:
        print(f"    - {m[0]} ({m[1]})")


def query_by_property(conn: sqlite3.Connection, prop_name: str, min_val: float = None):
    """按性能指标查询，可选最小值过滤。"""
    print(f"\n--- 按性能查询: {prop_name} (>= {min_val}) ---")
    sql = ("SELECT m.name, m.formula, p.property_name, p.value, p.unit "
           "FROM properties p JOIN materials m ON p.material_id = m.id "
           "WHERE p.property_name LIKE ?")
    params = [f"%{prop_name}%"]
    if min_val is not None:
        sql += " AND p.value >= ?"
        params.append(min_val)

    rows = conn.execute(sql, params).fetchall()
    for r in rows:
        print(f"  {r[0]} ({r[1]}): {r[2]} = {r[3]} {r[4]}")


def query_by_method(conn: sqlite3.Connection, method_name: str):
    """按合成方法查询所有相关材料。"""
    print(f"\n--- 按方法查询: {method_name} ---")
    rows = conn.execute(
        "SELECT m.name, m.formula, mt.method_name, mt.parameters "
        "FROM methods mt JOIN materials m ON mt.material_id = m.id "
        "WHERE mt.method_name LIKE ?",
        (f"%{method_name}%",),
    ).fetchall()
    for r in rows:
        print(f"  {r[0]} ({r[1]}): {r[2]}, 参数: {r[3]}")


def main():
    # 连接数据库（每次运行重建，保证示例可复现）
    import os
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)
    insert_sample_data(conn)
    print(f"知识库已创建: {DB_PATH}")

    # 演示多维查询
    query_by_material(conn, "LiCoO2")
    query_by_property(conn, "比容量", min_val=150)
    query_by_method(conn, "固相反应")

    # 统计概览
    print("\n--- 知识库统计 ---")
    n_mat = conn.execute("SELECT COUNT(*) FROM materials").fetchone()[0]
    n_prop = conn.execute("SELECT COUNT(*) FROM properties").fetchone()[0]
    n_meth = conn.execute("SELECT COUNT(*) FROM methods").fetchone()[0]
    print(f"  材料数: {n_mat}, 性能记录数: {n_prop}, 方法记录数: {n_meth}")

    conn.close()


if __name__ == "__main__":
    main()
