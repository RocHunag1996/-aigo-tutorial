"""
AIGO 教程系列 - 路线 C·合成路线与工艺设计
ep57-synthesis-kb: 合成知识库构建
用 SQLite 存储和查询从文献中提取的合成条件
"""

import sqlite3
import json
import os
import tempfile


def create_database(db_path: str) -> sqlite3.Connection:
    """创建合成条件数据库，定义表结构"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 合成条件主表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS synthesis_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_name TEXT NOT NULL,
            synthesis_method TEXT,
            temperature_c REAL,
            time_hours REAL,
            atmosphere TEXT,
            heating_rate REAL,
            solvent TEXT,
            ph_value REAL,
            post_treatment TEXT,
            source_paper TEXT,
            confidence REAL DEFAULT 1.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 前驱体表（一对多关系）
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS precursors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record_id INTEGER,
            precursor_name TEXT NOT NULL,
            FOREIGN KEY (record_id) REFERENCES synthesis_records(id)
        )
    """)

    conn.commit()
    return conn


def insert_record(conn: sqlite3.Connection, record: dict) -> int:
    """插入一条合成记录"""
    cursor = conn.cursor()

    # 插入主记录
    cursor.execute("""
        INSERT INTO synthesis_records
        (material_name, synthesis_method, temperature_c, time_hours,
         atmosphere, heating_rate, solvent, ph_value, post_treatment,
         source_paper, confidence)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record.get("material_name"),
        record.get("synthesis_method"),
        record.get("temperature_c"),
        record.get("time_hours"),
        record.get("atmosphere"),
        record.get("heating_rate"),
        record.get("solvent"),
        record.get("ph_value"),
        record.get("post_treatment"),
        record.get("source_paper"),
        record.get("confidence", 1.0),
    ))

    record_id = cursor.lastrowid

    # 插入前驱体
    precursors = record.get("precursors", [])
    if isinstance(precursors, str):
        precursors = [precursors]
    for p in precursors:
        cursor.execute(
            "INSERT INTO precursors (record_id, precursor_name) VALUES (?, ?)",
            (record_id, p)
        )

    conn.commit()
    return record_id


def query_by_method(conn: sqlite3.Connection, method: str) -> list[dict]:
    """按合成方法查询记录"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM synthesis_records
        WHERE synthesis_method LIKE ?
        ORDER BY created_at DESC
    """, (f"%{method}%",))

    columns = [desc[0] for desc in cursor.description]
    results = []
    for row in cursor.fetchall():
        record = dict(zip(columns, row))
        # 查询对应前驱体
        cursor2 = conn.cursor()
        cursor2.execute(
            "SELECT precursor_name FROM precursors WHERE record_id = ?",
            (record["id"],)
        )
        record["precursors"] = [r[0] for r in cursor2.fetchall()]
        results.append(record)

    return results


def query_by_material(conn: sqlite3.Connection, keyword: str) -> list[dict]:
    """按材料名称关键词查询"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT material_name, synthesis_method, temperature_c,
               time_hours, atmosphere, source_paper
        FROM synthesis_records
        WHERE material_name LIKE ?
    """, (f"%{keyword}%",))

    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def print_statistics(conn: sqlite3.Connection):
    """打印知识库统计信息"""
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM synthesis_records")
    total = cursor.fetchone()[0]

    print(f"\n知识库统计：共 {total} 条合成记录")
    print("-" * 40)

    # 按合成方法统计
    cursor.execute("""
        SELECT synthesis_method, COUNT(*) as cnt
        FROM synthesis_records
        GROUP BY synthesis_method
        ORDER BY cnt DESC
    """)
    print("\n按合成方法统计：")
    for method, count in cursor.fetchall():
        print(f"  {method or '未知':20s} | {count} 条")

    # 温度分布
    cursor.execute("""
        SELECT
            CASE
                WHEN temperature_c < 500 THEN '< 500°C'
                WHEN temperature_c < 1000 THEN '500-1000°C'
                ELSE '> 1000°C'
            END as temp_range,
            COUNT(*) as cnt
        FROM synthesis_records
        WHERE temperature_c IS NOT NULL
        GROUP BY temp_range
    """)
    print("\n温度分布：")
    for temp_range, count in cursor.fetchall():
        bar = "█" * count
        print(f"  {temp_range:12s} | {bar} ({count})")


def main():
    print("ep57 - 合成知识库构建")
    print("=" * 60)

    # 在临时目录创建演示数据库
    db_path = os.path.join(tempfile.gettempdir(), "synthesis_kb_demo.db")
    print(f"\n数据库路径: {db_path}")

    conn = create_database(db_path)

    # 插入示例数据（模拟 ep56 提取结果）
    demo_records = [
        {
            "material_name": "Li7La3Zr2O12 (LLZO)",
            "synthesis_method": "溶胶-凝胶法",
            "precursors": ["LiNO3", "La(NO3)3", "Zr(O-nBu)4"],
            "temperature_c": 750,
            "time_hours": 6,
            "atmosphere": "空气",
            "heating_rate": 5.0,
            "source_paper": "Zhang et al., J. Power Sources, 2023",
        },
        {
            "material_name": "Li6.4La3Zr1.4Ta0.6O12",
            "synthesis_method": "固相法",
            "precursors": ["Li2CO3", "La2O3", "ZrO2", "Ta2O5"],
            "temperature_c": 1050,
            "time_hours": 12,
            "atmosphere": "空气",
            "source_paper": "Wang et al., Chem. Mater., 2022",
        },
        {
            "material_name": "Li1.3Al0.3Ti1.7(PO4)3",
            "synthesis_method": "溶胶-凝胶法",
            "precursors": ["LiOH", "Al(NO3)3", "Ti(OC4H9)4", "NH4H2PO4"],
            "temperature_c": 800,
            "time_hours": 8,
            "atmosphere": "空气",
            "source_paper": "Liu et al., ACS Appl. Mater. Interfaces, 2023",
        },
        {
            "material_name": "BaTiO3",
            "synthesis_method": "水热法",
            "precursors": ["Ba(OH)2", "TiCl4"],
            "temperature_c": 200,
            "time_hours": 24,
            "atmosphere": "氮气",
            "ph_value": 14.0,
            "source_paper": "Kim et al., J. Am. Ceram. Soc., 2021",
        },
    ]

    print("\n插入示例数据...")
    for record in demo_records:
        rid = insert_record(conn, record)
        print(f"  [✓] {record['material_name']} (id={rid})")

    # 查询演示
    print("\n" + "-" * 40)
    print("查询：溶胶-凝胶法合成的材料")
    print("-" * 40)
    sol_gel = query_by_method(conn, "溶胶-凝胶")
    for r in sol_gel:
        print(f"  - {r['material_name']} | {r['temperature_c']}°C | {r['time_hours']}h")

    print("\n" + "-" * 40)
    print("查询：含 Li 的材料")
    print("-" * 40)
    li_records = query_by_material(conn, "Li")
    for r in li_records:
        print(f"  - {r['material_name']} | {r['synthesis_method']}")

    # 统计
    print_statistics(conn)

    conn.close()
    # 清理临时文件
    os.remove(db_path)
    print(f"\n演示完成，已清理临时数据库。")


if __name__ == "__main__":
    main()
