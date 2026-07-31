# data/

示例数据与运行产物目录。

## 入库文件

- `extraction_schema.json` — 知识抽取的字段 Schema（模块二·第 19 期）
- `gap_types.json` — Research Gap 类型定义（模块二·第 24 期）

## 不入库文件（本地生成，已被 .gitignore 排除）

- `*.pdf` — 论文原文，涉及版权，请自行放入。教程示例默认从这里读取待解析的 PDF。
- `*.db` / `*.sqlite` — 由抽取流程生成的知识库，可由代码复现，不入库。

复现时把你要解析的论文 PDF 放到本目录，再运行 `examples/module2-basic-task/` 下对应的脚本即可。
