# 从 0 开始构建材料科学文献驱动的科学发现智能体

> 配套教程系列：**从零搭建一个能自主检索文献、解析 PDF、抽取知识、识别 Research Gap 并生成调研报告的科学发现智能体**
> 公众号：**小黄的材料AI Lab**

---

## 项目简介

本仓库是教程系列「**从 0 开始构建材料科学文献驱动的科学发现智能体**」的配套代码。

教程共 **64 期**，分为五大模块，从 LLM 基础调用一路搭到完整的文献调研 Agent，再扩展到构效关系发现、模拟方法、合成路线三个进阶方向。采用 **概念讲解 + 可运行代码** 的方式，面向材料领域研究生撰写。

完整目录见 [docs/教程系列总目录.md](docs/教程系列总目录.md)。

## 教程模块一览

| 模块 | 内容 | 期数 |
|---|---|---|
| 一 | LLM 与 Agent 基础认知 | 01–08 |
| 二 | 核心任务·文献调研 Agent（MinerU / Sciverse / 知识抽取 / Gap 识别 / 报告生成） | 09–30 |
| 三 | 进阶方向 A·构效关系发现 | 31–44 |
| 四 | 进阶方向 B·模拟方法创新 | 45–54 |
| 五 | 进阶方向 C·合成路线与工艺设计 | 55–64 |

## 仓库结构

```
-aigo-tutorial/
├── README.md
├── .env.example                # 环境变量模板（复制为 .env 后填入自己的 key）
├── .gitignore
├── requirements-base.txt       # 基础依赖
├── src/                        # 可复用的智能体核心库
│   ├── llm_call.py             # LLM 调用封装（DeepSeek / OpenAI 兼容）
│   ├── mineru_parse.py         # MinerU PDF 解析封装
│   ├── sciverse_client.py      # Sciverse 文献检索封装
│   ├── test_sciverse_api.py    # 检索连通性冒烟测试
│   └── config.json.example     # MinerU token 配置模板
├── examples/                   # 每期可运行示例，按模块/期号组织
│   ├── module1-llm-agent/
│   ├── module2-basic-task/
│   ├── module3-route-a/
│   ├── module4-route-b/
│   └── module5-route-c/
├── docs/                       # 教程文档
│   └── 教程系列总目录.md
└── data/                       # 示例数据、schema、知识库（大文件/版权 PDF 不入库）
    ├── extraction_schema.json
    └── gap_types.json
```

> 部分纯概念篇没有对应代码，`examples/` 只收录有可运行脚本的期。每个 episode 目录含 `main.py`、`README.md`、`requirements.txt`。

## 环境配置

- **Python** 3.11+（推荐 conda 管理）
- **操作系统** Windows / macOS / Linux 均可

### 快速开始

```bash
git clone https://github.com/RocHunag1996/-aigo-tutorial.git
cd -aigo-tutorial

conda create -n aigo python=3.11 -y
conda activate aigo

pip install -r requirements-base.txt

# 配置密钥：复制模板后填入你自己的 key
cp .env.example .env
# 然后编辑 .env，填入 DEEPSEEK_API_KEY / SCIVERSE_API_KEY / MINERU_TOKEN
```

### 运行某一期示例

```bash
# 示例的 main.py 会自动把 src/ 加入 import 路径
python examples/module2-basic-task/ep15-sciverse-api/main.py
```

代码通过环境变量读取密钥。运行前请先 `export`（或在 `.env` 中填好后由 `run_with_key.py` 载入）：

```bash
export DEEPSEEK_API_KEY=你的key
export SCIVERSE_API_KEY=你的key
export MINERU_TOKEN=你的token
```

## 需要用到的 API

| 服务 | 用途 | 获取方式 |
|---|---|---|
| DeepSeek API | LLM 调用 | [platform.deepseek.com](https://platform.deepseek.com) |
| MinerU | PDF 解析 | [mineru.net](https://mineru.net) 注册获取 token |
| Sciverse | 文献检索 | [sciverse.net](https://sciverse.net) 注册获取 API key |
| Materials Project | 材料数据（方向 A） | [materialsproject.org](https://materialsproject.org) 注册 |

> ⚠️ **切勿把任何真实密钥提交到仓库。** 所有 key 通过 `.env` / 环境变量注入，`.env` 与 `src/config.json` 已被 `.gitignore` 排除。

## 更新节奏

- **模块一 + 模块二（核心任务）**：每周 2–3 篇，约 3–4 个月
- **模块三至五（三个进阶方向）**：每周 1–2 篇，交替发布

关注公众号 **小黄的材料AI Lab** 获取每期图文推送。

## 问题反馈

运行代码遇到问题，欢迎在 [Issues](https://github.com/RocHunag1996/-aigo-tutorial/issues) 提问。

## License

MIT
