"""
第9课：PDF解析为什么是难题
演示用 PyMuPDF(fitz) 提取文本的局限性：双栏混乱、表格丢失、公式消失
"""
import sys, os

try:
    import fitz  # PyMuPDF
except ImportError:
    print("请先安装 PyMuPDF: pip install PyMuPDF"); sys.exit(1)

SAMPLE_PDF = os.environ.get("SAMPLE_PDF", "sample.pdf")


def extract_and_show(pdf_path: str):
    """用 fitz 提取文本，展示常见问题"""
    doc = fitz.open(pdf_path)
    print(f"PDF 共 {len(doc)} 页\n")
    for i, page in enumerate(doc):
        print(f"{'='*50}\n第 {i+1} 页 ({page.rect.width:.0f}x{page.rect.height:.0f})")
        # 1. 直接提取文本 —— 双栏会混在一起
        text = page.get_text("text")
        print(f"\n【文本提取】前500字符:\n{text[:500]}\n[共 {len(text)} 字符]")
        # 2. 表格检测（fitz 能力有限）
        try:
            tables = page.find_tables()
            n_tables = len(tables.tables) if tables else 0
        except Exception:
            n_tables = 0
        print(f"【表格】检测到 {n_tables} 个")
        # 3. 图片
        print(f"【图片】{len(page.get_images())} 张")
        # 4. 公式 —— 公式通常以特殊字体存在，fitz 无法还原为 LaTeX
        fonts = set()
        for blk in page.get_text("dict")["blocks"]:
            for ln in blk.get("lines", []):
                for sp in ln.get("spans", []):
                    fonts.add(sp["font"])
        math_fonts = [f for f in fonts if any(k in f.lower()
                      for k in ["math","symbol","cmr","cmm","cmsy","stix"])]
        print(f"【公式字体】{math_fonts[:5]}")
        if i >= 2:
            break
    doc.close()


def show_layout_problem(pdf_path: str):
    """展示双栏布局问题：文本块位置暴露阅读顺序混乱"""
    doc = fitz.open(pdf_path)
    blocks = doc[0].get_text("blocks")
    doc.close()
    print(f"\n{'='*50}\n【双栏问题】第1页共 {len(blocks)} 个文本块:")
    for idx, b in enumerate(blocks[:8]):
        x0, y0, x1, y1 = b[:4]
        txt = b[4][:60].replace("\n", " ")
        print(f"  块{idx} ({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f}) | {txt}...")


def main():
    if not os.path.exists(SAMPLE_PDF):
        print(f"未找到 {SAMPLE_PDF}，请设置环境变量 SAMPLE_PDF"); return
    print("=== PDF 解析局限性演示 ===\n")
    extract_and_show(SAMPLE_PDF)
    show_layout_problem(SAMPLE_PDF)
    print(f"\n{'='*50}")
    print("总结：传统工具的问题")
    print("  1. 双栏/多栏文本顺序混乱")
    print("  2. 表格结构完全丢失")
    print("  3. 数学公式无法还原为 LaTeX")
    print("  4. 图片与文本的关系断裂")
    print("=> 需要 MinerU 等专业工具来解决！")


if __name__ == "__main__":
    main()
