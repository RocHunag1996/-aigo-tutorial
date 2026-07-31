"""
第16课：语义检索 vs 关键词检索
对比 search_papers（关键词）和 semantic_search（语义）的结果差异
"""
import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from sciverse_client import SciverseClient

QUERY_KW = "machine learning predict thermoelectric properties"
QUERY_SEM = "如何用机器学习方法预测热电材料的热电优值ZT"


def main():
    print("=== 语义检索 vs 关键词检索 ===\n")
    try:
        client = SciverseClient()
    except ValueError as e:
        print(f"请设置 SCIVERSE_API_KEY: {e}"); return

    # 1. 关键词检索
    print(f'[1] 关键词: "{QUERY_KW}"')
    print("-" * 50)
    kw = client.search_papers(QUERY_KW, page_size=5).get("results", [])
    kw_titles = []
    for i, p in enumerate(kw, 1):
        t = p.get("title", "N/A")
        kw_titles.append(t.lower())
        print(f"  {i}. [{p.get('publication_published_year','')}] {t}")

    # 2. 语义检索
    print(f'\n[2] 语义: "{QUERY_SEM}"')
    print("-" * 50)
    sem = client.semantic_search(QUERY_SEM, top_k=5, mode="balanced").get("chunks", [])
    sem_titles = []
    for i, c in enumerate(sem, 1):
        t = c.get("title", "N/A")
        sem_titles.append(t.lower())
        print(f"  {i}. [score={c.get('score',0):.3f}] {t}")

    # 3. 对比
    print(f"\n[3] 结果对比")
    print("-" * 50)
    overlap = set(kw_titles) & set(sem_titles)
    print(f"关键词结果: {len(kw)}  语义结果: {len(sem)}  重叠: {len(overlap)}")
    only_kw = set(kw_titles) - set(sem_titles)
    only_sem = set(sem_titles) - set(kw_titles)
    if only_kw: print(f"仅关键词: {list(only_kw)[:2]}")
    if only_sem: print(f"仅语义:   {list(only_sem)[:2]}")
    print("\n结论:")
    print("  关键词检索: 精确匹配词汇，适合已知术语")
    print("  语义检索:   理解语义，能发现用词不同但相关的文献")


if __name__ == "__main__":
    main()
