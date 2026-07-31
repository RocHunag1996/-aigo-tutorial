"""
ep04-function-calling: Function Calling
演示工具调用机制：LLM 选择工具 → 提取参数 → 执行 → 返回结果。
"""

import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from llm_call import llm_call


# ── 工具函数 ──────────────────────────────────────────

def calculate_density(mass: float, volume: float) -> dict:
    """计算材料密度"""
    return {"density_g_cm3": round(mass / volume, 2), "note": "密度 = 质量 / 体积"}


def get_crystal_structure(material: str) -> dict:
    """查询晶体结构（模拟数据库）"""
    db = {"铁": "BCC, a=2.87Å", "铝": "FCC, a=4.05Å", "钛": "HCP, a=2.95Å", "铜": "FCC, a=3.61Å"}
    return {"structure": db[material]} if material in db else {"error": f"未找到 {material}"}


def compare_materials(mat_a: str, mat_b: str) -> dict:
    """对比两种材料"""
    props = {"铁": {"密度": 7.87, "熔点": 1538}, "铝": {"密度": 2.70, "熔点": 660},
             "钛": {"密度": 4.51, "熔点": 1668}, "铜": {"密度": 8.96, "熔点": 1085}}
    return {mat_a: props.get(mat_a, {}), mat_b: props.get(mat_b, {})}


# ── 工具注册表 ──────────────────────────────────────────

TOOLS = {
    "calculate_density": {"desc": "计算密度", "params": "mass, volume", "func": calculate_density},
    "get_crystal_structure": {"desc": "查晶体结构", "params": "material", "func": get_crystal_structure},
    "compare_materials": {"desc": "对比材料", "params": "mat_a, mat_b", "func": compare_materials},
}


def let_llm_decide(query: str) -> dict:
    """让 LLM 输出 JSON 决策：选哪个工具、传什么参数"""
    tool_list = "\n".join(f"  - {n}: {t['desc']}，参数: {t['params']}" for n, t in TOOLS.items())
    prompt = f"""可用工具：
{tool_list}

用户问题：{query}
选择合适的工具，以 JSON 回复：{{"tool": "工具名", "arguments": {{...}}}}
不需要工具则回复：{{"tool": "none", "response": "直接回答"}}"""
    return llm_call(prompt, system="只输出合法 JSON。", temperature=0.0, max_tokens=200, response_format={"type": "json_object"})


def execute(decision: dict) -> str:
    """根据决策执行工具"""
    name = decision.get("tool", "none")
    if name == "none":
        return decision.get("response", "无法处理")
    if name not in TOOLS:
        return f"未知工具: {name}"
    result = TOOLS[name]["func"](**decision.get("arguments", {}))
    return json.dumps(result, ensure_ascii=False)


def main():
    print("🔧 ep04 — Function Calling\n")
    queries = [
        "质量 200g、体积 50cm³，密度是多少？",
        "钛的晶体结构是什么？",
        "对比铝和钛的属性",
    ]
    for i, q in enumerate(queries, 1):
        print(f"{'=' * 45}\n测试 {i}：{q}")
        decision = json.loads(let_llm_decide(q))
        print(f"  工具：{decision.get('tool')}  参数：{decision.get('arguments', {})}")
        print(f"  结果：{execute(decision)}\n")

    print("✅ 要点：Function Calling = LLM 选工具 + 提参数 + 执行 + 返回。")


if __name__ == "__main__":
    main()
