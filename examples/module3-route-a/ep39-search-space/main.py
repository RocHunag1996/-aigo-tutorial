"""
AIGO 教程系列 - 路线 A·构效关系发现
ep39-search-space: 搜索空间设计

演示如何把材料学先验编码为搜索约束：
- 成分范围约束（元素化合价、电负性差异）
- 相稳定性规则（Hume-Rothery 规则简化版）
- 热力学可行性过滤
"""
import numpy as np


# ── 元素属性（简化版）──────────────────────────────────────
ELEMENT_DATA = {
    "Bi": {"valence": 3, "radius": 1.60, "en": 2.02, "group": 15},
    "Te": {"valence": -2, "radius": 1.40, "en": 2.10, "group": 16},
    "Sb": {"valence": 3, "radius": 1.40, "en": 2.05, "group": 15},
    "Se": {"valence": -2, "radius": 1.20, "en": 2.55, "group": 16},
    "Pb": {"valence": 2, "radius": 1.75, "en": 2.33, "group": 14},
    "Sn": {"valence": 2, "radius": 1.40, "en": 1.96, "group": 14},
    "Ge": {"valence": 4, "radius": 1.25, "en": 2.01, "group": 14},
    "Si": {"valence": 4, "radius": 1.10, "en": 1.90, "group": 14},
    "Ti": {"valence": 4, "radius": 1.45, "en": 1.54, "group": 4},
    "Ni": {"valence": 2, "radius": 1.25, "en": 1.91, "group": 10},
    "Co": {"valence": 2, "radius": 1.25, "en": 1.88, "group": 9},
    "Fe": {"valence": 2, "radius": 1.25, "en": 1.83, "group": 8},
    "Cu": {"valence": 1, "radius": 1.30, "en": 1.90, "group": 11},
    "Zn": {"valence": 2, "radius": 1.35, "en": 1.65, "group": 12},
    "Mn": {"valence": 2, "radius": 1.25, "en": 1.55, "group": 7},
}


class SearchSpace:
    """搜索空间管理器：编码材料学先验约束。"""

    def __init__(self, candidate_elements=None):
        self.elements = candidate_elements or list(ELEMENT_DATA.keys())
        self.constraints = []

    def add_constraint(self, name, func):
        """添加一个约束条件。"""
        self.constraints.append((name, func))
        print(f"  [OK] 添加约束: {name}")

    def check(self, composition):
        """
        检查一个成分是否满足所有约束。
        composition: {元素: 摩尔分数}
        返回 (是否通过, 违反的约束列表)
        """
        violations = []
        for name, func in self.constraints:
            if not func(composition):
                violations.append(name)
        return len(violations) == 0, violations

    def filter_candidates(self, candidates):
        """批量过滤候选成分。"""
        passed = []
        for comp in candidates:
            ok, _ = self.check(comp)
            if ok:
                passed.append(comp)
        return passed


# ── 约束函数定义 ────────────────────────────────────────────

def charge_balance_constraint(composition, tolerance=0.5):
    """电荷平衡约束：化合物总价态应接近零。"""
    total_charge = sum(
        ELEMENT_DATA[e]["valence"] * frac
        for e, frac in composition.items()
        if e in ELEMENT_DATA
    )
    return abs(total_charge) < tolerance


def electronegativity_constraint(composition, max_diff=1.5):
    """电负性差异约束：成键元素电负性差异不宜过大。"""
    elements = [e for e in composition if e in ELEMENT_DATA]
    if len(elements) < 2:
        return True
    en_values = [ELEMENT_DATA[e]["en"] for e in elements]
    return (max(en_values) - min(en_values)) <= max_diff


def radius_ratio_constraint(composition, max_ratio=2.0):
    """原子半径比约束（Hume-Rothery 简化版）。"""
    elements = [e for e in composition if e in ELEMENT_DATA]
    if len(elements) < 2:
        return True
    radii = [ELEMENT_DATA[e]["radius"] for e in elements]
    return max(radii) / min(radii) <= max_ratio


def min_fraction_constraint(composition, min_frac=0.05):
    """最小含量约束：每种元素至少占 5%。"""
    return all(frac >= min_frac for frac in composition.values())


def max_elements_constraint(composition, max_n=4):
    """限制最大元素种类数。"""
    return len(composition) <= max_n


def generate_random_compositions(elements, n_samples=20):
    """随机生成候选成分。"""
    compositions = []
    for _ in range(n_samples):
        n_elem = np.random.randint(2, min(5, len(elements) + 1))
        chosen = list(np.random.choice(elements, n_elem, replace=False))
        raw = np.random.dirichlet(np.ones(n_elem))
        comp = {elem: float(frac) for elem, frac in zip(chosen, raw)}
        compositions.append(comp)
    return compositions


def format_composition(comp):
    """格式化成分为可读字符串。"""
    parts = []
    for elem, frac in sorted(comp.items(), key=lambda x: -x[1]):
        coeff = round(frac * 10)
        parts.append(f"{elem}{coeff}" if coeff > 1 else elem)
    return "".join(parts)


def main():
    print("=" * 60)
    print("  ep39 - 搜索空间设计与先验约束")
    print("=" * 60)

    space = SearchSpace(candidate_elements=list(ELEMENT_DATA.keys()))

    print("\n  添加材料学先验约束：")
    space.add_constraint("电荷平衡", lambda c: charge_balance_constraint(c))
    space.add_constraint("电负性差异<=1.5", lambda c: electronegativity_constraint(c))
    space.add_constraint("原子半径比<=2.0", lambda c: radius_ratio_constraint(c))
    space.add_constraint("最小含量>=5%", lambda c: min_fraction_constraint(c))
    space.add_constraint("元素种类<=4", lambda c: max_elements_constraint(c))

    print(f"\n  随机生成 20 个候选成分...")
    candidates = generate_random_compositions(space.elements, n_samples=20)

    passed = space.filter_candidates(candidates)
    print(f"  通过约束: {len(passed)}/{len(candidates)}")

    print(f"\n  通过约束的候选材料：")
    print("-" * 55)
    for i, comp in enumerate(passed):
        formula = format_composition(comp)
        print(f"  {i+1:>2d}. {formula:<20s} ({len(comp)} 种元素)")
    print("-" * 55)

    # 手动测试
    print(f"\n  手动测试: Bi0.4Te0.6")
    test_comp = {"Bi": 0.4, "Te": 0.6}
    ok, violations = space.check(test_comp)
    print(f"  通过: {ok}")
    if violations:
        print(f"  违反: {violations}")

    print(f"\n  搜索空间设计要点：")
    print("  - 约束太松 -> 搜索空间爆炸，浪费计算资源")
    print("  - 约束太紧 -> 可能错过有价值的候选")
    print("  - 建议先用宽松约束粗筛，再逐步收紧")
    print("  - 领域知识是约束设计的核心（如 Hume-Rothery 规则）")


if __name__ == "__main__":
    main()
