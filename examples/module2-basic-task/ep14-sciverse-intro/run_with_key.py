# 便捷本地运行：从仓库根 .env 载入 key 后执行 main（不含任何硬编码 key）
import os, sys
from pathlib import Path

root = Path(__file__).resolve().parents[3]
envf = root / '.env'
if envf.exists():
    for line in envf.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            os.environ.setdefault(k.strip(), v.strip())
sys.path.insert(0, os.path.dirname(__file__))
import main
main.main()
