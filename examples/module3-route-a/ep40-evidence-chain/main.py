"""
AIGO 教程系列 - 路线 A·构效关系发现
ep40-evidence-chain: 文献证据链

用 Sciverse 检索相关文献，与计算结果对比，构建证据链。
演示如何将计算预测与文献数据交叉验证。
"""
import sys
from pathlib import Path
import os
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
class EvidenceNode:
    """证据链中的一个节点。"""
    def __init__(self, source_type, material, claim, confidence=0.5, reference=None):
        self.source_type = source_type  # "计算" / "文献" / "实验"
        self.material = material
        self.claim = claim
        self.confidence = confidence    # 置信度 0-1
        self.reference = reference

    def __repr__(self):
        return f"[{self.source_type}] {self.material}: {self.claim} (置信度={self.confidence:.1f})"


class EvidenceChain:
    """证据链管理器：收集和交叉验证多源证据。"""

    def __init__(self):
        self.nodes = []

    def add_computation(self, material, property_name, value, method="DFT"):
        """添加计算证据。"""
        node = EvidenceNode(
            source_type="计算",
            material=material,
            claim=f"{property_name} = {value} (方法: {method})",
            confidence=0.7,
            reference=f"{method} 计算",
        )
        self.nodes.append(node)
        return node

    def add_literature(self, material, property_name, value, paper_title, year):
        """添加文献证据。"""
        node = EvidenceNode(
            source_type="文献",
            material=material,
            claim=f"{property_name} = {value}",
            confidence=0.8,
            reference=f"{paper_title} ({year})",
        )
        self.nodes.append(node)
        return node

    def add_experimental(self, material, property_name, value, lab=""):
        """添加实验证据（最高置信度）。"""
        node = EvidenceNode(
            source_type="实验",
            material=material,
            claim=f"{property_name} = {value}",
            confidence=0.95,
            reference=f"实验测量{f' ({lab})' if lab else ''}",
        )
        self.nodes.append(node)
        return node

    def cross_validate(self, material, property_name, tolerance=0.2):
        """
        交叉验证：对同一材料的同一性质，比较不同来源的数据。
        """
        relevant = [
            n for n in self.nodes
            if n.material == material and property_name in n.claim
        ]

        if len(relevant) < 2:
            return {"status": "证据不足", "nodes": relevant}

        # 提取数值
        values = []
        for node in relevant:
            parts = node.claim.split("=")
            if len(parts) >= 2:
                try:
                    val_str = parts[1].split()[0].strip()
                    values.append(float(val_str))
                except ValueError:
                    pass

        if len(values) < 2:
            return {"status": "无法解析数值", "nodes": relevant}

        mean_val = sum(values) / len(values)
        max_dev = max(abs(v - mean_val) for v in values) / abs(mean_val) if mean_val != 0 else 0
        consistent = max_dev <= tolerance
        boost = min(0.1 * len(relevant), 0.2)

        return {
            "status": "一致" if consistent else "存在分歧",
            "mean": mean_val,
            "max_deviation": max_dev,
            "confidence_boost": boost if consistent else 0,
            "nodes": relevant,
        }

    def print_chain(self):
        """打印完整证据链。"""
        print("\n  证据链：")
        print("=" * 65)
        for i, node in enumerate(self.nodes, 1):
            print(f"  {i}. {node}")
            if node.reference:
                print(f"     来源: {node.reference}")
        print("=" * 65)


def search_literature_evidence(material, property_name):
    """用 Sciverse 检索文献证据。"""
    try:
        from sciverse_client import SciverseClient
        client = SciverseClient()
        results = client.search_papers(
            f"{material} {property_name}",
            year_from=2020,
            page_size=3,
        )
        return results.get("results", [])
    except Exception as e:
        print(f"  [!] Sciverse 检索失败: {e}，使用演示数据")
        return _demo_papers(material)


def _demo_papers(material):
    """演示文献数据。"""
    return [
        {
            "title": f"High thermoelectric performance in {material} (demo)",
            "publication_published_year": 2023,
            "abstract": f"We report ZT=1.5 in {material} through band engineering...",
        },
        {
            "title": f"First-principles study of {material} thermoelectrics (demo)",
            "publication_published_year": 2022,
            "abstract": f"DFT calculations predict optimal ZT~1.2 for {material}...",
        },
    ]


def main():
    print("=" * 65)
    print("  ep40 - 文献证据链构建")
    print("=" * 65)

    material = "Bi2Te3"
    property_name = "ZT"
    print(f"\n  目标: {material} 的 {property_name}")

    chain = EvidenceChain()

    # 1. 添加计算证据
    print("\n  Step 1: 添加计算预测...")
    chain.add_computation(material, "ZT", 1.3, method="DFT+BoltzTraP")
    chain.add_computation(material, "带隙", 0.33, method="HSE06")

    # 2. 检索文献证据
    print("\n  Step 2: 检索文献证据...")
    papers = search_literature_evidence(material, property_name)
    for paper in papers:
        title = paper.get("title", "N/A")
        year = paper.get("publication_published_year", "N/A")
        print(f"  - [{year}] {title}")
        chain.add_literature(material, "ZT", 1.5, title, year)

    # 3. 添加实验数据
    print("\n  Step 3: 添加实验验证数据...")
    chain.add_experimental(material, "ZT", 1.4, lab="MIT 实验组")

    # 4. 打印证据链
    chain.print_chain()

    # 5. 交叉验证
    print(f"\n  Step 4: 交叉验证 {material} 的 {property_name}...")
    result = chain.cross_validate(material, property_name, tolerance=0.3)
    print(f"  验证状态: {result['status']}")
    if "mean" in result:
        print(f"  平均值: {result['mean']:.2f}")
        print(f"  最大偏差: {result['max_deviation']:.1%}")
        print(f"  置信度提升: +{result['confidence_boost']:.1f}")

    print(f"\n  证据链构建要点：")
    print("  - 多源交叉验证提高结论可靠性")
    print("  - 计算预测 + 文献支撑 + 实验验证 = 完整证据")
    print("  - 分歧数据不是坏事，可能揭示新的物理机制")


if __name__ == "__main__":
    main()
