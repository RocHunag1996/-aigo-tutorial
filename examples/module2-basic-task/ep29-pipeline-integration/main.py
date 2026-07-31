"""
AIGO 教程系列 - 基本任务·文献调研 Agent
ep29-pipeline-integration: 系统整合

把检索→解析→抽取→Gap→报告串成完整 pipeline。
实现一个 LiteratureAgent 类，串联各模块，端到端跑通。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# 导入共享模块
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from llm_call import llm_call, llm_call_json

# ── Pipeline 各阶段定义 ───────────────────────────────────────


class LiteratureAgent:
    """文献调研 Agent：串联检索→抽取→Gap 发现→报告生成的完整流程。"""

    def __init__(self, topic: str):
        self.topic = topic
        self.papers: list[dict] = []       # 检索到的论文
        self.extractions: list[dict] = []   # 抽取结果
        self.gaps: list[dict] = []          # 发现的 Gap
        self.report: str = ""               # 生成的报告

    # ── 阶段 1: 文献检索 ──────────────────────────────────────

    def search_literature(self):
        """检索相关文献（模拟，实际可调用 Sciverse）。"""
        print(f"\n[阶段 1] 检索文献: \"{self.topic}\"")
        # 模拟检索结果
        self.papers = [
            {
                "title": "High-performance LFP cathodes via carbon coating",
                "year": 2023,
                "abstract": (
                    "LiFePO4 cathodes with carbon coating achieve 160 mAh/g "
                    "at 25 deg C. At -10 deg C, capacity drops to 95 mAh/g."
                ),
            },
            {
                "title": "Ether-based electrolyte for low-temp batteries",
                "year": 2024,
                "abstract": (
                    "Novel ether electrolyte enables LiFePO4 to reach "
                    "140 mAh/g at -20 deg C. Low viscosity is the key."
                ),
            },
            {
                "title": "Interface-limited kinetics in LFP at low temperature",
                "year": 2024,
                "abstract": (
                    "Rate-limiting step at low temperature is charge transfer, "
                    "not diffusion. Carbon coating shows negligible improvement "
                    "below -20 deg C."
                ),
            },
        ]
        print(f"  检索到 {len(self.papers)} 篇论文")
        for p in self.papers:
            print(f"    - [{p['year']}] {p['title']}")

    # ── 阶段 2: 信息抽取 ──────────────────────────────────────

    def extract_knowledge(self):
        """从论文摘要中抽取结构化知识。"""
        print(f"\n[阶段 2] 信息抽取")
        system_prompt = (
            "你是材料科学信息抽取专家。从摘要中抽取材料、性能、方法，"
            "输出 JSON：{\"materials\": [...], \"properties\": [...], \"methods\": [...]}"
        )
        for paper in self.papers:
            prompt = f"从以下摘要抽取结构化信息：\n\n{paper['abstract']}"
            try:
                result = llm_call_json(prompt, system=system_prompt, temperature=0.1)
                result["source"] = paper["title"]
                self.extractions.append(result)
                n_mat = len(result.get("materials", []))
                n_prop = len(result.get("properties", []))
                print(f"  ✓ {paper['title'][:40]}... → {n_mat} 材料, {n_prop} 性能")
            except Exception as e:
                print(f"  ✗ {paper['title'][:40]}... → 抽取失败: {e}")

    # ── 阶段 3: Gap 发现 ──────────────────────────────────────

    def discover_gaps(self):
        """对比分析论文，发现 Research Gap。"""
        print(f"\n[阶段 3] Gap 发现")
        abstracts = "\n".join(
            f"[{i+1}] {p['title']}: {p['abstract']}"
            for i, p in enumerate(self.papers)
        )
        system_prompt = (
            "你是研究分析专家。对比论文找出 Research Gap，输出 JSON："
            "{\"gaps\": [{\"type\": \"...\", \"title\": \"...\", \"description\": \"...\"}]}"
        )
        prompt = f"对比以下论文，找出 Research Gap：\n\n{abstracts}"
        try:
            result = llm_call_json(prompt, system=system_prompt, temperature=0.3)
            self.gaps = result.get("gaps", [])
            print(f"  发现 {len(self.gaps)} 个 Gap:")
            for g in self.gaps:
                print(f"    - [{g.get('type', '?')}] {g.get('title', 'N/A')}")
        except Exception as e:
            print(f"  Gap 发现失败: {e}")

    # ── 阶段 4: 报告生成 ──────────────────────────────────────

    def generate_report(self):
        """基于 Gap 分析生成综述报告。"""
        print(f"\n[阶段 4] 生成报告")
        gap_summary = "\n".join(
            f"- [{g.get('type', '?')}] {g.get('title', '')}: {g.get('description', '')}"
            for g in self.gaps
        )
        prompt = (
            f"请基于以下 Research Gap 分析，写一份简短的综述报告（500 字以内），"
            f"包含：引言、现状分析、Gap 总结、未来展望。\n\n"
            f"主题：{self.topic}\n\nGap 清单：\n{gap_summary}"
        )
        try:
            self.report = llm_call(
                prompt,
                system="你是材料科学领域的学术写作专家。",
                temperature=0.7,
            )
            print(f"  报告生成完成，共 {len(self.report)} 字")
        except Exception as e:
            self.report = f"报告生成失败: {e}"
            print(f"  {self.report}")

    # ── 端到端运行 ────────────────────────────────────────────

    def run(self):
        """运行完整 pipeline。"""
        print("=" * 55)
        print(f"  LiteratureAgent Pipeline")
        print(f"  主题: {self.topic}")
        print("=" * 55)

        self.search_literature()
        self.extract_knowledge()
        self.discover_gaps()
        self.generate_report()

        # 输出最终报告
        print("\n" + "=" * 55)
        print("  最终报告")
        print("=" * 55)
        print(self.report)

        # 保存报告
        report_path = "pipeline_report.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(self.report)
        print(f"\n报告已保存至: {report_path}")

        return self.report


def main():
    topic = "锂电池正极材料低温性能研究"
    agent = LiteratureAgent(topic)
    agent.run()


if __name__ == "__main__":
    main()
