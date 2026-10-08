# visual-observation.json 模板

在实际看图前生成绑定信息；实际审阅后填写观察。`REPLACE_*` 需由当前运行值替换。

```json
{
  "schema_version": "cad.visual-observation.v1",
  "profile": "cad.document-publication.zh.v1",
  "profile_sha256": "REPLACE_PROFILE_SHA256",
  "object_id": "REPLACE_OBJECT_ID",
  "version": "v1",
  "source_manifest_sha256": "REPLACE_SOURCE_MANIFEST_SHA256",
  "preview_policy": "required",
  "images": [],
  "review_status": "not_run",
  "reviewer": null,
  "reviewed_at": null,
  "visible_shape": null,
  "purpose_candidate": null,
  "purpose_status": "unknown",
  "purpose_reason": "尚未审阅",
  "limitations": [],
  "reason": "尚未实际读取图像"
}
```

images 项含 path、sha256、view、render_receipt_ref，path 相对于对象版本目录；列出实际被查看的图像。审阅时间记录带时区的 ISO 8601 时间，不能预填未来动作。

review_status 为 not_run / reviewed / skipped / failed。required 模式的 reviewed 必须对应真实图片读取、匹配绑定和非空外形；无法看图、错版或看不清时保留原因。

purpose_status 为 candidate / unknown / not_applicable。有推断时 purpose_candidate 填写“可能/候选”，正文始终标注未验证；没有合理推断时保留 null 和理由。

visible_shape 可写可见轮廓、开口、表面特征和布局，不从图像补写精确尺寸、隐藏面、承重或兼容性。limitations 记录遮挡、视角、显示颜色等限制。
