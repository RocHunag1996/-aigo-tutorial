"""
第10课：MinerU 精准 API 实战
演示完整流程：提交 -> 轮询 -> 下载 -> 查看结果
"""
import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from mineru_parse import parse_pdf

# 从环境变量读取 token 和 PDF 路径
MINERU_TOKEN = os.environ.get("MINERU_TOKEN", "")
SAMPLE_PDF = os.environ.get("SAMPLE_PDF", "sample.pdf")


def main():
    if not MINERU_TOKEN:
        print("请设置环境变量 MINERU_TOKEN")
        print("示例: set MINERU_TOKEN=your_token_here")
        return

    if not os.path.exists(SAMPLE_PDF):
        print(f"未找到 {SAMPLE_PDF}，请设置环境变量 SAMPLE_PDF")
        return

    print(f"=== MinerU 精准 API 解析 ===")
    print(f"PDF 文件: {SAMPLE_PDF}")
    print(f"输出目录: {SAMPLE_PDF}_mineru/\n")

    # 调用 parse_pdf，内部完成：提交上传 -> 轮询等待 -> 下载解压
    print("[1/3] 提交解析任务...")
    result = parse_pdf(
        SAMPLE_PDF,
        token=MINERU_TOKEN,
        language="ch",       # 中英文混合
    )

    print("[2/3] 解析完成！")
    print(f"  batch_id : {result['batch_id']}")
    print(f"  输出目录 : {result['output_dir']}")
    print(f"  图片数量 : {result['image_count']}")

    # 读取并展示 Markdown 结果
    print("[3/3] 查看解析结果\n")

    if result["md_path"] and result["md_path"].exists():
        md_text = result["md_path"].read_text(encoding="utf-8")
        print(f"--- Markdown 前1000字符 ---")
        print(md_text[:1000])
        print(f"--- [全文共 {len(md_text)} 字符] ---")
    else:
        print("未找到 full.md 文件")

    if result["html_path"] and result["html_path"].exists():
        print(f"\nHTML 版本已生成: {result['html_path']}")

    if result["images_dir"] and result["images_dir"].exists():
        imgs = list(result["images_dir"].glob("*"))
        print(f"\n提取的图片文件 ({len(imgs)} 张):")
        for img in imgs[:5]:
            print(f"  - {img.name}")
        if len(imgs) > 5:
            print(f"  ... 还有 {len(imgs)-5} 张")


if __name__ == "__main__":
    main()
