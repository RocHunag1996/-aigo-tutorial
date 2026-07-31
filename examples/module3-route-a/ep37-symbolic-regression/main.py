"""
AIGO 教程系列 - 路线 A·构效关系发现
ep37-symbolic-regression: 符号回归

演示符号回归思路 -- 用遗传编程（GP）搜索数学表达式。
不依赖 PySR，用 numpy 实现简化版，发现数据中的解析关系。
"""
import numpy as np


# ── 算子定义 ────────────────────────────────────────────────
class Node:
    """表达式树节点。"""
    def __init__(self, value, left=None, right=None):
        self.value = value   # 运算符/变量/常数
        self.left = left
        self.right = right

    def __repr__(self):
        if self.left is None and self.right is None:
            return str(self.value)
        if self.left and self.right:
            return f"({self.left} {self.value} {self.right})"
        return f"{self.value}({self.left})"


# 终端节点（变量和常数）
TERMINALS = ["x1", "x2", "x3"]
# 二元运算符
OPERATORS = ["+", "-", "*", "/"]
UNARY_OPS = ["sqrt", "square"]


def generate_random_tree(depth=2):
    """随机生成一棵表达式树。"""
    if depth == 0 or np.random.random() < 0.3:
        if np.random.random() < 0.7:
            return Node(np.random.choice(TERMINALS))
        else:
            return Node(f"{np.random.uniform(-2, 2):.2f}")

    if np.random.random() < 0.8:
        op = np.random.choice(OPERATORS)
        left = generate_random_tree(depth - 1)
        right = generate_random_tree(depth - 1)
        return Node(op, left, right)
    else:
        op = np.random.choice(UNARY_OPS)
        child = generate_random_tree(depth - 1)
        return Node(op, child, None)


def safe_eval(node, variables):
    """
    安全地计算表达式树的值。
    variables: {"x1": val1, "x2": val2, ...}
    """
    val = node.value
    if val in variables:
        return variables[val]
    try:
        return float(val)
    except (ValueError, TypeError):
        pass

    # 二元运算符
    if val in OPERATORS and node.left and node.right:
        l_val = safe_eval(node.left, variables)
        r_val = safe_eval(node.right, variables)
        if val == "+": return l_val + r_val
        if val == "-": return l_val - r_val
        if val == "*": return l_val * r_val
        if val == "/":
            return l_val / r_val if abs(r_val) > 1e-10 else 1e10

    # 一元运算符
    if val == "sqrt" and node.left:
        v = safe_eval(node.left, variables)
        return np.sqrt(abs(v))
    if val == "square" and node.left:
        v = safe_eval(node.left, variables)
        return v ** 2

    return 0.0


def evaluate_tree(node, X):
    """对数据集批量求值。X: (n_samples, n_features)。"""
    results = np.zeros(X.shape[0])
    for i in range(X.shape[0]):
        variables = {f"x{j+1}": X[i, j] for j in range(X.shape[1])}
        results[i] = safe_eval(node, variables)
    results = np.clip(results, -1e10, 1e10)
    return results


def compute_fitness(node, X, y):
    """适应度 = 1 / (1 + MSE)，越接近 1 越好。"""
    try:
        y_pred = evaluate_tree(node, X)
        if np.any(np.isnan(y_pred)) or np.any(np.isinf(y_pred)):
            return 0.0
        mse = np.mean((y_pred - y) ** 2)
        return 1.0 / (1.0 + mse)
    except Exception:
        return 0.0


def crossover(tree1, tree2):
    """子树交叉：随机选一个子树交换。"""
    new_tree = Node(tree1.value, tree1.left, tree1.right)
    if np.random.random() < 0.5 and tree2.left:
        new_tree.left = tree2.left
    elif tree2.right:
        new_tree.right = tree2.right
    return new_tree


def mutate(tree):
    """点变异：随机修改一个节点。"""
    if np.random.random() < 0.3:
        return Node(np.random.choice(TERMINALS + [f"{np.random.uniform(-1, 1):.2f}"]))
    new_tree = Node(tree.value, tree.left, tree.right)
    if np.random.random() < 0.5 and new_tree.left:
        new_tree.left = mutate(new_tree.left)
    elif new_tree.right:
        new_tree.right = mutate(new_tree.right)
    return new_tree


def symbolic_regression(X, y, pop_size=50, n_gen=30, max_depth=3):
    """遗传编程主循环。"""
    print(f"\n  符号回归参数：种群={pop_size}, 代数={n_gen}, 最大深度={max_depth}")

    population = [generate_random_tree(max_depth) for _ in range(pop_size)]

    for gen in range(n_gen):
        fitnesses = np.array([compute_fitness(ind, X, y) for ind in population])

        best_idx = np.argmax(fitnesses)
        best_fit = fitnesses[best_idx]
        best_expr = population[best_idx]

        if (gen + 1) % 5 == 0 or gen == 0:
            mse = 1.0 / best_fit - 1.0 if best_fit > 0 else float("inf")
            print(f"  第 {gen+1:>3d} 代 | 适应度 = {best_fit:.4f} | "
                  f"MSE = {mse:.4f} | 最优表达式: {best_expr}")

        # 选择 + 交叉 + 变异
        new_pop = [population[best_idx]]  # 精英保留
        while len(new_pop) < pop_size:
            idx1, idx2 = np.random.choice(pop_size, 2, replace=False)
            parent1 = population[idx1] if fitnesses[idx1] > fitnesses[idx2] else population[idx2]
            idx3, idx4 = np.random.choice(pop_size, 2, replace=False)
            parent2 = population[idx3] if fitnesses[idx3] > fitnesses[idx4] else population[idx4]

            child = crossover(parent1, parent2)
            if np.random.random() < 0.2:
                child = mutate(child)
            new_pop.append(child)

        population = new_pop[:pop_size]

    fitnesses = np.array([compute_fitness(ind, X, y) for ind in population])
    best_idx = np.argmax(fitnesses)
    return population[best_idx], fitnesses[best_idx]


def main():
    print("=" * 60)
    print("  ep37 - 符号回归发现构效关系")
    print("=" * 60)

    # 生成模拟数据：y = 2*x1 + x2^2 - x3（含非线性关系）
    np.random.seed(42)
    n_samples = 100
    X = np.random.uniform(-2, 2, size=(n_samples, 3))
    y_true = 2 * X[:, 0] + X[:, 1] ** 2 - X[:, 2]
    y = y_true + np.random.normal(0, 0.3, n_samples)

    print(f"\n  模拟数据：{n_samples} 个样本，3 个特征")
    print(f"  真实关系: y = 2*x1 + x2^2 - x3")
    print(f"  噪声水平: sigma = 0.3")

    best_expr, best_fit = symbolic_regression(X, y, pop_size=50, n_gen=25)

    mse = 1.0 / best_fit - 1.0 if best_fit > 0 else float("inf")
    print(f"\n  发现的最优表达式: {best_expr}")
    print(f"  适应度: {best_fit:.4f}, MSE: {mse:.4f}")

    print("\n  符号回归的优势：")
    print("  - 自动发现可解释的数学公式，而非黑箱模型")
    print("  - 可直接用于科学发现（如新物理关系）")
    print("  - 生产环境推荐用 PySR 或 gplearn 等成熟库")


if __name__ == "__main__":
    main()
