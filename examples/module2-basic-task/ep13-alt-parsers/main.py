"""
第13课：备选方案对比
演示用不同方式解析 PDF，对比 fitz 和 pdfplumber 的优劣
"""
from __future__ import annotations

import sys, os

try:
    import fitz
except ImportError:
    fitz = None
try:
    import pdfplumber
except ImportError:
    pdfplumber = None

SAMPLE_PDF = os.environ.get("SAMPLE_PDF", "sample.pdf")


def extract_with_fitz(pdf_path: str) -> dict | None:
    """用 PyMuPDF 提取文本"""
    if not fitz:
        print("[fitz] 未安装，跳过"); return None
    doc = fitz.open(pdf_path)
    text = "\n".join(p.get_text("text") for p in doc)
    doc.close()
    return {"tool": "PyMuPDF (fitz)", "chars": len(text), "tables": "-", "preview": text[:400]}


def extract_with_pdfplumber(pdf_path: str) -> dict | None:
    """用 pdfplumber 提取文本和表格"""
    if not pdfplumber:
        print("[pdfplumber] 未安装，跳过 (pip install pdfplumber)"); return None
    texts, tables_n = [], 0
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            texts.append(page.extract_text() or "")
            tables = page.extract_tables()
            if tables: tables_n += len(tables)
    text = "\n".join(texts)
    return {"tool": "pdfplumber", "chars": len(text), "tables": tables_n, "preview": text[:400]}


def main():
    if not os.path.exists(SAMPLE_PDF):
        print(f"未找到 {SAMPLE_PDF}，请设置 SAMPLE_PDF"); return

    print(f"=== PDF 解析工具对比 ===\n文件: {SAMPLE_PDF}\n")
    results = []

    for name, fn in [("PyMuPDF", extract_with_fitz), ("pdfplumber", extract_with_pdfplumber)]:
        print(f"[{name}] 提取中...")
        r = fn(SAMPLE_PDF)
        if r:
            results.append(r)
            print(f"  字符数:{r['chars']}  表格:{r['tables']}")
            print(f"  预览: {r['preview'][:200]}\n")

    if len(results) < 2:
        print("\n提示: pip install PyMuPDF pdfplumber 以获得完整对比")
        return

    # 对比表格
    print(f"\n{'='*50}\n{'工具':<18} {'字符数':<10} {'表格数':<10}")
    print("-" * 38)
    for r in results:
        print(f"{r['tool']:<18} {r['chars']:<10} {r['tables']:<10}")

    print(f"\n各工具特点:")
    print("  PyMuPDF    : 速度快，文本好，表格/公式弱")
    print("  pdfplumber : 表格提取强，速度较慢")
    print("  MinerU     : 全能型，公式/表格/图片均佳，需联网")


if __name__ == "__main__":
    main()
