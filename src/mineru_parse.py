"""MinerU PDF 解析工具（精准 API v4）。

可当脚本用，也可被 import。
不依赖 config.py，token 从参数或环境变量传入。

用法（命令行）：
    python mineru_parse.py <pdf_path> [--token <token>] [--out <dir>]

用法（import）：
    from mineru_parse import parse_pdf
    result = parse_pdf("paper.pdf", token="...")
    # result = {"md_path": "...", "html_path": "...", "images_dir": "...", "zip_dir": "..."}
"""
from __future__ import annotations

import argparse
import io
import json
import os
import sys
import time
import zipfile
from pathlib import Path

import requests

MINERU_BASE = "https://mineru.net/api/v4"


# ── 底层 API ──────────────────────────────────────────────

def _headers(token: str) -> dict:
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }


def submit_batch(
    files: list[dict],
    *,
    token: str,
    model_version: str = "vlm",
    enable_formula: bool = True,
    enable_table: bool = True,
    language: str = "ch",
    extra_formats: list[str] | None = None,
) -> dict:
    """申请上传链接 + PUT 上传文件。返回 {"batch_id": ..., "uploads": {data_id: {...}}}。

    files: [{"path": Path, "data_id": str, "is_ocr": bool (可选)}]
    """
    if not files:
        raise ValueError("files 为空")
    if len(files) > 50:
        raise ValueError(f"单批最多 50 个，当前 {len(files)}")

    payload = {
        "files": [
            {
                "name": Path(f["path"]).name,
                "data_id": f["data_id"],
                **({"is_ocr": True} if f.get("is_ocr") else {}),
            }
            for f in files
        ],
        "model_version": model_version,
        "enable_formula": enable_formula,
        "enable_table": enable_table,
        "language": language,
    }
    if extra_formats:
        payload["extra_formats"] = extra_formats

    r = requests.post(
        f"{MINERU_BASE}/file-urls/batch",
        headers=_headers(token),
        json=payload,
        timeout=60,
    )
    r.raise_for_status()
    body = r.json()
    if body.get("code") != 0:
        raise RuntimeError(f"申请上传URL失败: {body}")

    batch_id = body["data"]["batch_id"]
    upload_urls = body["data"]["file_urls"]
    if len(upload_urls) != len(files):
        raise RuntimeError(f"上传URL数量不匹配: 申请{len(files)} 返回{len(upload_urls)}")

    uploads = {}
    for spec, url in zip(files, upload_urls):
        info = {"url": url, "uploaded": False, "err": None}
        try:
            with open(spec["path"], "rb") as fp:
                up = requests.put(url, data=fp, timeout=300)
            if up.status_code == 200:
                info["uploaded"] = True
            else:
                info["err"] = f"HTTP {up.status_code}: {up.text[:200]}"
        except Exception as e:
            info["err"] = repr(e)
        uploads[spec["data_id"]] = info

    return {"batch_id": batch_id, "uploads": uploads}


def query_batch(batch_id: str, token: str) -> list:
    """返回 extract_result 列表。"""
    r = requests.get(
        f"{MINERU_BASE}/extract-results/batch/{batch_id}",
        headers=_headers(token),
        timeout=60,
    )
    r.raise_for_status()
    body = r.json()
    if body.get("code") != 0:
        raise RuntimeError(f"查询batch失败: {body}")
    return body["data"].get("extract_result", []) or []


def wait_batch(
    batch_id: str,
    token: str,
    *,
    poll_interval: int = 10,
    timeout: int = 600,
) -> list:
    """阻塞轮询，直到所有文件 done/failed 或超时。"""
    terminal = {"done", "failed"}
    start = time.time()
    while True:
        results = query_batch(batch_id, token)
        if results and all(item.get("state") in terminal for item in results):
            return results
        if time.time() - start > timeout:
            raise TimeoutError(f"batch {batch_id} 等待超过 {timeout}s")
        time.sleep(poll_interval)


def download_and_extract(zip_url: str, target_dir: Path) -> Path:
    """下载 zip 并解压到 target_dir/。"""
    target_dir.mkdir(parents=True, exist_ok=True)
    r = requests.get(zip_url, timeout=300)
    r.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
        zf.extractall(target_dir)
    return target_dir


# ── 高层封装：单个 PDF 一键解析 ──────────────────────────────

