# CAD Document Ingest

独立的标准 Agent Skill package，提供 **CAD Document Ingest Baseline 0.1.0**，将 CAD 文件与依赖转换为规定的事实、观察、说明及分层摘要文档。

仓库形式参考 `assembly-package-design`：安装的 Skill 仅含 Markdown 规范和模板；验证脚本与 CI 留在仓库层。包内不包含 CAD 应用、解析运行后端、第三方源库、凭据或预置模型。执行转换时使用目标环境实际可用的工具，不绑定某种文件扩展名或知识库。

## 安装与使用

将仓库中的 `skills/cad-document-ingest/` 整个目录复制到所用 Agent 的标准 skills 目录即可。也可以使用标准 [skills CLI](https://github.com/vercel-labs/skills) 从 [GitHub 仓库](https://github.com/yijunw-aiVersion/cad-document-ingest) 安装：

```bash
npx skills add yijunw-aiVersion/cad-document-ingest
npx skills add yijunw-aiVersion/cad-document-ingest --agent pi --skill cad-document-ingest --copy --yes
```

在本地仓库根目录检查可安装内容或安装本地版本：

```bash
npx skills add . --list
npx skills add . --agent pi --skill cad-document-ingest --copy --yes
```

CLI 默认安装到当前项目；用户级安装按实际需要添加 `--global`。私有仓库需要访问权限和可用的 Git 凭据。无需发布 npm package。安装不会自动安装 CAD 运行依赖。

Pi 会话加载后使用：

```text
/skill:cad-document-ingest 将这些 CAD 文件转换为五类中文文本文档，保留原生文件、依赖和真实预览，完成本地验收并交付到指定目录。
```

Codex 支持的显式调用形式：

```text
$cad-document-ingest 按我给的文档 schema 转换这些工程文件，并报告实际来源、未知字段和验收结果。
```

已有工程或知识库的目录、字段、模板和命名可以通过 profile 映射，不要求更换源文件格式。

## 默认交付

| 文档 | 作用 |
|---|---|
| `facts.json` | 可核查的源声明与计算事实 |
| `visual-observation.json` | 同版真实图像的观察与用途候选 |
| `asset.md` | 可读完整说明 |
| `.abstract.md` | L0 摘要 |
| `.overview.md` | L1 概览，默认与 asset.md 相同正文 |

原始 CAD、依赖与预览作为配套证据保留。用户指定格式优先于默认；五类文本代表默认信息分工，不限制整个交付只能有五个文件。只有本地门槛通过才报告合格交付；要求知识库入库时，还需真实发布、检索和回读检查。

## 内容

| 内容 | 文件 |
|---|---|
| Skill 入口与执行流程 | [SKILL.md](skills/cad-document-ingest/SKILL.md) |
| 10 条核心规则 | [baseline.md](skills/cad-document-ingest/references/baseline.md) |
| 五类文档、目录、字段与哈希契约 | [document-contract.md](skills/cad-document-ingest/references/document-contract.md) |
| 输入与目标适配方法 | [format-adapters.md](skills/cad-document-ingest/references/format-adapters.md) |
| 快照、观察、执行状态与本地验收 | [execution-evidence.md](skills/cad-document-ingest/references/execution-evidence.md) |
| 可选知识库发布与回读 | [publication.md](skills/cad-document-ingest/references/publication.md) |
| 可落实的验收用例 | [conformance.md](skills/cad-document-ingest/references/conformance.md) |
| 来源与旧工作流迁移映射 | [implementation-map.md](skills/cad-document-ingest/references/implementation-map.md) |
| 转换 profile 模板 | [CONVERSION-PROFILE.template.md](skills/cad-document-ingest/assets/CONVERSION-PROFILE.template.md) |
| 事实模板 | [FACTS.template.md](skills/cad-document-ingest/assets/FACTS.template.md) |
| 观察模板 | [VISUAL-OBSERVATION.template.md](skills/cad-document-ingest/assets/VISUAL-OBSERVATION.template.md) |
| L0/L1/说明生成模板 | [DOCUMENTS.template.md](skills/cad-document-ingest/assets/DOCUMENTS.template.md) |

## 仓库结构

```text
skills/cad-document-ingest/
  SKILL.md
  references/
  assets/
scripts/validate_skill.py       # 仓库维护，不随 Skill 安装
.github/workflows/validate.yml  # 仓库 CI，不随 Skill 安装
```

## 验证

```bash
python3 scripts/validate_skill.py
```

脚本检查目录/frontmatter、引用、自包含性、JSON 模板可解析性和 Markdown-only 安装内容。它不证明任何 CAD 后端或远端服务已支持某格式；实际转换按验收用例记录执行证据。CI 在临时项目中通过固定版本 skills CLI 检查发现与安装。

本次封装已通过内容验证、Skill Creator 格式验证，以及 skills CLI 1.7.0 在隔离临时 Pi 项目中的发现与复制安装检查。该版本实际复制安装到 `.pi/skills/cad-document-ingest/`；其他 CLI 版本以实际安装结果为准。未执行实际 CAD 转换或远端发布。

来源：用户提供的已有文件转换流程及独立设计 Skill 结构。提炼后维护通用转换规范；没有把原运行后端改名后声称具备跨格式能力。详细对应关系见迁移映射。
