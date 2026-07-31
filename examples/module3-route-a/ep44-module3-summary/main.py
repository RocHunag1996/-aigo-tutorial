"""
AIGO 教程系列 - 路线 A·构效关系发现
ep44-module3-summary: 模块三总结

汇总路线 A 的关键代码和常见翻车点。
"""


def print_pipeline_summary():
    """打印路线 A 完整 pipeline 总结。"""
    steps = [
        ("ep32-33", "数据采集",
         "MP/OQMD REST API -> 结构化数据",
         "requests.get() + JSON 解析"),
        ("ep34", "特征工程",
         "成分->Magpie特征（加权平均/方差/极差）",
         "numpy 向量化计算"),
        ("ep35", "遗传算法",
         "编码->选择->交叉->变异->精英保留",
         "numpy.random + Dirichlet 分布"),
        ("ep36", "贝叶斯优化",
         "GP建模->EI采集函数->迭代建议",
         "RBF核 + 矩阵求解"),
        ("ep37", "符号回归",
         "表达式树->GP搜索->可解释公式",
         "树结构递归 + 安全求值"),
        ("ep38", "LLM融合",
         "LLM生成->搜索验证->LLM评估->循环",
         "llm_call_json + 闭环设计"),
        ("ep39", "搜索空间",
         "电荷平衡/电负性/半径比约束",
         "约束函数组合过滤"),
        ("ep40", "证据链",
         "计算+文献+实验->交叉验证",
         "Sciverse检索 + 多源对比"),
        ("ep41", "可解释性",
         "相关性分析->特征排序->物理解释",
         "Pearson + 互信息近似"),
        ("ep42", "实战案例",
         "Heusler合金完整pipeline",
         "串联所有步骤"),
    ]

    print("\n  路线 A Pipeline 总结：")
    print("=" * 70)
    for ep, name, desc, tech in steps:
        print(f"\n  [{ep}] {name}")
        print(f"    内容: {desc}")
        print(f"    技术: {tech}")
    print("\n" + "=" * 70)


def print_common_pitfalls():
    """打印常见翻车点。"""
    pitfalls = [
        {
            "title": "API 调用失败",
            "symptom": "requests 超时或返回 401/403",
            "cause": "API key 未设置或额度用完",
            "fix": "检查环境变量: echo $MP_API_KEY / $DEEPSEEK_API_KEY",
        },
        {
            "title": "特征维度不一致",
            "symptom": "numpy 报 shape mismatch",
            "cause": "某些元素不在属性数据库中，导致特征缺失",
            "fix": "在 featurize 前检查所有元素是否在 ELEMENT_PROPERTIES 中",
        },
        {
            "title": "遗传算法不收敛",
            "symptom": "多代后最优适应度不变",
            "cause": "变异率太低（局部最优）或太高（退化为随机搜索）",
            "fix": "变异率建议 0.1-0.2，加入精英保留策略",
        },
        {
            "title": "LLM 返回非法 JSON",
            "symptom": "json.loads 报 JSONDecodeError",
            "cause": "模型输出了 markdown 代码块或多余文字",
            "fix": "使用 llm_call_json（已内置 response_format）",
        },
        {
            "title": "搜索空间过大",
            "symptom": "搜索数万种成分，计算时间爆炸",
            "cause": "约束太少或元素池太大",
            "fix": "先加领域约束（电荷平衡、半径比），缩小到可计算范围",
        },
        {
            "title": "过拟合",
            "symptom": "训练集表现好，新数据预测差",
            "cause": "模型太复杂或数据太少",
            "fix": "简化模型、增加数据、交叉验证",
        },
    ]

    print("\n  常见翻车点：")
    print("=" * 65)
    for i, p in enumerate(pitfalls, 1):
        print(f"\n  {i}. {p['title']}")
        print(f"     症状: {p['symptom']}")
        print(f"     原因: {p['cause']}")
        print(f"     修复: {p['fix']}")
    print("\n" + "=" * 65)


def print_key_takeaways():
    """打印核心收获。"""
    print("\n  核心收获：")
    takeaways = [
        "数据质量决定上限：多源交叉验证 > 单一数据库",
        "特征工程是核心竞争力：好的特征 > 复杂的模型",
        "多种搜索策略互补：GA 全局探索 + BO 精细开发 + SR 可解释",
        "LLM 是科学直觉的放大器：不是替代搜索，而是指导搜索方向",
        "可解释性不是附加项：评审看重 WHY，不只是 WHAT",
    ]
    for i, t in enumerate(takeaways, 1):
        print(f"  {i}. {t}")


def main():
    print("=" * 65)
    print("  ep44 - 模块三总结：路线 A 关键代码与常见翻车点")
    print("=" * 65)

    print_pipeline_summary()
    print_common_pitfalls()
    print_key_takeaways()

    print("\n  模块三学习完成！")
    print("  下一步: 进入模块四 - 路线 B - 模拟方法创新")


if __name__ == "__main__":
    main()
