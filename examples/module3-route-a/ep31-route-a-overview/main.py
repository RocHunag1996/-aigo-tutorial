"""
AIGO 教程系列 - 路线 A·构效关系发现
ep31-route-a-overview: 路线 A 总览 —— 打印技术路线图，说明各步骤对应的代码文件
"""


def print_roadmap():
    """打印路线 A 完整技术路线图。"""
    roadmap = """
+================================================================+
|              路线 A - 构效关系发现 技术路线图                     |
+================================================================+
|                                                                  |
|  +-------------+    +--------------+    +------------------+     |
|  | 数据采集     |--->| 特征工程      |--->| 搜索与优化        |    |
|  | ep32/ep33   |    | ep34         |    | ep35/ep36/ep37   |    |
|  +-------------+    +--------------+    +------------------+     |
|         |                     |                      |           |
|         v                     v                      v           |
|  +-------------+    +--------------+    +------------------+     |
|  | LLM 融合    |--->| 搜索空间设计  |--->| 证据链构建        |    |
|  | ep38        |    | ep39         |    | ep40             |    |
|  +-------------+    +--------------+    +------------------+     |
|                                                   |              |
|                                                   v              |
|                              +--------------+  +------------+    |
|                              | 可解释性分析  |->| 实战案例    |   |
|                              | ep41         |  | ep42       |   |
|                              +--------------+  +------------+    |
+================================================================+
"""
    print(roadmap)


def print_file_index():
    """打印各期代码文件索引。"""
    index = [
        ("ep31", "route-a-overview",     "路线 A 总览（本文件）"),
        ("ep32", "materials-project",    "Materials Project API 数据查询"),
        ("ep33", "oqmd-nomad",           "OQMD / NOMAD 数据库对接"),
        ("ep34", "feature-engineering",  "成分->特征工程（Magpie 简化版）"),
        ("ep35", "genetic-algorithm",    "遗传算法搜索高 ZT 成分"),
        ("ep36", "bayesian-optimization","贝叶斯优化催化剂成分"),
        ("ep37", "symbolic-regression",  "符号回归发现构效公式"),
        ("ep38", "llm-search-fusion",    "LLM + 搜索融合循环"),
        ("ep39", "search-space",         "搜索空间设计与先验约束"),
        ("ep40", "evidence-chain",       "文献证据链构建"),
        ("ep41", "interpretability",     "特征重要性与物理解释"),
        ("ep42", "case-study",           "Heusler 合金实战案例"),
        ("ep43", "route-a-scoring",      "质量清单逐项拆解"),
        ("ep44", "module3-summary",      "模块三总结与常见翻车点"),
    ]

    print("\n  路线 A 代码文件索引：")
    print("-" * 60)
    for ep, folder, desc in index:
        print(f"  {ep} | {folder:<26s} | {desc}")
    print("-" * 60)


def main():
    print("=" * 66)
    print("  AIGO 教程 - 模块三 - 路线 A - 构效关系发现")
    print("=" * 66)

    print_roadmap()
    print_file_index()

    print("\n  学习建议：")
    print("  1. 先跑通 ep32/ep33 的数据采集，熟悉数据库 API")
    print("  2. ep34 特征工程是后续所有步骤的基础，务必理解")
    print("  3. ep35-37 是三种不同的搜索策略，可以并行学习")
    print("  4. ep38 开始引入 LLM，注意 prompt 设计技巧")
    print("  5. ep42 是综合实战，建议在前面的 episode 都跑通后再做")


if __name__ == "__main__":
    main()
