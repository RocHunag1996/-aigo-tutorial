"""
第14课：Sciverse 是什么
演示 Sciverse 的基本功能：查看字段、检索论文、了解数据规模
"""
import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from sciverse_client import SciverseClient


def main():
    print("=== Sciverse 平台介绍 ===\n")

    # 初始化客户端（从环境变量 SCIVERSE_API_KEY 读取）
    try:
        client = SciverseClient()
    except ValueError as e:
        print(f"请设置环境变量 SCIVERSE_API_KEY")
        print(f"  {e}")
        return

    # 1. 查看可用字段 schema
    print("[1] 查看数据目录 (catalog)")
    print("-" * 40)
    try:
        catalog = client.list_catalog(collection="papers", include_sample_values=True)
        fields = catalog.get("catalog", catalog.get("fields", []))
        print(f"可用字段数: {len(fields)}")
        print("部分字段:")
        for f in fields[:10]:
            name = f.get("name", f.get("field", "unknown"))
            ftype = f.get("type", "unknown")
            print(f"  - {name} ({ftype})")
        if len(fields) > 10:
            print(f"  ... 还有 {len(fields)-10} 个字段")
    except Exception as e:
        print(f"获取 catalog 失败: {e}")

    # 2. 做一次简单检索
    print(f"\n[2] 关键词检索示例")
    print("-" * 40)
    query = "thermoelectric materials"
    print(f"查询: {query}")
    try:
        results = client.search_papers(query, page_size=5)
        papers = results.get("results", [])
        total = results.get("total", len(papers))
        print(f"命中: {total} 篇\n")

        for i, paper in enumerate(papers, 1):
            title = paper.get("title", "N/A")
            year = paper.get("publication_published_year", "N/A")
            authors = paper.get("author", [])
            if isinstance(authors, list) and authors:
                if isinstance(authors[0], dict):
                    authors = ", ".join(a.get("name", "") for a in authors[:3])
                else:
                    authors = ", ".join(authors[:3])
                if len(paper.get("author", [])) > 3:
                    authors += " et al."
            print(f"  {i}. [{year}] {title}")
            print(f"     作者: {authors}")
    except Exception as e:
        print(f"检索失败: {e}")

    # 3. 展示数据规模
    print(f"\n[3] 数据规模")
    print("-" * 40)
    print("Sciverse 是一个面向科研文献的检索平台，")
    print("涵盖多个学科领域的论文、作者和期刊数据。")
    print("支持关键词检索、语义检索、引用关系查询等功能。")


if __name__ == "__main__":
    main()
