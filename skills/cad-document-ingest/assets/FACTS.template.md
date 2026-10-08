# facts.json 模板

使用下列结构填写实际事实。`REPLACE_*` 是模板参数，最终文档不能保留。未知事实保持 null 与 reason；不要把模板作为已经提取的结果。默认三维字段可按已确定的二维/其他 profile 映射。

```json
{
  "schema_version": "cad.document-facts.v1",
  "profile": "cad.document-publication.zh.v1",
  "object_id": "REPLACE_OBJECT_ID",
  "version": "v1",
  "title": {"value": null, "status": "unknown", "basis": null, "reason": "尚未提取"},
  "category": {"value": null, "status": "unknown", "basis": null, "reason": "尚未提取"},
  "source": {
    "format": "REPLACE_FORMAT",
    "format_version": null,
    "format_basis": "REPLACE_IDENTIFICATION_BASIS",
    "entry_path": "source/REPLACE_ENTRY_FILENAME",
    "files": [],
    "manifest_sha256": "REPLACE_SOURCE_MANIFEST_SHA256",
    "dependency_status": "unknown"
  },
  "extraction": {
    "tool": "REPLACE_TOOL",
    "tool_version": "REPLACE_TOOL_VERSION",
    "status": "not_run",
    "config_sha256": "REPLACE_CONFIG_SHA256",
    "receipt_ref": "REPLACE_RECEIPT_REF",
    "supported_scope": [],
    "losses": []
  },
  "units": {
    "status": "unknown",
    "source_length_unit": null,
    "normalized_length_unit": null,
    "scale_to_normalized": null,
    "basis": null,
    "reason": "尚未确认单位"
  },
  "coordinate_system": {
    "status": "unknown",
    "dimension": null,
    "source_frame": null,
    "normalized_frame": null,
    "source_to_normalized": null,
    "basis": null,
    "reason": "尚未确认坐标"
  },
  "geometry": {
    "status": "unknown",
    "representation": null,
    "bbox": null,
    "method": null,
    "tolerance": null,
    "basis": [],
    "reason": "尚未计算"
  },
  "interfaces": {
    "status": "unknown",
    "items": [],
    "basis": [],
    "reason": "尚无同版接口证据"
  },
  "properties": [],
  "diagnostics": [],
  "licenses": [],
  "limitations": ["文档转换不证明工程安装、制造或性能"]
}
```

`source.files` 项使用 `{path, role, sha256}`；role 为 entry / dependency / source_library。path 相对于对象版本目录，哈希使用真实原字节，清单不能在最终文档中为空。manifest 算法见 [文档契约](../references/document-contract.md)。

三维 bbox 已知时填写 `{min: [x,y,z], max: [x,y,z], extent: [x,y,z], unit, frame, accuracy}`，extent = max - min。未知单位的原始坐标可保留，但不能写为已知规范化长度。曲面离散化包络须记录估计方法与误差，不能宣称精确极值。

`properties` 项使用 `{name, value, unit, status, basis, method}`；basis 指明源 path/实体或回执。`interfaces.items` 结构由领域 profile 定义，至少有 ID、类型、源绑定和证据；接口数量从真实 items 计算。

diagnostics 项含 code、severity、message、source_ref、affected_fields。licenses 项保留源声明和 path；无声明时明确 unknown。extraction.status 使用 not_run / succeeded / partial / failed / unsupported，不与事实字段状态混淆。
