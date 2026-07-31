"""
ep02-prompt-engineering: Prompt Engineering
演示 Few-shot、CoT、系统提示词的效果差异。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from llm_call import llm_call


def demo_zero_shot_vs_few_shot():
    """Zero-shot vs Few-shot 对比"""
    print("=" * 50)
    print("【演示 1】Zero-shot vs Few-shot")
    print("=" * 50)
    question = "将以下材料分类为金属/陶瓷/聚合物：Ti-6Al-4V"

    print("\n--- Zero-shot ---")
    print(llm_call(question, temperature=0.0, max_tokens=100))

    print("\n--- Few-shot ---")
    few_shot = """请对材料进行分类。示例：
输入：SiC → 类别：陶瓷
输入：PEEK → 类别：聚合物
输入：Inconel 718 → 类别：金属

现在请分类：
输入：Ti-6Al-4V → 类别："""
    print(llm_call(few_shot, temperature=0.0, max_tokens=50))
    print()


def demo_cot():
    """普通提问 vs Chain-of-Thought"""
    print("=" * 50)
    print("【演示 2】普通提问 vs CoT")
    print("=" * 50)
    question = ("一块铝（密度 2.7 g/cm³）和一块钛（密度 4.5 g/cm³）体积相同，"
                "铝块质量 540g，钛块质量是多少？")

    print("\n--- 普通提问 ---")
    print(llm_call(question, temperature=0.0, max_tokens=200))

    print("\n--- CoT（逐步推理）---")
    cot = question + "\n\n让我们一步一步来：\n第一步：算体积\n第二步：算钛块质量"
    print(llm_call(cot, temperature=0.0, max_tokens=200))
    print()


def demo_system_prompt():
    """不同系统提示词塑造不同角色"""
    print("=" * 50)
    print("【演示 3】系统提示词塑造角色")
    print("=" * 50)
    question = "3D 打印钛合金骨骼植入物有什么优势？"

    print("\n--- A：严谨学术审稿人 ---")
    print(llm_call(question, system="你是严谨的学术审稿人，务必指出证据不足。", temperature=0.3, max_tokens=150))

    print("\n--- B：小学生科普老师 ---")
    print(llm_call(question, system="你是面向小学生的科普老师，用比喻解释概念。", temperature=0.7, max_tokens=150))
    print()


def main():
    print("📝 ep02 — Prompt Engineering\n")
    demo_zero_shot_vs_few_shot()
    demo_cot()
    demo_system_prompt()
    print("✅ 要点：好的 Prompt = 清晰指令 + 示例 + 角色 + 思维链。")


if __name__ == "__main__":
    main()
