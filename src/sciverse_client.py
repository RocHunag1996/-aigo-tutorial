"""
shared/sciverse_client.py
Sciverse 文献检索 API 同步封装（requests 版）。

覆盖 Sciverse 6 个工具接口：
  - search_papers        POST /meta-search        关键词 + 结构化过滤
  - semantic_search      POST /agentic-search     自然语言语义检索
  - list_catalog         GET  /meta-catalog       查看可用字段 schema
  - list_paper_relations POST /meta-paper-relations  引用关系分页查询
  - read_content         GET  /content            按字节区间读全文
  - get_resource         GET  /resource           取论文中嵌入的图片

用法：
    from sciverse_client import SciverseClient

    client = SciverseClient(api_key="sci_xxx")
    results = client.search_papers("thermoelectric materials", year_from=2023)
"""
from __future__ import annotations

import os
from typing import Optional

import requests

SCIVERSE_BASE_URL = "https://api.sciverse.space"


class SciverseClient:
    """Sciverse API 同步客户端。"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = SCIVERSE_BASE_URL,
        timeout: int = 30,
    ):
        if api_key is None:
            api_key = os.environ.get("SCIVERSE_API_KEY", "")
        if not api_key:
            raise ValueError(
                "请设置 SCIVERSE_API_KEY 环境变量或传入 api_key 参数"
            )
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        })

    # ── 1. search_papers ──────────────────────────────────

    def search_papers(
        self,
        query: str = "",
        *,
        title_contains: Optional[str] = None,
        abstract_contains: Optional[str] = None,
        authors: Optional[list] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        journals: Optional[list] = None,
        subjects: Optional[list] = None,
        sort_by_year: str = "none",
        freshness_boost: str = "NONE",
        page: int = 1,
        page_size: int = 10,
    ) -> dict:
        """
        关键词 + 结构化条件检索论文。

        Parameters
        ----------
        query : str
            BM25 关键词，匹配标题/摘要/期刊名。留空则纯靠过滤。
        title_contains : str
            标题中必须包含的词。
        abstract_contains : str
            摘要中必须包含的词。
        authors : list[str]
            作者名列表，任一命中即可。
        year_from, year_to : int
            发表年份范围。
        journals : list[str]
            期刊名列表。
        subjects : list[str]
            学科分类，如 ["Materials Science"]。
        sort_by_year : str
            "desc" / "asc" / "none"。
        freshness_boost : str
            "NONE" / "MILD"（近10年加权）/ "STRONG"（近3年加权）。
        page, page_size : int
            分页参数。

        Returns
        -------
        dict
            包含 results 列表，每条含 unique_id, title, author, abstract 等。
        """
        # 构建 canonical 格式（filters + sort）
        payload = {}

        filters = []
        if title_contains:
            filters.append({
                "field": "title",
                "operator": "FILTER_OP_CONTAINS",
                "value": title_contains,
            })
        # abstract 字段不支持 FILTER_OP_CONTAINS，改为合并到 query（BM25 全文搜索覆盖摘要）
        if abstract_contains:
            if query:
                query = f"{query} {abstract_contains}"
            else:
                query = abstract_contains
        if query:
            payload["query"] = query
        if authors:
            filters.append({
                "field": "author",
                "operator": "FILTER_OP_IN",
                "value": list(authors),
            })
        if year_from is not None:
            filters.append({
                "field": "publication_published_year",
                "operator": "FILTER_OP_GTE",
                "value": year_from,
            })
        if year_to is not None:
            filters.append({
                "field": "publication_published_year",
                "operator": "FILTER_OP_LTE",
                "value": year_to,
            })
        if journals:
            filters.append({
                "field": "publication_venue_name_unified",
                "operator": "FILTER_OP_IN",
                "value": list(journals),
            })
        if subjects:
            filters.append({
                "field": "subjects",
                "operator": "FILTER_OP_IN",
                "value": list(subjects),
            })
        if filters:
            payload["filters"] = filters

        # 排序
        sort = []
        if sort_by_year in ("desc", "asc"):
            sort.append({
                "field": "publication_published_year",
                "order": "SORT_ORDER_DESC" if sort_by_year == "desc" else "SORT_ORDER_ASC",
            })
        if sort:
            payload["sort"] = sort

        # 新鲜度加权
        if freshness_boost != "NONE" and query:
            payload["freshness_boost"] = freshness_boost

        payload["page"] = page
        payload["page_size"] = page_size

        resp = self.session.post(
            f"{self.base_url}/meta-search", json=payload, timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json()

    # ── 2. semantic_search ────────────────────────────────

    def semantic_search(
        self,
        query: str,
        *,
        top_k: int = 10,
        mode: str = "balanced",
        source_types: Optional[list] = None,
    ) -> dict:
        """
        自然语言语义检索，返回相关文献片段（chunk）。

        Parameters
        ----------
        query : str
            自然语言查询，1-200 字最佳。
        top_k : int
            返回结果数，1-30。
        mode : str
            "fast"（~200ms）/ "balanced"（~600ms）/ "quality"（~2-4s）。
        source_types : list[str]
            来源类型过滤，如 ["pdf"] 或 ["web"]。

        Returns
        -------
        dict
            包含 chunks 列表，每条含 chunk_id, doc_id, chunk, score, title 等。
        """
        payload = {"query": query, "top_k": top_k, "mode": mode}
        if source_types:
            payload["source_types"] = source_types

        resp = self.session.post(
            f"{self.base_url}/agentic-search", json=payload, timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json()

    # ── 3. list_catalog ───────────────────────────────────

    def list_catalog(
        self,
        *,
        collection: str = "papers",
        include_sample_values: bool = False,
        include_field_stats: bool = False,
    ) -> dict:
        """
        查看可检索字段的 schema（字段名、类型、能否过滤/排序等）。

        Parameters
        ----------
        collection : str
            "papers" / "authors" / "sources"。
        include_sample_values : bool
            是否返回枚举字段的样本值。
        include_field_stats : bool
            是否返回字段统计信息。

        Returns
        -------
        dict
            包含 catalog 字段列表。
        """
        params = {
            "collection": collection,
            "include_sample_values": str(include_sample_values).lower(),
        }
        if include_field_stats:
            params["include_field_stats"] = "true"

        resp = self.session.get(
            f"{self.base_url}/meta-catalog", params=params, timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json()

    # ── 4. list_paper_relations ───────────────────────────

    def list_paper_relations(
        self,
        unique_id: str,
        relation: str,
        *,
        page: int = 1,
        page_size: int = 25,
    ) -> dict:
        """
        分页查询某篇论文的引用关系。

        Parameters
        ----------
        unique_id : str
            论文 unique_id（来自 search_papers 结果）。
        relation : str
            "CITATIONS"（被引）/ "REFERENCES"（参考文献）/ "RELATED_WORKS"。
        page, page_size : int
            分页参数。

        Returns
        -------
        dict
            包含关系论文列表。
        """
        payload = {
            "unique_id": unique_id,
            "relation": relation,
            "page": page,
            "page_size": page_size,
        }
        resp = self.session.post(
            f"{self.base_url}/meta-paper-relations", json=payload, timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json()

    # ── 5. read_content ───────────────────────────────────

    def read_content(
        self,
        doc_id: str,
        *,
        offset: int = 0,
        limit: int = 4096,
    ) -> dict:
        """
        按字节区间读取文献原文片段。

        Parameters
        ----------
        doc_id : str
            文献 ID（来自 search_papers / semantic_search）。
        offset : int
            起始字节偏移。
        limit : int
            读取字节数，最大 16384。

        Returns
        -------
        dict
            包含 text, bytes_returned, next_offset, has_more。
        """
        params = {"doc_id": doc_id, "offset": offset, "limit": limit}
        resp = self.session.get(
            f"{self.base_url}/content", params=params, timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json()

    # ── 6. get_resource ───────────────────────────────────

    def get_resource(self, file_name: str) -> tuple:
        """
        获取论文中嵌入的图片二进制数据。

        Parameters
        ----------
        file_name : str
            图片文件名（来自 read_content 返回的 Markdown 中的图片引用）。

        Returns
        -------
        tuple(bytes, str)
            (图片二进制数据, MIME 类型)
        """
        resp = self.session.get(
            f"{self.base_url}/resource",
            params={"file_name": file_name},
            headers={"accept": "image/*"},
            timeout=self.timeout,
        )
        resp.raise_for_status()
        mime = resp.headers.get("content-type", "application/octet-stream").split(";")[0].strip()
        return resp.content, mime


# ── 便捷函数（不实例化也能用）──────────────────────────────

_default_client: Optional[SciverseClient] = None


def _get_client() -> SciverseClient:
    global _default_client
    if _default_client is None:
        _default_client = SciverseClient()
    return _default_client


def search_papers(query: str, **kwargs) -> dict:
    """便捷函数：关键词检索论文。"""
    return _get_client().search_papers(query, **kwargs)


def semantic_search(query: str, **kwargs) -> dict:
    """便捷函数：语义检索。"""
    return _get_client().semantic_search(query, **kwargs)


if __name__ == "__main__":
    # 快速测试（需要设置 SCIVERSE_API_KEY 环境变量）
    import json

    client = SciverseClient()

    print("=== 关键词检索 ===")
    results = client.search_papers(
        "thermoelectric materials machine learning",
        year_from=2023,
        page_size=3,
    )
    for paper in results.get("results", [])[:3]:
        title = paper.get("title", "N/A")
        year = paper.get("publication_published_year", "N/A")
        print(f"  - [{year}] {title}")

    print("\n=== 语义检索 ===")
    chunks = client.semantic_search(
        "如何用机器学习预测热电材料的优值",
        top_k=3,
        mode="fast",
    )
    for chunk in chunks.get("chunks", [])[:3]:
        print(f"  - {chunk.get('title', 'N/A')} (score: {chunk.get('score', 0):.3f})")
