"""
ep08-module1-summary: 模块一总结 — 综合实战
完整 Pipeline：接收问题 → CoT 分析 → 调用工具 → 生成报告。
"""

import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from llm_call import llm_call


# ── 工具函数 ──────────────────────────────────────────

def query_material_db(material: str) -> dict:
    db = {"钛合金": {"密度": "4.51", "强度": "900MPa", "特点": "比强度高", "价格": "较高"},
          "铝合金": {"密度": "2.70", "强度": "310MPa", "特点": "轻质易加工", "价格": "中等"},
          "碳纤维复合材料": {"密度": "1.60", "强度": "1500MPa", "特点": "超轻超强", "价格": "很高"}}
    return db.get(material, {"error": f"无 {material} 数据"})


def estimate_cost(material: str, kg: float) -> dict:
    prices = {"钛合金": 300, "铝合金": 25, "碳纤维复合材料": 800}
    unit = prices.get(material, 50)
    return {"材料": material, "数量kg": kg, "单价": f"¥{unit}/kg", "总价": f"¥{unit * kg:,.0f}"}


# ── Pipeline 三步 ─────────────────────────────────────

def step1_analyze(question: str) -> str:
    print("\n📋 步骤 1：CoT 分析")
    print("─" * 40)
    return llm_call(
        f"分析以下问题，拆解所需信息和步骤：\n{question}\n按 1.核心 2.需查材料 3.比较 4.报告内容 思考。",
        system="材料分析师。", temperature=0.2, max_tokens=300,
    )


def step2_gather(analysis: str) -> str:
    print("🔍 步骤 2：收集数据")
    print("─" * 40)
    raw = llm_call(
        f"从分析中提取材料名，JSON 回复：\n{analysis}\n格式：{{\"materials\": [\"材料1\"]}}",
        system="只输出 JSON。", temperature=0.0, max_tokens=80, response_format={"type": "json_object"},
    )
    try:
        materials = json.loads(raw).get("materials", [])
    except json.JSONDecodeError:
        materials = ["钛合金", "铝合金"]
    collected = []
    for mat in materials:
        info, cost = query_material_db(mat), estimate_cost(mat, 10)
        collected.append(f"【{mat}】{json.dumps(info, ensure_ascii=False)} | 成本: {json.dumps(cost, ensure_ascii=False)}")
        print(f"  📦 {mat}：{json.dumps(info, ensure_ascii=False)[:50]}...")
    return "\n".join(collected)


def step3_report(question: str, analysis: str, data: str) -> str:
    print("📝 步骤 3：生成报告")
    print("─" * 40)
    return llm_call(
        f"基于以下信息生成材料选型报告（需求/对比/推荐/成本）：\n"
        f"问题：{question}\n分析：{analysis}\n数据：{data}",
        system="材料工程师，报告简洁。", temperature=0.3, max_tokens=500,
    )


def main():
    print("🎓 ep08 — 模块一总结：综合 Pipeline\n")
    question = "设计无人机机臂，在钛合金和碳纤维复合材料之间选择，请分析。"
    print(f"👤 {question}")

    analysis = step1_analyze(question)
    print(analysis)
    data = step2_gather(analysis)
    report = step3_report(question, analysis, data)
    print(report)

    print("\n" + "=" * 50)
    print("🏁 Pipeline 完成！串联知识：")
    print("  ep01 LLM | ep02 CoT | ep03 API | ep04 工具")
    print("  ep05-06 Agent | ep07 纯 Python")
    print("\n🎉 模块一完结！下一模块深入 Agent 架构。")


if __name__ == "__main__":
    main()
