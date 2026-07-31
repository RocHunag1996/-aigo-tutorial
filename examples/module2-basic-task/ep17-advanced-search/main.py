"""
第17课：高级检索策略
演示布尔逻辑、字段过滤、引文网络追踪
"""
import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from sciverse_client import SciverseClient


def demo_field_filters(client: SciverseClient):
    """(1) title_contains + abstract_contains 组合"""
    print('[1] 组合过滤: 标题含 "graphene" 且 摘要含 "thermal conductivity"')
    print("-" * 50)
    res = client.search_papers("", title_contains="graphene",
                               abstract_contains="thermal conductivity",
                               year_from=2022, page_size=5)
    for i, p in enumerate(res.get("results", []), 1):
        print(f"  {i}. [{p.get('publication_published_year','')}] {p.get('title','')}")
    return res.get("results", [])


def demo_author_journal(client: SciverseClient):
    """(2) 按作者 + 期刊过滤"""
    print(f'\n[2] 作者含 "Goodenough" + 关键词 "sodium ion battery"')
    print("-" * 50)
    res = client.search_papers("sodium ion battery", authors=["Goodenough"],
                               year_from=2018, page_size=5)
    for i, p in enumerate(res.get("results", []), 1):
        authors = p.get("author", [])
        if isinstance(authors, list) and authors:
            if isinstance(authors[0], dict):
                authors = ", ".join(a.get("name", "") for a in authors[:3])
            else:
                authors = ", ".join(authors[:3])
        print(f"  {i}. [{p.get('publication_published_year','')}] {p.get('title','')}")
        print(f"     作者: {authors}")
    return res.get("results", [])


def demo_citation_chain(client: SciverseClient, paper_id: str):
    """(3) 用 list_paper_relations 追踪引用链"""
    print(f"\n[3] 引用追踪 (id: {paper_id[:30]}...)")
    print("-" * 50)
    for rel, label in [("CITATIONS", "被引"), ("REFERENCES", "参考文献")]:
        print(f"  [{label}]:")
        try:
            res = client.list_paper_relations(paper_id, rel, page_size=5)
            for i, p in enumerate(res.get("items", [])[:5], 1):
                print(f"    {i}. [{p.get('publication_published_year','')}] {p.get('title','')}")
        except Exception as e:
            print(f"    查询失败: {e}")


def main():
    print("=== 高级检索策略 ===\n")
    try:
        client = SciverseClient()
    except ValueError as e:
        print(f"请设置 SCIVERSE_API_KEY: {e}"); return

    p1 = demo_field_filters(client)
    p2 = demo_author_journal(client)
    target = (p1[0].get("unique_id") if p1 else
              p2[0].get("unique_id") if p2 else None)
    if target:
        demo_citation_chain(client, target)
    else:
        print("\n[3] 无可用论文 ID，跳过引用追踪")


if __name__ == "__main__":
    main()
