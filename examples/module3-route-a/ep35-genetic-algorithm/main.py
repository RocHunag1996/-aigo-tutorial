"""
AIGO 教程系列 - 路线 A·构效关系发现
ep35-genetic-algorithm: 遗传算法搜索高热电优值成分

实现简单 GA（编码、选择、交叉、变异），用于搜索高 ZT 热电材料成分。
用 numpy 随机模拟适应度函数。
"""
import numpy as np

# ── 候选元素池（热电材料常见元素）──────────────────────────
CANDIDATE_ELEMENTS = ["Bi", "Te", "Sb", "Se", "Pb", "Sn", "Ge", "Si"]
N_ELEMENTS = len(CANDIDATE_ELEMENTS)

# 模拟的 ZT 适应度函数参数（真实场景应调用 DFT 或实验数据）
np.random.seed(42)
# 每种元素对 ZT 的"理想贡献"
IDEAL_FRACTIONS = np.array([0.25, 0.30, 0.15, 0.10, 0.08, 0.05, 0.04, 0.03])


def fitness(composition):
    """
    模拟适应度函数：计算成分与理想配方的"接近程度"。
    composition: 长度为 N_ELEMENTS 的数组，各元素摩尔分数之和为 1。
    返回模拟 ZT 值（0~3 范围）。
    """
    # 与理想配方的负欧氏距离 -> 越接近理想值，ZT 越高
    distance = np.sqrt(np.sum((composition - IDEAL_FRACTIONS) ** 2))
    # 加入少量随机噪声模拟真实场景
    noise = np.random.normal(0, 0.05)
    zt = max(0, 2.5 * np.exp(-3 * distance) + noise)
    return min(zt, 3.0)


def create_individual(n_genes=N_ELEMENTS):
    """创建一个随机个体（成分向量），各分量之和为 1。"""
    return np.random.dirichlet(np.ones(n_genes))


def create_population(pop_size=20):
    """初始化种群。"""
    return np.array([create_individual() for _ in range(pop_size)])


def select_parents(population, fitnesses, n_parents=10):
    """锦标赛选择：每次随机抽 k 个，取最优。"""
    pop_size = len(population)
    selected = []
    for _ in range(n_parents):
        candidates = np.random.choice(pop_size, size=3, replace=False)
        best = candidates[np.argmax(fitnesses[candidates])]
        selected.append(population[best])
    return np.array(selected)


def crossover(parent1, parent2):
    """均匀交叉：随机从两个亲本中各取部分基因。"""
    child = parent1.copy()
    mask = np.random.random(len(parent1)) > 0.5
    child[mask] = parent2[mask]
    # 归一化使总和为 1
    child = child / child.sum()
    return child


def mutate(individual, mutation_rate=0.1, strength=0.05):
    """高斯变异：对每个基因以一定概率施加随机扰动。"""
    for i in range(len(individual)):
        if np.random.random() < mutation_rate:
            individual[i] += np.random.normal(0, strength)
            individual[i] = max(0, individual[i])
    # 归一化
    individual = individual / individual.sum()
    return individual


def run_ga(pop_size=30, n_generations=50, mutation_rate=0.15):
    """运行遗传算法主循环。"""
    print(f"\n  遗传算法参数：")
    print(f"  种群大小={pop_size}, 迭代代数={n_generations}, 变异率={mutation_rate}")

    population = create_population(pop_size)
    history = []

    for gen in range(n_generations):
        # 计算适应度
        fitnesses = np.array([fitness(ind) for ind in population])

        # 记录统计
        best_idx = np.argmax(fitnesses)
        history.append({
            "gen": gen + 1,
            "best_zt": fitnesses[best_idx],
            "avg_zt": fitnesses.mean(),
            "best_comp": population[best_idx].copy(),
        })

        # 选择、交叉、变异
        parents = select_parents(population, fitnesses)
        new_population = []

        # 精英保留
        elite_idx = np.argsort(fitnesses)[-3:]
        for idx in elite_idx:
            new_population.append(population[idx].copy())

        # 生成后代
        while len(new_population) < pop_size:
            p1, p2 = parents[np.random.choice(len(parents), 2, replace=False)]
            child = crossover(p1, p2)
            child = mutate(child, mutation_rate)
            new_population.append(child)

        population = np.array(new_population[:pop_size])

        # 每 10 代打印一次进度
        if (gen + 1) % 10 == 0 or gen == 0:
            print(f"  第 {gen+1:>3d} 代 | 最优 ZT = {fitnesses[best_idx]:.3f} "
                  f"| 平均 ZT = {fitnesses.mean():.3f}")

    return history


def decode_composition(individual):
    """将数值向量解码为化学式字符串。"""
    threshold = 0.05
    parts = []
    for i, frac in enumerate(individual):
        if frac >= threshold:
            elem = CANDIDATE_ELEMENTS[i]
            coeff = round(frac * 10)
            parts.append(f"{elem}{coeff}" if coeff > 1 else elem)
    return "".join(parts) if parts else "N/A"


def main():
    print("=" * 60)
    print("  ep35 - 遗传算法搜索高热电优值成分")
    print("=" * 60)

    ideal_pct = {e: round(f * 100, 1) for e, f in zip(CANDIDATE_ELEMENTS, IDEAL_FRACTIONS)}
    print(f"\n  候选元素池: {CANDIDATE_ELEMENTS}")
    print(f"  理想成分配比（模拟）: {ideal_pct}%")

    history = run_ga(pop_size=30, n_generations=50)

    # 展示最终结果
    best = history[-1]
    print(f"\n  最优结果（第 {best['gen']} 代）：")
    print(f"  模拟 ZT = {best['best_zt']:.3f}")
    print(f"  成分配比:")
    for i, elem in enumerate(CANDIDATE_ELEMENTS):
        frac = best["best_comp"][i]
        bar = "#" * int(frac * 40)
        print(f"    {elem}: {frac:.3f} {bar}")
    print(f"  化学式（近似）: {decode_composition(best['best_comp'])}")

    print(f"\n  进化趋势：")
    print(f"  初始最优 ZT: {history[0]['best_zt']:.3f}")
    print(f"  最终最优 ZT: {history[-1]['best_zt']:.3f}")
    print(f"  提升幅度: {history[-1]['best_zt'] - history[0]['best_zt']:.3f}")

    print("\n  要点：")
    print("  - 真实场景中 fitness 应替换为 DFT/实验计算")
    print("  - 精英保留策略防止最优解丢失")
    print("  - 变异率过大会导致随机搜索，过小会陷入局部最优")


if __name__ == "__main__":
    main()
