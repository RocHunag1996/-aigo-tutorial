"""
ep05-agent-concept: Agent 到底是什么
演示 Observe→Think→Act 的 ReAct 循环，Agent 多步完成研究任务。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from llm_call import llm_call

# ── 模拟知识库 ──────────────────────────────────────────

KNOWLEDGE = {
    "形状记忆合金": "发现1932年；代表NiTi镍钛诺；原理：马氏体相变；应用：医疗器械、航天",
    "石墨烯": "发现2004年；单层碳原子二维材料；原理：sp²蜂窝晶格；应用：电子、复合材料、能源",
}


def search_knowledge(topic: str) -> str:
    """模拟文献检索"""
    return f"【检索】{KNOWLEDGE[topic]}" if topic in KNOWLEDGE else f"【检索】未找到 {topic}"


# ── ReAct Agent ──────────────────────────────────────────

def react_agent(task: str, max_steps: int = 5):
    """Observe → Think → Act 循环"""
    print(f"\n📋 任务：{task}\n")
    history = []

    for step in range(1, max_steps + 1):
        print(f"{'─' * 45}\n📍 步骤 {step}")
        context = "\n".join(history) if history else "（刚开始）"

        # Think + Act：让 LLM 决定下一步
        response = llm_call(
            f"任务：{task}\n可用工具：search_knowledge(主题)\n进度：{context}\n\n"
            f"回复格式：\nThought: <思考>\nAction: search_knowledge(<主题>)\n"
            f"或 Action: FINISH",
            system="材料科学助手，按 Thought/Action 格式回复。",
            temperature=0.0, max_tokens=250,
        )

        # 解析 Thought / Action
        thought, action = "", ""
        for line in response.strip().split("\n"):
            if line.startswith("Thought:"):
                thought = line.split(":", 1)[1].strip()
                print(f"🧠 {thought}")
            elif line.startswith("Action:"):
                action = line.split(":", 1)[1].strip()

        # 判断是否完成
        if "FINISH" in action:
            print("\n✅ 任务完成！生成总结...")
            summary = llm_call(
                f"基于以下记录给出总结：\n任务：{task}\n记录：{context}",
                temperature=0.3, max_tokens=250,
            )
            print(f"\n📊 最终报告：\n{summary}")
            return

        # 执行工具（Observe）
        if "search_knowledge(" in action:
            topic = action.split("(")[1].rstrip(")").strip().strip("\"'")
            print(f"🔍 Act：search_knowledge(\"{topic}\")")
            observation = search_knowledge(topic)
            print(f"👁️ Observe：{observation}")
            history.append(f"步骤{step}: 检索 {topic} → {observation}")
        else:
            print(f"⚠️ 无法解析：{action}")

    print("\n⚠️ 达到最大步数。")


def main():
    print("🤖 ep05 — Agent 到底是什么\n")
    print("Agent 循环：Observe → Think → Act\n")
    react_agent("调研形状记忆合金和石墨烯的关键信息，做简要对比。")
    print("\n✅ 要点：Agent = LLM + 工具 + 循环。")


if __name__ == "__main__":
    main()
