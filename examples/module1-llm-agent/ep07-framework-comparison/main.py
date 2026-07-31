"""
ep07-framework-comparison: Agent 框架选型
用纯 Python 实现 Agent，对比 LangChain/CrewAI 等框架的优劣。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from llm_call import llm_call

# ══════════════════════════════════════════════════════════
# 框架对比（阅读即可）
# ══════════════════════════════════════════════════════════
#
#  ┌──────────┬─────────────┬─────────────┬─────────────┐
#  │          │ 手写 Python  │ LangChain   │ CrewAI      │
#  ├──────────┼─────────────┼─────────────┼─────────────┤
#  │ 代码量    │ <100 行     │ 多（模板多）  │ 中等        │
#  │ 学习成本  │ 几乎为零    │ 较高         │ 中等        │
#  │ 灵活性    │ 完全可控    │ 受约束       │ 受约束      │
#  │ 调试      │ 容易        │ 较难         │ 中等        │
#  │ 生态      │ 需自己对接  │ 丰富         │ 中等        │
#  │ 适合      │ 原型/简单   │ 复杂 RAG    │ 多 Agent    │
#  └──────────┴─────────────┴─────────────┴─────────────┘
#
# 结论：先手写理解原理 → 复杂场景再选框架
# ══════════════════════════════════════════════════════════


# ── 纯 Python Agent（~50 行核心代码）─────────────────────

def lookup_material(query: str) -> str:
    """模拟材料数据库"""
    db = {"碳纤维": "轻质高强，密度1.8，用于航空航天",
          "陶瓷": "高硬度耐高温，但脆性大",
          "形状记忆合金": "能恢复原始形状，用于医疗支架"}
    for key, val in db.items():
        if key in query:
            return f"【{key}】{val}"
    return "未找到相关材料"


def mini_agent(question: str) -> str:
    """极简 Agent：决策 → 执行 → 循环"""
    history = []
    for step in range(5):
        ctx = "\n".join(history) if history else "无"
        resp = llm_call(
            f"工具：lookup_material(query) — 查材料\n\n"
            f"问题：{question}\n记录：{ctx}\n\n"
            f"需工具回复：CALL: lookup_material(\"关键词\")\n"
            f"可回答回复：ANSWER: <内容>",
            system="材料科学助手，善用工具。", temperature=0.0, max_tokens=250,
        )
        if "ANSWER:" in resp:
            return resp.split("ANSWER:")[1].strip()
        if "CALL:" in resp:
            call_text = resp.split("CALL:")[1].strip()
            keyword = call_text.split('"')[1] if '"' in call_text else call_text
            result = lookup_material(keyword)
            history.append(f"查询 '{keyword}' → {result}")
            print(f"  🔧 步骤 {step+1}：{result[:50]}...")
        else:
            return resp.strip()
    return "处理超时。"


def main():
    print("⚖️ ep07 — Agent 框架选型\n")
    print("先阅读文件顶部对比表格，再看演示。\n")
    print("=" * 50)
    print("纯 Python Agent（无框架依赖）")
    print("=" * 50)

    for q in ["碳纤维有什么特点？", "形状记忆合金用在哪里？"]:
        print(f"\n👤 {q}")
        print(f"🤖 {mini_agent(q)}")

    print("\n" + "=" * 50)
    print("💡 总结：")
    print("  • ~50 行 Python，无框架依赖")
    print("  • 简单任务手写更透明、更易调试")
    print("  • 需要 RAG/多 Agent 协作时再考虑框架")
    print("=" * 50)


if __name__ == "__main__":
    main()
