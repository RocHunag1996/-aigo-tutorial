"""
AIGO 教程系列 - 基本任务·文献调研 Agent
ep22-entity-alignment: 实体对齐与消歧

演示化学式归一化（如 "LiCoO2" vs "LiCoO_2" vs "LCO"）、缩写展开、
材料名称标准化。用规则+简单字典实现。
"""

from __future__ import annotations

import re

# ── 缩写词典：常见材料缩写 → 标准化学式 ───────────────────────

ABBREVIATION_DICT = {
    "LCO":  "LiCoO2",
    "LFP":  "LiFePO4",
    "LMO":  "LiMn2O4",
    "NMC":  "LiNiMnCoO2",
    "NCA":  "LiNiCoAlO2",
    "LLZO": "Li7La3Zr2O12",
    "LLTO": "Li3xLa2/3-xTiO3",
    "PZT":  "PbZr0.52Ti0.48O3",
    "BTO":  "BaTiO3",
    "GO":   "Graphene Oxide",
    "RGO":  "Reduced Graphene Oxide",
    "CNT":  "Carbon Nanotube",
}

# 同义名称映射 → 标准化学式
SYNONYM_MAP = {
    "钴酸锂":       "LiCoO2",
    "磷酸铁锂":     "LiFePO4",
    "锰酸锂":       "LiMn2O4",
    "三元材料":     "LiNiMnCoO2",
    "石榴石电解质": "Li7La3Zr2O12",
    "titanium dioxide": "TiO2",
    "titania":          "TiO2",
    "silicon dioxide":  "SiO2",
    "silica":           "SiO2",
}


def normalize_formula(raw: str) -> str:
    """
    归一化化学式：
    1. 去除下标格式（LaTeX 下划线、HTML sub 标签、Unicode 下标）
    2. 展开已知缩写
    3. 匹配同义词
    """
    text = raw.strip()

    # 去除 LaTeX 下标标记：LiCoO_2 → LiCoO2
    text = re.sub(r"_\{?(\d+)\}?", r"\1", text)

    # 去除 HTML <sub> 标签
    text = re.sub(r"<sub>(\d+)</sub>", r"\1", text)

    # Unicode 下标数字映射
    unicode_sub = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
    text = text.translate(unicode_sub)

    # 去除多余空格
    text = re.sub(r"\s+", "", text)

    # 尝试展开缩写（全大写短词）
    upper = text.upper()
    if upper in ABBREVIATION_DICT:
        return ABBREVIATION_DICT[upper]

    # 尝试同义词映射（不区分大小写）
    lower = text.lower()
    for synonym, standard in SYNONYM_MAP.items():
        if lower == synonym.lower():
            return standard

    return text


def align_material_name(name: str) -> dict:
    """对材料名称做对齐与消歧，返回归一化结果。"""
    normalized = normalize_formula(name)
    has_formula = bool(re.search(r"\d", normalized))
    return {
        "original": name,
        "normalized": normalized,
        "formula": normalized if has_formula else None,
    }


def demo_alignment():
    """演示各种需要归一化的材料名称。"""
    test_cases = [
        # 化学式格式差异
        "LiCoO_2", "LiCoO2", "LiCoO2", "LCO",
        # 缩写
        "LFP", "LLZO", "NMC",
        # 中文同义词
        "钴酸锂", "磷酸铁锂", "石榴石电解质",
        # 英文同义词
        "titania", "silica",
        # 带 HTML 下标
        "BaTiO<sub>3</sub>",
    ]

    print("=" * 55)
    print("  实体对齐与消歧结果")
    print("=" * 55)
    print(f"{'原始名称':<22} {'归一化名称':<22} {'化学式'}")
    print("-" * 65)

    for name in test_cases:
        result = align_material_name(name)
        formula = result["formula"] or "-"
        print(f"{result['original']:<22} {result['normalized']:<22} {formula}")


def main():
    # 运行对齐演示
    demo_alignment()

    # 演示：同一材料的不同写法归一化到同一实体
    print("\n\n--- 对齐验证：不同写法是否归一为同一实体 ---")
    variants = ["LCO", "LiCoO_2", "钴酸锂", "LiCoO2"]
    normalized_set = set()
    for v in variants:
        result = align_material_name(v)
        normalized_set.add(result["normalized"])
        print(f"  '{v}' → '{result['normalized']}'")

    if len(normalized_set) == 1:
        print(f"\n  所有写法归一化为: {normalized_set.pop()}")
    else:
        print(f"\n  归一化结果不一致: {normalized_set}")


if __name__ == "__main__":
    main()