def parse_pdf(
    pdf_path,
    token=None,
    out_dir=None,
    data_id=None,
    model_version="vlm",
    language="ch",
    poll_interval=10,
    timeout=600,
):
    """解析单个 PDF，返回结果路径字典。

    返回:
        {
            "batch_id": str,
            "md_path": Path,        # full.md 路径
            "html_path": Path,      # full.html 路径（如存在）
            "images_dir": Path,     # images/ 目录
            "output_dir": Path,     # 整个解压目录
            "image_count": int,
        }
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(pdf_path)

    if out_dir is None:
        out_dir = pdf_path.parent / "{}_mineru".format(pdf_path.stem)
    out_dir = Path(out_dir)

    if data_id is None:
        data_id = pdf_path.stem
    # data_id 只能含字母数字._-，<=128
    data_id = "".join(c if c.isalnum() or c in "._-" else "_" for c in data_id)[:128]

    # 1) 提交 + 上传
    spec = {"path": str(pdf_path), "data_id": data_id}
    sub = submit_batch(
        [spec],
        token=token,
        model_version=model_version,
        enable_formula=True,
        enable_table=True,
        language=language,
        extra_formats=["html"],
    )
    batch_id = sub["batch_id"]

    upload_info = sub["uploads"].get(data_id, {})
    if not upload_info.get("uploaded"):
        raise RuntimeError("上传失败: {}".format(upload_info.get("err")))

    # 2) 轮询
    items = wait_batch(batch_id, token, poll_interval=poll_interval, timeout=timeout)
    done = [it for it in items if it.get("state") == "done"]
    failed = [it for it in items if it.get("state") == "failed"]

    if failed and not done:
        errs = [it.get("err_msg", "unknown") for it in failed]
        raise RuntimeError("解析失败: {}".format("; ".join(errs)))
    if not done:
        raise RuntimeError("解析未返回任何结果")

    # 3) 下载解压
    zip_url = done[0]["full_zip_url"]
    download_and_extract(zip_url, out_dir)

    # 4) 定位关键文件
    md_path = out_dir / "full.md"
    html_path = out_dir / "full.html"
    images_dir = out_dir / "images"

    result = {
        "batch_id": batch_id,
        "output_dir": out_dir,
        "md_path": md_path if md_path.exists() else None,
        "html_path": html_path if html_path.exists() else None,
        "images_dir": images_dir if images_dir.exists() else None,
    }

    # 统计图片数
    if result["images_dir"]:
        imgs = list(result["images_dir"].glob("*"))
        result["image_count"] = len(imgs)
    else:
        result["image_count"] = 0

    return result


# ── 命令行入口 ────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="MinerU PDF 解析（精准 API v4）")
    ap.add_argument("pdf", help="PDF 文件路径")
    ap.add_argument("--token", default=None,
                    help="MinerU API token（默认从环境变量 MINERU_TOKEN 读取）")
    ap.add_argument("--out", default=None, help="输出目录（默认 <pdf名>_mineru/）")
    ap.add_argument("--model", default="vlm", help="模型版本（默认 vlm）")
    ap.add_argument("--poll-interval", type=int, default=10)
    ap.add_argument("--timeout", type=int, default=600)
    args = ap.parse_args()

    token = args.token or os.environ.get("MINERU_TOKEN", "")
    if not token:
        # 尝试从 config.json 读取
        config_paths = [
            Path(__file__).parent / "config.json",
            Path.home() / ".mineru_config.json",
        ]
        for cp in config_paths:
            if cp.exists():
                try:
                    cfg = json.loads(cp.read_text(encoding="utf-8"))
                    keys = cfg.get("mineru_api_keys", [])
                    if keys:
                        token = keys[0]
                        print("[info] 从 {} 读取 token".format(cp))
                        break
                except Exception:
                    pass
    if not token:
        print("错误：未提供 token。请用 --token 参数或设置 MINERU_TOKEN 环境变量。")
        sys.exit(1)

    print("解析: {}".format(args.pdf))
    result = parse_pdf(
        args.pdf,
        token=token,
        out_dir=args.out,
        model_version=args.model,
        poll_interval=args.poll_interval,
        timeout=args.timeout,
    )
    print("\n完成！")
    print("  batch_id  : {}".format(result["batch_id"]))
    print("  输出目录  : {}".format(result["output_dir"]))
    print("  full.md   : {}".format(result["md_path"]))
    print("  full.html : {}".format(result["html_path"]))
    print("  图片数    : {}".format(result["image_count"]))
    if result["images_dir"]:
        print("  图片目录  : {}".format(result["images_dir"]))


if __name__ == "__main__":
    main()
