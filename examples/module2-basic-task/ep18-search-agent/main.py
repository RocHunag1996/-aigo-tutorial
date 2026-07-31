"""
第18课：构建检索 Agent
将 Sciverse API 封装成 Agent，用 LLM 自动决策调用哪个接口
"""
import sys, os, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from sciverse_client import SciverseClient
from llm_call import llm_call_json

SYSTEM_PROMPT = """你是文献检索助手。根据用户问题选择工具并返回 JSON。
工具:
1. search_papers: 关键词检索，参数: query, year_from, year_to, journals(list), authors(list), page_size
2. semantic_search: 语义检索，参数: query, top_k, mode(fast/balanced/quality)
3. list_paper_relations: 引用关系，参数: unique_id, relation(CITATIONS/REFERENCES)
返回: {"tool": "工具名", "params": {...}, "reason": "理由"}"""


def decide_tool(question: str) -> dict:
    """LLM 决策：调用哪个工具"""
    return llm_call_json(f"用户问题: {question}\n\n选择工具:", system=SYSTEM_PROMPT)


def execute_tool(client: SciverseClient, decision: dict) -> str:
    """执行工具调用并返回格式化结果"""
    tool, params = decision["tool"], decision.get("params", {})
    print(f"  工具: {tool}  参数: {json.dumps(params, ensure_ascii=False)}")
    print(f"  理由: {decision.get('reason','')}\n")

    if tool == "search_papers":
        papers = client.search_papers(params.get("query",""),
            year_from=params.get("year_from"), year_to=params.get("year_to"),
            journals=params.get("journals"), authors=params.get("authors"),
            page_size=params.get("page_size",5)).get("results",[])
        return "\n".join(f"[{p.get('publication_published_year','')}] {p.get('title','')}" for p in papers) or "无结果"

    elif tool == "semantic_search":
        chunks = client.semantic_search(params.get("query",""),
            top_k=params.get("top_k",5), mode=params.get("mode","balanced")).get("chunks",[])
        return "\n".join(f"[{c.get('score',0):.3f}] {c.get('title','')}" for c in chunks) or "无结果"

    elif tool == "list_paper_relations":
        papers = client.list_paper_relations(params.get("unique_id",""),
            params.get("relation","CITATIONS"), page_size=5).get("items",[])
        return "\n".join(f"[{p.get('publication_published_year','')}] {p.get('title','')}" for p in papers) or "无结果"
    return f"未知工具: {tool}"


def search_agent(question: str):
    """检索 Agent 主函数"""
    print(f"问题: {question}\n")
    try:
        client = SciverseClient()
    except ValueError as e:
        print(f"请设置 SCIVERSE_API_KEY: {e}"); return
    print("[1] LLM 决策...")
    decision = decide_tool(question)
    print("[2] 执行检索...")
    results = execute_tool(client, decision)
    print("[3] 结果:")
    print("-" * 40)
    print(results)


def main():
    print("=== 文献检索 Agent ===\n")
    q = sys.argv[1] if len(sys.argv) > 1 else "最近两年有没有关于用机器学习预测热电材料性能的文章？"
    search_agent(q)


if __name__ == "__main__":
    main()
