"""
ep06-first-agent: 动手搭第一个 Agent
用 DeepSeek + 模拟 Function Calling 构建 Mini Agent，能查天气和材料属性。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from llm_call import llm_call


# ── 工具函数 ──────────────────────────────────────────

def get_weather(city: str) -> str:
    db = {"北京": "晴，25°C", "上海": "多云，28°C", "深圳": "阵雨，30°C", "成都": "阴，22°C"}
    return db.get(city, f"暂无 {city} 天气数据")


def get_material_property(material: str, prop: str) -> str:
    db = {"钛合金": {"密度": "4.51 g/cm³", "熔点": "1668°C", "弹性模量": "114 GPa"},
          "铝合金": {"密度": "2.70 g/cm³", "熔点": "660°C", "弹性模量": "70 GPa"}}
    val = db.get(material, {}).get(prop)
    return f"{material}的{prop}：{val}" if val else f"未找到 {material} 的 {prop}"


TOOLS = {
    "get_weather": {"desc": "查天气", "params": "city", "func": get_weather},
    "get_material_property": {"desc": "查材料属性", "params": "material, prop", "func": get_material_property},
}
TOOL_DESC = "可用工具：\n" + "\n".join(f"  - {n}: {t['desc']}，参数: {t['params']}" for n, t in TOOLS.items())


def agent_loop(query: str, max_turns: int = 5) -> str:
    """Agent 主循环：决策 → 调用工具 → 生成回答"""
    print(f"\n👤 提问：{query}\n")
    history = []
    for turn in range(1, max_turns + 1):
        print(f"--- 轮次 {turn} ---")
        ctx = "\n".join(history) if history else "（无记录）"
        resp = llm_call(
            f"{TOOL_DESC}\n\n问题：{query}\n记录：{ctx}\n\n"
            f"调用工具：TOOL_CALL: 工具名(参数1, 参数2)\n"
            f"可以回答：FINAL_ANSWER: <回答>",
            system="你是有用助手，合理使用工具。", temperature=0.0, max_tokens=300,
        )
        print(f"  LLM：{resp.strip()[:120]}...")
        if "FINAL_ANSWER:" in resp:
            answer = resp.split("FINAL_ANSWER:")[1].strip()
            print(f"\n🤖 回答：{answer}")
            return answer
        if "TOOL_CALL:" in resp:
            call_str = resp.split("TOOL_CALL:")[1].strip()
            try:
                name = call_str.split("(")[0].strip()
                args = [a.strip().strip("\"'") for a in call_str.split("(")[1].rstrip(")").split(",")]
                if name in TOOLS:
                    result = TOOLS[name]["func"](*args)
                    print(f"  🔧 {name} → {result}")
                    history.append(f"{name}({','.join(args)}) → {result}")
                else:
                    print(f"  ⚠️ 未知工具: {name}")
            except Exception as e:
                print(f"  ❌ 错误: {e}")
        else:
            return resp.strip()
    return "处理超时。"


def main():
    print("🚀 ep06 — 动手搭第一个 Agent\n")
    for q in ["北京今天天气怎么样？", "钛合金的密度是多少？和铝合金比哪个更轻？"]:
        print("=" * 50)
        agent_loop(q)
        print()
    print("✅ 要点：Agent = LLM 决策 + 工具执行 + 循环。")


if __name__ == "__main__":
    main()
