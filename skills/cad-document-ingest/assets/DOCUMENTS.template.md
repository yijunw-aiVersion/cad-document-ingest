# 文本投影模板

从当前 facts 与绑定 observation 生成正文。花括号变量表示字段映射，最终正文不能保留变量名。无值时生成明确未知和原因，而不是空白或猜测。精确数值、计数、单位与哈希由提取结果或代码生成；自然语言只组织事实和实际观察。

## L0 → .abstract.md

```text
{object_id}@{version}｜{display_category_or_unknown}｜{source_title_or_unknown}。
外形：{reviewed_visible_shape_or_unreviewed_reason}。
用途候选（未验证）：{purpose_candidate_or_unknown_reason}。
源几何：{supported_geometry_summary_with_unit_frame_and_method}。
接口：{declared_interface_summary_or_unknown_reason}。
边界：{source_and_visual_limitations}。
profile：{profile}；{review_status_summary}；数值来自源声明/计算。
```

依据 profile 长度限制组织为摘要；不能为缩短而丢失用途未验证、接口未知或必要的单位边界。

## L1 → .overview.md 与 asset.md

```markdown
# {object_id}@{version}｜{display_category}｜{source_title}

{同一份L0正文}

## 源事实

- 源格式/版本：{source_format_and_version_or_unknown}。
- 源类别/标题及依据：{raw_category_title_and_basis}。
- 单位与坐标：{units_frame_transform_and_basis}。
- 几何：{available_geometry_with_method_accuracy_and_scope}。
- 接口：{status_count_types_and_source_binding}。
- 其他关键属性：{sourced_properties_or_unknown}。
- 展示范围：{shown_total_if_truncated_and_full_facts_link}。

## 视觉与用途候选

- 审阅状态：{review_status_reviewer_or_reason}。
- 可见外形：{actual_observation_or_unreviewed_reason}。
- 用途候选（未验证）：{purpose_candidate_or_unknown_reason}。
- 视觉限制：{occlusion_views_display_colors}。

## 来源与转换证据

- 原生入口：{source_link}；依赖状态：{dependency_status}。
- 完整事实：{facts_link}；观察记录：{observation_link}。
- 实际预览：{preview_links_or_unavailable_reason}。
- 提取工具/版本与方法：{extraction_tool_version_and_method}。
- 源 manifest SHA-256：{source_manifest_sha256}。
- 主源与图像 SHA-256：{entry_and_reviewed_images_sha256}。
- profile ID / SHA-256：{profile_and_profile_sha256}。
- 诊断与损失：{diagnostics_and_losses_or_none_with_basis}。

## 使用边界与重新验收

{limitations_and_optional_stage_degradations}
源声明、几何、可见外形和用途候选具有不同证据范围。
源/依赖、工具解释、profile、图像或规定正文改变时重新检查受影响证据。
```

默认 asset 与 L1 只生成一份正文并复制相同字节。JSON/源/预览链接默认相对于所在版本目录，远端交付按 profile 重写为受支持的 URI；最终链接须实际核对。

可选父目录 L0 使用版本 L0，父 L1 需将正文相对链接重写为当前版本路径并追加当前版本导航。重写后核查内容语义保持一致与链接可用；若目标需严格同正文，采用 profile 定义的绝对 URI 链接。

用户模板替换此模板时保留本包的来源、状态与一致性约束，通过目标适配映射记录变化。
