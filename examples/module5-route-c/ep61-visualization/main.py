"""
AIGO 教程系列 - 路线 C·合成路线与工艺设计
ep61-visualization: 推理过程可视化
用 ASCII 图形展示合成决策流程与路线对比
"""


def draw_decision_flowchart():
    """绘制合成决策流程图"""
    chart = """
╔══════════════════════════════════════════════════════════════════╗
║                    合成路线决策流程图                             ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║   ┌─────────────┐                                               ║
║   │  目标材料    │                                               ║
║   └──────┬──────┘                                               ║
║          │                                                       ║
║          ▼                                                       ║
║   ┌─────────────┐     否     ┌─────────────┐                    ║
║   │ 知识库中有  │──────────▶│ LLM 推理    │                    ║
║   │ 相似合成?   │            │ 生成新路线  │                    ║
║   └──────┬──────┘            └──────┬──────┘                    ║
║          │ 是                       │                            ║
║          ▼                          ▼                            ║
║   ┌─────────────┐            ┌─────────────┐                    ║
║   │ 提取已知    │            │ 评估可行性  │                    ║
║   │ 最优条件    │            │ (热力学/成本)│                    ║
║   └──────┬──────┘            └──────┬──────┘                    ║
║          │                          │                            ║
║          └──────────┬───────────────┘                            ║
║                     ▼                                            ║
║              ┌─────────────┐                                     ║
║              │ 候选路线池  │                                     ║
║              └──────┬──────┘                                     ║
║                     │                                            ║
║          ┌──────────┼──────────┐                                 ║
║          ▼          ▼          ▼                                 ║
║   ┌──────────┐┌──────────┐┌──────────┐                          ║
║   │ 路线 A   ││ 路线 B   ││ 路线 C   │                          ║
║   │ 固相法   ││ 溶胶凝胶 ││ 水热法   │                          ║
║   │ 1100°C   ││ 750°C    ││ 200°C    │                          ║
║   │ 产率:85% ││ 产率:78% ││ 产率:65% │                          ║
║   └────┬─────┘└────┬─────┘└────┬─────┘                          ║
║        │           │           │                                 ║
║        └───────────┼───────────┘                                 ║
║                    ▼                                             ║
║             ┌─────────────┐                                      ║
║             │ 多准则评估  │                                      ║
║             │ (产率/成本/ │                                      ║
║             │  可重复性)  │                                      ║
║             └──────┬──────┘                                      ║
║                    │                                             ║
║                    ▼                                             ║
║             ┌─────────────┐                                      ║
║             │ 推荐最优路线│                                      ║
║             └─────────────┘                                      ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""
    print(chart)


def draw_route_comparison(routes: list):
    """绘制路线对比条形图"""
    print("\n合成路线对比")
    print("=" * 50)

    metrics = ["产率", "成本", "可重复性", "安全性"]

    for route in routes:
        print(f"\n  [{route['name']}]")
        for metric in metrics:
            value = route["scores"].get(metric, 0)
            bar = "█" * int(value / 5) + "░" * (20 - int(value / 5))
            print(f"    {metric:6s} |{bar}| {value:.0f}/100")


def draw_timeline(steps: list):
    """绘制合成时间线"""
    print("\n合成时间线")
    print("=" * 50)

    total_time = sum(s.get("time_h", 0) for s in steps)
    current_time = 0

    for i, step in enumerate(steps):
        time_h = step.get("time_h", 0)
        current_time += time_h

        # 时间条
        bar_len = int(time_h / max(total_time, 1) * 40)
        bar = "█" * max(bar_len, 1)

        print(f"\n  步骤 {i+1}: {step['name']}")
        print(f"    {bar} {time_h}h")
        if step.get("temp"):
            print(f"    温度: {step['temp']}°C")

    print(f"\n  总耗时: {total_time}h ({total_time/24:.1f}天)")


def draw_parameter_space():
    """绘制参数空间热力图（ASCII）"""
    print("\n参数空间热力图（温度 vs 时间 → 产率）")
    print("=" * 50)

    # 模拟产率数据
    temps = [900, 950, 1000, 1050, 1100, 1150, 1200]
    times = [4, 8, 12, 16, 20]

    import numpy as np
    print("\n         | " + " | ".join(f"{t:4d}" for t in temps) + " |")
    print("   " + "-" * (7 * len(temps) + 5))

    for t in times:
        row = f"  {t:3d}h | "
        for temp in temps:
            # 模拟产率
            yield_val = np.exp(-0.5 * ((temp - 1075) / 75) ** 2) * \
                        np.exp(-0.5 * ((t - 12) / 5) ** 2) * 100
            # ASCII 灰度
            if yield_val > 80:
                cell = "████"
            elif yield_val > 60:
                cell = "▓▓▓▓"
            elif yield_val > 40:
                cell = "▒▒▒▒"
            elif yield_val > 20:
                cell = "░░░░"
            else:
                cell = "    "
            row += f"{cell} "
        row += "|"
        print(row)

    print("\n  图例: ████ >80%  ▓▓▓▓ >60%  ▒▒▒▒ >40%  ░░░░ >20%     <20%")


def main():
    print("ep61 - 推理过程可视化")
    print("=" * 60)

    # 1. 决策流程图
    draw_decision_flowchart()

    # 2. 路线对比
    routes = [
        {"name": "路线A: 固相法", "scores": {"产率": 85, "成本": 70, "可重复性": 80, "安全性": 75}},
        {"name": "路线B: 溶胶凝胶", "scores": {"产率": 78, "成本": 55, "可重复性": 85, "安全性": 80}},
        {"name": "路线C: 水热法", "scores": {"产率": 65, "成本": 60, "可重复性": 70, "安全性": 85}},
    ]
    draw_route_comparison(routes)

    # 3. 时间线
    steps = [
        {"name": "前驱体称量与混合", "time_h": 2, "temp": None},
        {"name": "球磨", "time_h": 12, "temp": None},
        {"name": "预烧", "time_h": 6, "temp": 800},
        {"name": "二次球磨", "time_h": 4, "temp": None},
        {"name": "烧结", "time_h": 12, "temp": 1100},
        {"name": "冷却与表征", "time_h": 8, "temp": None},
    ]
    draw_timeline(steps)

    # 4. 参数空间热力图
    draw_parameter_space()


if __name__ == "__main__":
    main()
