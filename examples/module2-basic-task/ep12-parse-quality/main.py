"""
第12课：解析质量评估
对 MinerU 解析结果做自动化校验：公式、表格、图片、文本完整性
"""
import sys, os, re
from pathlib import Path

try:
    import fitz
except ImportError:
    fitz = None


def count_formulas(md: str) -> dict:
    inline = re.findall(r'\$[^$]+\$', md)
    block = re.findall(r'\$\$[^$]+\$\$', md)
    return {"inline": len(inline), "block": len(block), "total": len(inline)+len(block)}


def count_tables(md: str) -> int:
    in_table, n = False, 0
    for line in md.split("\n"):
        if line.strip().startswith("|"):
            if not in_table: n, in_table = n+1, True
        else:
            in_table = False
    return n


def count_image_refs(md: str) -> int:
    return len(re.findall(r'!\[.*?\]\(.*?\)', md))


def generate_report(pdf_path: str, result_dir: str):
    md_path = Path(result_dir) / "full.md"
    if not md_path.exists():
        print(f"未找到 {md_path}"); return
    md = md_path.read_text("utf-8")
    images_dir = Path(result_dir) / "images"
    actual_imgs = len(list(images_dir.glob("*"))) if images_dir.exists() else 0
    pdf_pages = len(fitz.open(pdf_path)) if fitz else -1

    print(f"=== 解析质量评估报告 ===")
    print(f"PDF: {pdf_path}  |  解析目录: {result_dir}\n")

    formulas = count_formulas(md)
    print(f"[公式] 行内:{formulas['inline']}  块级:{formulas['block']}  合计:{formulas['total']}")
    print(f"[表格] {count_tables(md)} 个")
    print(f"[图片] Markdown引用:{count_image_refs(md)}  实际文件:{actual_imgs}")
    print(f"[文本] PDF页数:{pdf_pages}  Markdown字符数:{len(md)}")

    # 综合评估
    print(f"\n{'='*40}\n[综合评估]")
    issues = []
    if formulas["total"] == 0 and ("equation" in md.lower() or "公式" in md):
        issues.append("可能遗漏公式")
    if count_tables(md) == 0 and "table" in md.lower():
        issues.append("可能遗漏表格")
    if count_image_refs(md) == 0 and actual_imgs > 0:
        issues.append("图片未正确引用")
    if pdf_pages > 0 and len(md) < pdf_pages * 50:
        issues.append("文本可能不完整")
    if issues:
        for issue in issues: print(f"  - {issue}")
    else:
        print("  解析质量良好")


def main():
    pdf = os.environ.get("SAMPLE_PDF", "sample.pdf")
    result = os.environ.get("MINERU_RESULT", "sample_mineru")
    if not os.path.exists(pdf):
        print(f"未找到 {pdf}，请设置 SAMPLE_PDF 和 MINERU_RESULT"); return
    generate_report(pdf, result)


if __name__ == "__main__":
    main()
