"""
第11课：MinerU 批量解析
遍历文件夹，批量提交 PDF 到 MinerU，支持断点续传
"""
import sys, os, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from mineru_parse import submit_batch, wait_batch, download_and_extract

MINERU_TOKEN = os.environ.get("MINERU_TOKEN", "")
PDF_DIR = os.environ.get("PDF_DIR", "pdfs")
PROGRESS_FILE = "batch_progress.json"


def load_progress() -> dict:
    return json.loads(Path(PROGRESS_FILE).read_text("utf-8")) if os.path.exists(PROGRESS_FILE) else {}

def save_progress(progress: dict):
    Path(PROGRESS_FILE).write_text(json.dumps(progress, ensure_ascii=False, indent=2), "utf-8")

def main():
    if not MINERU_TOKEN:
        print("请设置环境变量 MINERU_TOKEN"); return
    pdfs = sorted(Path(PDF_DIR).glob("*.pdf"))
    if not pdfs:
        print(f"在 {PDF_DIR} 中未找到 PDF"); return
    print(f"=== MinerU 批量解析 ===\n共 {len(pdfs)} 个 PDF\n")
    progress = load_progress()
    done_ids = {k for k, v in progress.items() if v.get("status") == "done"}
    # 过滤已完成的文件
    pending = []
    for p in pdfs:
        did = p.stem[:128]
        if did in done_ids:
            print(f"  [跳过] {p.name}")
        else:
            pending.append({"path": str(p), "data_id": did})
    if not pending:
        print("全部已完成！"); return
    print(f"\n待解析: {len(pending)} 个\n{'-'*40}")
    # 每批最多 50 个
    for i in range(0, len(pending), 50):
        batch = pending[i:i+50]
        print(f"\n[批次 {i//50+1}] 提交 {len(batch)} 个文件...")
        try:
            result = submit_batch(batch, token=MINERU_TOKEN)
            print(f"  batch_id: {result['batch_id']}")
            for did, info in result["uploads"].items():
                print(f"  上传 {did}: {'成功' if info['uploaded'] else '失败: '+str(info.get('err'))}")
            print("  等待解析...")
            items = wait_batch(result["batch_id"], MINERU_TOKEN, timeout=600)
            for item in items:
                did = item.get("data_id", "")
                if item.get("state") == "done" and item.get("full_zip_url"):
                    download_and_extract(item["full_zip_url"], Path(PDF_DIR) / f"{did}_mineru")
                    progress[did] = {"status": "done"}
                    print(f"  [完成] {did}")
                elif item.get("state") == "failed":
                    progress[did] = {"status": "failed", "error": item.get("err_msg")}
                    print(f"  [失败] {did}: {item.get('err_msg')}")
            save_progress(progress)
        except Exception as e:
            print(f"  异常: {e}"); save_progress(progress)
    done_n = sum(1 for v in progress.values() if v.get("status") == "done")
    fail_n = sum(1 for v in progress.values() if v.get("status") == "failed")
    print(f"\n{'='*40}\n成功: {done_n}  失败: {fail_n}\n进度: {PROGRESS_FILE}")

if __name__ == "__main__":
    main()
