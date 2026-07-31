"""
AIGO 教程系列 - 路线 A·构效关系发现
ep38-llm-search-fusion: LLM + 搜索融合

用 LLM 生成种子候选材料、评估搜索结果科学性。
实现 LLM 指导搜索方向的闭环迭代。
"""
import sys
from pathlib import Path
import os
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from llm_call import llm_call, llm_call_json


SYSTEM_PROMPT = "你是一位材料科学专家，专注于热电材料研究。回答要简洁、专业、有依据。"


def llm_generate_candidates(target_property="高热电优值 ZT > 2", n_candidates=5):
    """用 LLM 生成种子候选材料列表。"""
    prompt = f"""请推荐 {n_candidates} 个有潜力实现"{target_property}"的材料体系。
要求：
1. 给出化学式
2. 简述推荐理由（1 句话）
3. 预估 ZT 范围

请以 JSON 格式返回：
{{"candidates": [{{"formula": "...", "reason": "...", "estimated_zt": "x-y"}}]}}"""

    print("\n  LLM 生成种子候选材料...")
    result = llm_call_json(prompt, system=SYSTEM_PROMPT)
    return result.get("candidates", [])


def llm_evaluate_search_results(query, results_summary):
    """用 LLM 评估搜索结果的科学性。"""
    prompt = f"""搜索查询: {query}

搜索结果摘要:
{results_summary}

请评估：
1. 这些结果是否科学合理？（1-10 分）
2. 有无明显遗漏的材料体系？
3. 建议下一步搜索方向

以 JSON 返回：
{{"score": 0, "assessment": "...", "missing": "...", "next_query": "..."}}"""

    print(f"\n  LLM 评估搜索结果...")
    result = llm_call_json(prompt, system=SYSTEM_PROMPT)
    return result


def llm_refine_search_direction(history):
    """根据历史搜索记录，让 LLM 调整搜索策略。"""
    history_text = "\n".join([
        f"第{h['round']}轮: 查询='{h['query']}', 评分={h['score']}, 评估={h['assessment']}"
        for h in history
    ])

    prompt = f"""以下是之前的搜索历史：
{history_text}

请分析：
1. 哪些搜索方向有成效？
2. 哪些方向应该放弃？
3. 给出下一轮的具体搜索查询（关键词）

以 JSON 返回：
{{"analysis": "...", "abandon": "...", "next_queries": ["query1", "query2"]}}"""

    print(f"\n  LLM 调整搜索方向...")
    result = llm_call_json(prompt, system=SYSTEM_PROMPT)
    return result


def simulate_search(query):
    """
    模拟数据库搜索（实际项目中应调用 Sciverse 或 MP API）。
    """
    simulated_results = {
        "Bi2Te3 热电": "找到 Bi2Te3 基材料 ZT~1.0，Se 掺杂可提升至 1.4",
        "Half-Heusler 热电": "TiNiSn 基 ZT~0.8，双掺杂策略报道 ZT~1.2",
        "SnSe 热电": "单晶 SnSe ZT~2.6（Nature 2014），多晶较低~0.8",
    }
    for key, value in simulated_results.items():
        if any(word in query for word in key.split()):
            return value
    return f"查询 '{query}' 找到若干相关结果，ZT 范围 0.5-1.5"


def run_fusion_loop(n_rounds=3):
    """运行 LLM 指导的搜索融合循环。"""
    history = []

    # 第 1 轮：LLM 生成种子候选
    candidates = llm_generate_candidates()
    print(f"\n  LLM 推荐了 {len(candidates)} 个候选材料：")
    for c in candidates:
        print(f"  - {c.get('formula', 'N/A')}: {c.get('reason', '')}")

    queries = [c.get("formula", "") for c in candidates[:3]]

    for round_num in range(1, n_rounds + 1):
        print(f"\n{'='*50}")
        print(f"  第 {round_num} 轮搜索")
        print(f"{'='*50}")

        query = queries[0] if queries else "热电材料 高ZT"
        print(f"\n  搜索查询: {query}")

        # 执行搜索
        result_summary = simulate_search(query)
        print(f"  搜索结果: {result_summary}")

        # LLM 评估
        evaluation = llm_evaluate_search_results(query, result_summary)
        score = evaluation.get("score", 5)
        assessment = evaluation.get("assessment", "")
        print(f"  LLM 评分: {score}/10")
        print(f"  LLM 评估: {assessment}")

        history.append({
            "round": round_num,
            "query": query,
            "score": score,
            "assessment": assessment,
        })

        # LLM 调整方向
        if round_num < n_rounds:
            direction = llm_refine_search_direction(history)
            print(f"\n  方向调整:")
            print(f"    分析: {direction.get('analysis', '')}")
            next_queries = direction.get("next_queries", [])
            if next_queries:
                queries = next_queries
                print(f"    下一轮查询: {queries}")

    return history


def main():
    print("=" * 60)
    print("  ep38 - LLM + 搜索融合循环")
    print("=" * 60)

    print("\n  核心思路：")
    print("  LLM 负责'科学直觉' -- 生成假设、评估结果、调整方向")
    print("  搜索引擎负责'数据验证' -- 检索文献、查询数据库")
    print("  两者形成闭环，逐步逼近最优解")

    history = run_fusion_loop(n_rounds=3)

    print(f"\n  搜索历史总结：")
    for h in history:
        print(f"  第{h['round']}轮: 评分 {h['score']}/10 - {h['query']}")

    print("\n  关键设计：")
    print("  - LLM 生成种子候选，避免盲目搜索")
    print("  - 每轮搜索后 LLM 评估科学性，过滤噪声")
    print("  - 历史积累帮助 LLM 做出更明智的方向调整")
    print("  - 实际项目中应接入 Sciverse/MP 等真实数据源")


if __name__ == "__main__":
    main()
