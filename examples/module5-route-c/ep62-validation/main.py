"""
AIGO 教程系列 - 路线 C·合成路线与工艺设计
ep62-validation: 合成验证策略
三级验证：计算验证 → 文献验证 → 实验验证
"""

import sys
from pathlib import Path
import os
import json

# 导入共享模块
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
def level1_computational_validation(target: str, route: dict) -> dict:
    """
    第一级：计算验证
    检查热力学可行性（反应焓、相稳定性）
    """
    print("\n" + "=" * 50)
    print("第一级验证：计算验证（热力学）")
    print("=" * 50)

    # 模拟热力学计算
    # 实际中可调用 Materials Project API 或 DFT 计算
    demo_checks = {
        "反应焓变 (ΔH)": {"value": -125.3, "unit": "kJ/mol", "pass": True},
        "产物相稳定性": {"value": "立方相 LLZO", "unit": "", "pass": True},
        "副产物风险": {"value": "La2Zr2O7 (微量)", "unit": "", "pass": True},
        "氧化态一致性": {"value": "Li(+1) La(+3) Zr(+4) O(-2)", "unit": "", "pass": True},
    }

    all_pass = True
    for check_name, result in demo_checks.items():
        status = "✓" if result["pass"] else "✗"
        print(f"  [{status}] {check_name}: {result['value']} {result['unit']}")
        if not result["pass"]:
            all_pass = False

    print(f"\n  计算验证结果: {'通过' if all_pass else '未通过'}")
    return {"level": 1, "passed": all_pass, "details": demo_checks}


def level2_literature_validation(target: str, route: dict) -> dict:
    """
    第二级：文献验证
    搜索相似体系的实验报道，对比条件
    """
    print("\n" + "=" * 50)
    print("第二级验证：文献验证")
    print("=" * 50)

    # 尝试用 Sciverse 搜索
    try:
        from sciverse_client import SciverseClient
        client = SciverseClient()
        papers = client.search_papers(f"{target} synthesis", limit=5)

        print(f"\n  找到 {len(papers)} 篇相关文献:")
        for p in papers:
            print(f"    - {p.get('title', 'N/A')} ({p.get('year', 'N/A')})")
            if p.get('abstract'):
                print(f"      摘要: {p['abstract'][:100]}...")

        return {"level": 2, "passed": len(papers) > 0, "papers_found": len(papers)}
    except Exception as e:
        print(f"\n  [演示模式] Sciverse 不可用: {e}")

    # 演示数据
    demo_papers = [
        {"title": "High-performance LLZO solid electrolyte...", "year": 2023, "match": 0.92},
        {"title": "Sol-gel synthesis of garnet-type...", "year": 2022, "match": 0.88},
        {"title": "Effect of Li excess on LLZO...", "year": 2023, "match": 0.85},
    ]

    print(f"\n  找到 {len(demo_papers)} 篇高度相关文献:")
    for p in demo_papers:
        print(f"    - [{p['match']:.0%} 匹配] {p['title']} ({p['year']})")

    print(f"\n  文献验证结果: 通过 (有相似体系报道)")
    return {"level": 2, "passed": True, "papers_found": len(demo_papers)}


def level3_experimental_validation(target: str, route: dict) -> dict:
    """
    第三级：实验验证规划
    设计关键表征步骤验证合成成功
    """
    print("\n" + "=" * 50)
    print("第三级验证：实验验证规划")
    print("=" * 50)

    validation_steps = [
        {
            "technique": "XRD (X射线衍射)",
            "purpose": "确认物相结构（立方/四方 LLZO）",
            "success_criteria": "特征峰位置与 ICDD 卡片匹配",
            "priority": "必须"
        },
        {
            "technique": "SEM (扫描电镜)",
            "purpose": "观察微观形貌与晶粒尺寸",
            "success_criteria": "致密微观结构，晶粒 > 1μm",
            "priority": "必须"
        },
        {
            "technique": "EIS (电化学阻抗谱)",
            "purpose": "测量离子电导率",
            "success_criteria": "室温电导率 > 10⁻⁴ S/cm",
            "priority": "必须"
        },
        {
            "technique": "ICP-OES",
            "purpose": "验证实际元素组成",
            "success_criteria": "Li:La:Zr 比例偏差 < 5%",
            "priority": "推荐"
        },
        {
            "technique": "TGA-DSC",
            "purpose": "分析热稳定性与相变",
            "success_criteria": "立方相稳定至 500°C 以上",
            "priority": "可选"
        },
    ]

    for step in validation_steps:
        priority_mark = {"必须": "★", "推荐": "○", "可选": "·"}[step["priority"]]
        print(f"\n  [{priority_mark}] {step['technique']}")
        print(f"      目的: {step['purpose']}")
        print(f"      判据: {step['success_criteria']}")

    return {"level": 3, "passed": None, "steps": validation_steps}


def run_full_validation(target: str, route: dict):
    """运行完整三级验证"""
    print(f"\n{'#'*60}")
    print(f"三级验证流程 - 目标材料: {target}")
    print(f"{'#'*60}")

    results = []

    # 第一级
    r1 = level1_computational_validation(target, route)
    results.append(r1)

    if not r1["passed"]:
        print("\n⚠ 计算验证未通过，建议修改路线后重新验证。")
        return results

    # 第二级
    r2 = level2_literature_validation(target, route)
    results.append(r2)

    # 第三级（无论前两级结果如何，都给出实验验证规划）
    r3 = level3_experimental_validation(target, route)
    results.append(r3)

    # 汇总
    print(f"\n{'='*60}")
    print("验证汇总")
    print(f"{'='*60}")
    for r in results:
        status = "通过" if r["passed"] else ("待验证" if r["passed"] is None else "未通过")
        print(f"  第{r['level']}级验证: {status}")

    return results


def main():
    print("ep62 - 合成验证策略（三级验证）")
    print("=" * 60)

    target = "Li7La3Zr2O12 (LLZO)"
    route = {
        "method": "溶胶-凝胶法",
        "temperature_c": 750,
        "precursors": ["LiNO3", "La(NO3)3", "Zr(O-nBu)4"],
    }

    run_full_validation(target, route)

    print("\n" + "=" * 60)
    print("验证策略要点：")
    print("""
    1. 计算验证（最快）：热力学可行性 → 排除不可能路线
    2. 文献验证（中等）：有无相似体系报道 → 增加信心
    3. 实验验证（最可靠）：实际表征 → 最终确认
    4. 三级递进：每级通过后才进入下一级，节省资源
    5. 失败分析：某级未通过时，回溯修改路线而非盲目实验
    """)


if __name__ == "__main__":
    main()
