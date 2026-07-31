"""
ep03-llm-api: 调用大模型 API
演示基础调用、流式输出模拟、错误重试、token 计费估算。
"""

import sys
from pathlib import Path
import time
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from llm_call import llm_call


def demo_basic_call():
    """基础调用"""
    print("=" * 50)
    print("【演示 1】基础调用")
    print("=" * 50)
    result = llm_call("用一句话解释什么是弹性模量", system="你是材料科学助教。", temperature=0.3, max_tokens=100)
    print(f"回复：{result}\n")


def demo_streaming():
    """模拟流式输出：先获取完整文本，再逐段打印"""
    print("=" * 50)
    print("【演示 2】模拟流式输出")
    print("=" * 50)
    full_text = llm_call("列举三种金属材料及用途，每句不超15字。", temperature=0.5, max_tokens=200)
    print("流式模拟：", end="", flush=True)
    for i in range(0, len(full_text), 4):
        print(full_text[i:i+4], end="", flush=True)
        time.sleep(0.05)
    print("\n")


def demo_retry():
    """演示内置重试机制"""
    print("=" * 50)
    print("【演示 3】错误重试")
    print("=" * 50)
    # 正常调用
    print(f"正常调用：{llm_call('1+1=?', max_tokens=20)}")
    # 故意失败
    print("错误 URL（触发重试后失败）...")
    try:
        llm_call("测试", base_url="https://invalid.example.com/v1", max_retries=2, max_tokens=10)
    except RuntimeError as e:
        print(f"捕获异常：{e}")
    print()


def demo_token_cost():
    """Token 用量与费用估算"""
    print("=" * 50)
    print("【演示 4】Token 估算")
    print("=" * 50)
    prompt = "请介绍形状记忆合金的原理和应用，至少100字。"
    est_input = int(len(prompt) / 1.5)  # 中文约 1.5 字/token
    print(f"输入 prompt（{len(prompt)} 字）→ 估算 ~{est_input} tokens")

    result = llm_call(prompt, temperature=0.5, max_tokens=400)
    est_output = int(len(result) / 1.5)
    print(f"输出（{len(result)} 字）→ 估算 ~{est_output} tokens")
    # DeepSeek 参考价：输入 ¥1/百万，输出 ¥2/百万
    cost = est_input / 1e6 * 1.0 + est_output / 1e6 * 2.0
    print(f"估算费用：¥{cost:.6f}（仅供参考）")


def main():
    print("🔌 ep03 — 调用大模型 API\n")
    demo_basic_call()
    demo_streaming()
    demo_retry()
    demo_token_cost()
    print("\n✅ 要点：理解 API 封装、流式输出、重试和成本。")


if __name__ == "__main__":
    main()
