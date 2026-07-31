"""
AIGO 教程系列 - 路线 A·构效关系发现
ep34-feature-engineering: 数据预处理与特征工程

成分->特征：Magpie features 简化版（原子半径、电负性等元素属性加权平均）
结构->描述符：简化的结构描述符计算
使用 numpy 做数值计算。
"""
import re
import numpy as np

# ── 元素属性数据库（简化版，覆盖常见热电元素）──────────────
ELEMENT_PROPERTIES = {
    # 元素: (原子半径/pm, 电负性, 原子质量, 价电子数, 熔点/K)
    "Bi":  (160, 2.02, 209.0, 5,  544),
    "Te":  (140, 2.10, 127.6, 6,  723),
    "Pb":  (175, 2.33, 207.2, 4,  601),
    "Sb":  (140, 2.05, 121.8, 5,  904),
    "Se":  (120, 2.55,  79.0, 6,  494),
    "Sn":  (140, 1.96, 118.7, 4,  505),
    "Ge":  (125, 2.01,  72.6, 4, 1211),
    "Si":  (110, 1.90,  28.1, 4, 1687),
    "Ti":  (145, 1.54,  47.9, 4, 1941),
    "Ni":  (125, 1.91,  58.7, 10, 1728),
    "Co":  (125, 1.88,  58.9, 9,  1768),
    "Fe":  (125, 1.83,  55.8, 8,  1811),
    "Mn":  (125, 1.55,  54.9, 7,  1519),
    "Cu":  (130, 1.90,  63.5, 11, 1358),
    "Zn":  (135, 1.65,  65.4, 12, 693),
}

PROP_NAMES = ["原子半径", "电负性", "原子质量", "价电子数", "熔点"]


def parse_formula(formula):
    """
    解析化学式，返回 {元素: 原子数} 字典。
    支持简单化学式，如 Bi2Te3, PbTe, TiNiSn。
    """
    pattern = r"([A-Z][a-z]?)(\d*\.?\d*)"
    matches = re.findall(pattern, formula)
    composition = {}
    for element, count_str in matches:
        count = float(count_str) if count_str else 1.0
        composition[element] = composition.get(element, 0) + count
    return composition


def compute_magpie_features(formula):
    """
    计算 Magpie 风格的成分特征（简化版）。
    对每种元素属性计算加权平均、方差、极差等统计量。
    """
    comp = parse_formula(formula)
    total_atoms = sum(comp.values())

    # 检查是否所有元素都在数据库中
    missing = [e for e in comp if e not in ELEMENT_PROPERTIES]
    if missing:
        print(f"  [!] 元素 {missing} 不在属性数据库中，跳过")
        return None

    # 提取各属性的加权值
    n_props = 5  # 属性数量
    weighted_means = np.zeros(n_props)
    weighted_vars = np.zeros(n_props)
    ranges = np.zeros(n_props)

    for i in range(n_props):
        values = np.array([ELEMENT_PROPERTIES[e][i] for e in comp])
        weights = np.array([comp[e] / total_atoms for e in comp])

        # 加权平均
        weighted_means[i] = np.sum(weights * values)
        # 加权方差
        weighted_vars[i] = np.sum(weights * (values - weighted_means[i]) ** 2)
        # 极差
        ranges[i] = np.max(values) - np.min(values)

    return {
        "加权平均": weighted_means,
        "加权方差": weighted_vars,
        "极差": ranges,
    }


def compute_structure_descriptor(formula, spacegroup=166, n_atoms_cell=15):
    """
    简化的结构描述符：基于空间群和晶胞原子数。
    实际项目中应从 CIF 文件提取更丰富的描述符。
    """
    return np.array([
        spacegroup / 230.0,           # 归一化空间群编号
        n_atoms_cell / 100.0,         # 归一化晶胞原子数
        np.log(n_atoms_cell + 1),     # 对数原子数
    ])


def build_feature_vector(formula, spacegroup=166, n_atoms_cell=15):
    """组合成分特征 + 结构描述符，得到完整特征向量。"""
    magpie = compute_magpie_features(formula)
    if magpie is None:
        return None

    struct_desc = compute_structure_descriptor(formula, spacegroup, n_atoms_cell)

    # 拼接: 加权平均(5) + 加权方差(5) + 极差(5) + 结构描述符(3)
    feature = np.concatenate([
        magpie["加权平均"],
        magpie["加权方差"],
        magpie["极差"],
        struct_desc,
    ])
    return feature


def main():
    print("=" * 60)
    print("  ep34 - 数据预处理与特征工程")
    print("=" * 60)

    # 演示材料列表
    materials = [
        ("Bi2Te3", 166, 15),
        ("PbTe", 225, 8),
        ("TiNiSn", 216, 12),
        ("CoSb3", 204, 32),
    ]

    print("\n  元素属性数据库（部分）：")
    header = f"  {'元素':<6s}"
    for name in PROP_NAMES:
        header += f" {name:<10s}"
    print(header)
    print("  " + "-" * 56)
    for elem, props in list(ELEMENT_PROPERTIES.items())[:6]:
        line = f"  {elem:<6s}"
        for p in props:
            line += f" {p:<10.2f}"
        print(line)

    print("\n  材料特征向量计算：")
    feature_matrix = []
    for formula, sg, natoms in materials:
        fv = build_feature_vector(formula, sg, natoms)
        if fv is not None:
            feature_matrix.append(fv)
            print(f"\n  {formula}:")
            print(f"    成分特征(加权平均): {fv[:5].round(2)}")
            print(f"    成分特征(方差):     {fv[5:10].round(2)}")
            print(f"    成分特征(极差):     {fv[10:15].round(2)}")
            print(f"    结构描述符:         {fv[15:].round(3)}")

    # 特征矩阵
    X = np.array(feature_matrix)
    print(f"\n  特征矩阵形状: {X.shape} (样本数 x 特征数)")
    print(f"  特征归一化（z-score）后的均值: {X.mean(axis=0).round(4)}")
    print(f"  特征归一化后的标准差: {X.std(axis=0).round(4)}")

    print("\n  要点：")
    print("  - Magpie features 是材料信息学最常用的成分描述符之一")
    print("  - 加权平均反映整体趋势，方差反映元素差异程度")
    print("  - 结构描述符需从实际晶体结构提取，此处为简化演示")


if __name__ == "__main__":
    main()
