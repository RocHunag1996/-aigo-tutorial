"""
AIGO 教程系列 - 路线 C·合成路线与工艺设计
ep59-route-generator: 合成路线生成 Agent
结合知识库与 LLM 推理，自动规划多步合成路线
"""

import sys
from pathlib import Path
import os
import json
import sqlite3
import tempfile

# 导入共享 LLM 模块
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from llm_call import llm_call_json


ROUTE_GEN_PROMPT = """你是材料合成路线规划 Agent。给定目标材料和可用前驱体库，设计合成路线。

目标材料：{target}
可用前驱体库：{precursors}
知识库参考（相似体系合成条件）：
{kb_context}

请设计一条完整的多步合成路线，返回 JSON：
{{
    "target": "{target}",
    "route_name": "路线名称",
    "steps": [
        {{
            "step_id": 1,
            "action": "操作描述",
            "reagents": ["试剂1", "试剂2"],
            "temperature_c": 数字或null,
            "time_hours": 数字或null,
            "expected_intermediate": "中间产物",
            "notes": "注意事项"
        }}
    ],
    "total_steps": 数字,
    "estimated_yield": "预估产率",
    "safety_notes": "安全注意事项"
}}"""


class SynthesisRouteGenerator:
    """合成路线生成 Agent"""

    def __init__(self, kb_conn: sqlite3.Connection = None):
        self.kb_conn = kb_conn
        self.history = []  # 生成历史

    def query_kb(self, material_keyword: str) -> str:
        """从知识库查询相似体系的合成条件"""
        if not self.kb_conn:
            return "（知识库未连接）"

        try:
            cursor = self.kb_conn.cursor()
            cursor.execute("""
                SELECT material_name, synthesis_method, temperature_c,
                       time_hours, precursors
                FROM synthesis_records
                WHERE material_name LIKE ?
                LIMIT 3
            """, (f"%{material_keyword}%",))

            rows = cursor.fetchall()
            if not rows:
                return "（知识库中无相似记录）"

            context = ""
            for row in rows:
                context += f"- {row[0]}: {row[1]}, {row[2]}°C, {row[3]}h\n"
            return context
        except Exception:
            return "（知识库查询失败）"

    def generate_route(self, target: str, available_precursors: list = None) -> dict:
        """生成合成路线"""
        if available_precursors is None:
            available_precursors = [
                "Li2CO3", "La2O3", "ZrO2", "TiO2", "Ba(OH)2",
                "SrCO3", "Nb2O5", "Ta2O5", "Al2O3", "SiO2",
                "HNO3", "NaOH", "NH3·H2O", "柠檬酸", "乙二醇"
            ]

        # 查询知识库
        kb_context = self.query_kb(target.split("(")[0].strip())

        try:
            result = llm_call_json(
                ROUTE_GEN_PROMPT.format(
                    target=target,
                    precursors=", ".join(available_precursors),
                    kb_context=kb_context
                ),
                system="你是材料合成路线规划 Agent，只返回 JSON。"
            )
            self.history.append(result)
            return result
        except Exception as e:
            print(f"  [警告] LLM 调用失败: {e}")
            return None

    def print_route(self, route: dict):
        """格式化打印合成路线"""
        if not route:
            print("  路线生成失败")
            return

        print(f"\n{'='*50}")
        print(f"目标: {route.get('target', 'N/A')}")
        print(f"路线: {route.get('route_name', 'N/A')}")
        print(f"总步数: {route.get('total_steps', 'N/A')}")
        print(f"{'='*50}")

        for step in route.get("steps", []):
            sid = step.get("step_id", "?")
            action = step.get("action", "")
            temp = step.get("temperature_c")
            time_h = step.get("time_hours")

            print(f"\n  步骤 {sid}: {action}")
            reagents = step.get("reagents", [])
            if reagents:
                print(f"    试剂: {', '.join(reagents)}")
            if temp:
                print(f"    温度: {temp}°C")
            if time_h:
                print(f"    时间: {time_h}h")
            intermediate = step.get("expected_intermediate")
            if intermediate:
                print(f"    中间产物: {intermediate}")
            notes = step.get("notes")
            if notes:
                print(f"    注意: {notes}")

        safety = route.get("safety_notes")
        if safety:
            print(f"\n  [安全] {safety}")


def demo_generation():
    """演示合成路线生成"""
    print("=" * 60)
    print("演示：生成 LLZO 固态电解质的合成路线")
    print("=" * 60)

    generator = SynthesisRouteGenerator()

    # 尝试 LLM 生成
    route = generator.generate_route("Li7La3Zr2O12 (LLZO)")

    if route:
        generator.print_route(route)
    else:
        # 演示模式
        print("\n[演示模式] 预期合成路线：")
        demo_route = {
            "target": "Li7La3Zr2O12 (LLZO)",
            "route_name": "溶胶-凝胶法合成 LLZO",
            "steps": [
                {
                    "step_id": 1,
                    "action": "配制金属盐前驱体溶液",
                    "reagents": ["LiNO3", "La(NO3)3", "Zr(O-nBu)4"],
                    "temperature_c": None,
                    "time_hours": None,
                    "expected_intermediate": "混合盐溶液",
                    "notes": "按 Li:La:Zr = 7.15:3:2 称量（Li 过量 5%）"
                },
                {
                    "step_id": 2,
                    "action": "加入柠檬酸络合，80°C 水浴搅拌成凝胶",
                    "reagents": ["柠檬酸"],
                    "temperature_c": 80,
                    "time_hours": 3,
                    "expected_intermediate": "湿凝胶",
                    "notes": "柠檬酸:金属离子 = 1.5:1"
                },
                {
                    "step_id": 3,
                    "action": "120°C 干燥过夜得到干凝胶",
                    "reagents": [],
                    "temperature_c": 120,
                    "time_hours": 12,
                    "expected_intermediate": "干凝胶前驱体",
                    "notes": "真空干燥箱"
                },
                {
                    "step_id": 4,
                    "action": "750°C 煅烧分解有机物，形成 LLZO 相",
                    "reagents": [],
                    "temperature_c": 750,
                    "time_hours": 6,
                    "expected_intermediate": "LLZO 粉末",
                    "notes": "升温速率 5°C/min，空气气氛"
                }
            ],
            "total_steps": 4,
            "estimated_yield": "~85%",
            "safety_notes": "Zr(O-nBu)4 遇水剧烈反应，需在手套箱中操作"
        }
        generator.print_route(demo_route)


def main():
    print("ep59 - 合成路线生成 Agent")
    print("=" * 60)

    demo_generation()

    print("\n" + "=" * 60)
    print("Agent 工作流程：")
    print("""
    1. 接收目标材料名称
    2. 查询知识库（ep57）获取相似体系合成条件
    3. 调用 LLM 生成合成路线
    4. 校验路线可行性（前驱体是否在库中）
    5. 输出格式化路线方案
    6. 记录到生成历史供后续参考
    """)


if __name__ == "__main__":
    main()
