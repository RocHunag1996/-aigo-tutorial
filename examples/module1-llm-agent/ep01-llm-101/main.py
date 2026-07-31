"""
ep01-llm-101: 大语言模型 101
演示调用大模型，观察 temperature 对输出的影响。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from llm_call import llm_call

QUESTION = "用一句话描述钛合金在航空航天中的应用前景。"
SYSTEM = "你是一位材料科学领域的科普作者，语言简洁准确。"


def demo_temperature():
    """对比不同 temperature 下的输出"""
    print("=" * 50)
    print("【演示 1】temperature 对输出的影响")
    print("=" * 50)
    print(f"问题：{QUESTION}\n")
    # temperature=0 → 确定性输出；0.7 → 平衡；1.5 → 天马行空
    for temp in [0.0, 0.7, 1.5]:
        print(f"--- temperature = {temp} ---")
        print(llm_call(QUESTION, system=SYSTEM, temperature=temp, max_tokens=100))
        print()


def demo_top_p():
    """用 temperature 近似模拟 top_p 的效果差异"""
    print("=" * 50)
    print("【演示 2】top_p 对输出的影响（temperature 近似）")
    print("=" * 50)
    # top_p 越小采样范围越窄，输出越集中
    for p in [0.1, 0.5, 0.95]:
        print(f"--- top_p ≈ {p} ---")
        print(llm_call(QUESTION, system=SYSTEM, temperature=max(0.0, p - 0.3), max_tokens=100))
        print()


def demo_reproducibility():
    """temperature=0 的可重复性测试"""
    print("=" * 50)
    print("【演示 3】temperature=0 可重复性（连续 3 次）")
    print("=" * 50)
    results = [llm_call(QUESTION, system=SYSTEM, temperature=0.0, max_tokens=80) for _ in range(3)]
    for i, r in enumerate(results, 1):
        print(f"第 {i} 次：{r}")
    verdict = "✓ 完全一致" if len(set(results)) == 1 else "✗ 存在微小差异"
    print(f"\n{verdict} — temperature=0 趋近确定性输出")


def main():
    print("🔬 ep01 — 大语言模型 101\n")
    demo_temperature()
    demo_top_p()
    demo_reproducibility()
    print("\n✅ 要点：temperature 越低越稳定，越高越有创造性。")


if __name__ == "__main__":
    main()
