"""
第15课：Sciverse API 上手
完整上手指南：初始化、关键词检索、带过滤检索、查看结果结构
"""
import sys
import os
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from sciverse_client import SciverseClient


def main():
    print("=== Sciverse API 上手指南 ===\n")

    # (1) 初始化客户端
    print("[1] 初始化客户端")
    try:
        client = SciverseClient()
        print("    客户端初始化成功\n")
    except ValueError as e:
        print(f"    失败: {e}")
        return

    # (2) 简单关键词检索
    print("[2] 关键词检索")
    print("-" * 40)
    results = client.search_papers("machine learning thermoelectric", page_size=5)
    papers = results.get("results", [])
    print(f"命中 {results.get('total', len(papers))} 篇，展示前 {len(papers)} 篇:\n")

    for i, p in enumerate(papers, 1):
        title = p.get("title", "N/A")
        year = p.get("publication_published_year", "N/A")
        authors = p.get("author", [])
        if isinstance(authors, list) and authors:
            if isinstance(authors[0], dict):
                authors = ", ".join(a.get("name", "") for a in authors[:3])
            else:
                authors = ", ".join(authors[:3])
        print(f"  {i}. [{year}] {title}")
        print(f"     作者: {authors}")

    # (3) 带过滤条件的检索
    print(f"\n[3] 带过滤条件的检索")
    print("-" * 40)
    print("条件: 2023-2024年, 期刊 Nature Energy")
    results2 = client.search_papers(
        "battery",
        year_from=2023,
        year_to=2024,
        journals=["Nature Energy"],
        page_size=5,
    )
    papers2 = results2.get("results", [])
    print(f"命中 {results2.get('total', len(papers2))} 篇:\n")

    for i, p in enumerate(papers2, 1):
        title = p.get("title", "N/A")
        year = p.get("publication_published_year", "N/A")
        venue = p.get("publication_venue_name", p.get("venue", "N/A"))
        print(f"  {i}. [{year}] {title}")
        print(f"     期刊: {venue}")

    # (4) 查看结果结构
    print(f"\n[4] 结果数据结构")
    print("-" * 40)
    if papers:
        sample = papers[0]
        print("单篇论文的字段:")
        for key, val in sample.items():
            val_str = str(val)[:80]
            print(f"  {key}: {val_str}")


if __name__ == "__main__":
    main()
