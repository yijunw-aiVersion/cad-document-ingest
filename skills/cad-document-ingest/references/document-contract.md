# 文档与数据契约

## 默认五类文本

默认 profile ID 为 `cad.document-publication.zh.v1`，facts schema 为 `cad.document-facts.v1`，observation schema 为 `cad.visual-observation.v1`。这些是本包定义的文档契约，与特定 CAD 软件或知识库内部 schema 无关。

| 文件 | 职责 | 来源 |
|---|---|---|
| `facts.json` | 身份、源格式、来源、单位/坐标、精确事实、诊断、边界 | 解析器、声明、可复现计算和源 manifest |
| `visual-observation.json` | 实际可见外形、审阅记录、用途候选、遮挡和未知 | 同版图像的实际审阅；包含源与图像绑定 |
| `asset.md` | 可读的完整资产说明 | facts 与 observation 的固定投影 |
| `.abstract.md` | L0：适合检索和快速判断的摘要 | 同版精确事实、可见外形、明确未知 |
| `.overview.md` | L1：字段、来源、观察和使用边界 | 与 asset.md 共用同一生成正文 |

默认 `asset.md` 和版本内 `.overview.md` 使用完全相同的 UTF-8 字节；一次生成后复制，避免分别撰写。L0 在 L1 中复用同一语义内容。严格遵循用户已有格式时，可以定义不同正文关系，并在 profile 记录一致性检查方法。

源文件不是被转换成了文本后就可以丢弃。保留其原后缀与字节、依赖闭包和实际预览。五类文本是文档角色计数，不是整个交付目录只能有五个物理文件。

## 建议目录

```text
<output>/objects/<category-slug>/<object-id>/
  .abstract.md                   # 可选：当前版本导航
  .overview.md                   # 可选：当前版本导航
  <version>/
    facts.json
    visual-observation.json
    asset.md
    .abstract.md
    .overview.md
    source/
      <entry-with-original-extension>
      <dependency-relative-paths>
    previews/
      <actual-preview-files>
<run>/
  conversion-profile.md
  inputs.json
  receipts/
  local-report.json
  remote-report.json             # 执行发布/核验时才有
```

`objects`、类别层、对象 ID、版本命名和 source 布局可以由目标规范替换。未知类别默认 `unknown`。ID 建议使用安全 ASCII token，保留原始名称到 ID 的映射；批量中的规范化碰撞必须解决后再生成。所有包内相对路径限制在所属根目录内，拒绝路径跳转和越界链接。

默认首次为 `v1`，后续版本由项目策略决定。可选父目录 L0 与当前版本 L0 同正文，父 L1 保持当前版本 L1 语义、将相对来源链接重写为版本路径，并追加当前版本导航；绝对 URI 模式可直接复用正文再追加导航。推进当前指针不能回退已有更新版本。父目录导航更新不改变历史版本。

## facts.json 最小语义

完整结构见 [事实模板](../assets/FACTS.template.md)。required 表示键必需，不意味着值总能获知。

| 字段 | 要求 |
|---|---|
| `schema_version`, `profile`, `object_id`, `version` | 必填，匹配当前 profile、manifest 和输出路径 |
| `title`, `category` | 保存原值与依据；未声明时 value 为 null、status 为 unknown |
| `source.format`, `source.format_version`, `source.entry_path` | 格式识别依据明确；格式版本未知可为 null |
| `source.files` | 主源和依赖列表，含相对 path、role、sha256；同路径不重复 |
| `source.manifest_sha256`, `source.dependency_status` | 对实际快照计算；complete / partial / unknown / not_applicable |
| `extraction` | 工具名、版本、配置/回执引用、支持范围、执行状态和损失 |
| `units`, `coordinate_system` | 声明原单位/坐标、规范化方法和原生到输出变换；未知不擅自设默认 |
| `geometry` | representation、status、方法、数值及适用范围；非三维输入可用自己的有量纲字段 |
| `interfaces` | status、items、依据；没有声明默认 unknown，空列表不能自行证明无接口 |
| `properties` | 有名有单位的源声明或计算值，以及字段级来源与方法 |
| `diagnostics`, `licenses`, `limitations` | 保存损失、未知、源许可证信息和结论边界 |

事实状态使用 `known / unknown / partial / unsupported / not_applicable`。数值未获知时为 null，并记录 reason；不得用 0 代表未知。已知不存在可以是 known 加空集合，但需有证明完整枚举的来源。NaN/Infinity 不能进入标准 JSON。

每项输出数值必须能指向源文件/实体标识、适配方法或计算回执。预览尺寸不进入精确数值字段。三维 profile 的 bbox 要区分 min/max、extent 和原生坐标系；包络算法必须说明是精确极值、离散网格估计还是保守边界及误差。

## 源 manifest 哈希

按 path 的 Unicode 码点顺序排序 `source.files`，每项仅以 `path`、`role`、`sha256` 三键参加哈希。path 使用区分大小写的 POSIX 相对路径且无重复或跳转。JSON 规范化为 `ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False` 的 UTF-8 字节，不加末尾换行；计算 SHA-256。文件自身 sha256 针对原字节。

manifest 包含实际使用的主源、工程依赖及影响解析/渲染的源库数据。工具版本和配置记录在 extraction/receipt 内，并另算实际配置哈希。profile 快照的 SHA-256 针对本次保存的原字节。观察与最终运行报告保存 profile 哈希，不能只绑定一个可变 profile 名字。

## 观察与摘要

默认图像必需。observation 固定 `object_id`、`version`、`source_manifest_sha256`、`profile_sha256`，并列出真实看过的图像 path/sha256。required profile 至少一张匹配的图，review_status 为 reviewed、reviewer 和 visible_shape 非空；若不能合理推断用途，purpose_candidate 为 null 并写明原因。

optional profile 未审阅可保留 not_run，并在正文说明缺口；not_applicable profile 写 skipped 与理由。任何模式都不能把未观察内容写成可见事实。

L0 至少含身份、源标题/类别、可见外形或未审阅、带未验证标记的用途候选、可获得的关键数值、接口状态及边界。L1 增加单位/坐标、事实依据、工具、来源/图像/facts/observation 链接、源与图像哈希、诊断与重新验收条件。源标题不翻译替换原值，可另提供展示名。

详细集合可以按 profile 展示上限截断，但应给出“展示 n/总数 m”及完整数据链接。不要把少量样例写成完整集合。
