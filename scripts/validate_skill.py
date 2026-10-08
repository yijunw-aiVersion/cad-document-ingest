"""Validate the self-contained Markdown-only Skill payload; Python stdlib only."""

import json
from pathlib import Path
import re
import sys


NAME = "cad-document-ingest"
EXPECTED = {
    "SKILL.md",
    "references/baseline.md",
    "references/document-contract.md",
    "references/format-adapters.md",
    "references/execution-evidence.md",
    "references/publication.md",
    "references/conformance.md",
    "references/implementation-map.md",
    "assets/CONVERSION-PROFILE.template.md",
    "assets/FACTS.template.md",
    "assets/VISUAL-OBSERVATION.template.md",
    "assets/DOCUMENTS.template.md",
}


def validate(root):
    root = Path(root).resolve()
    entries = list(root.rglob("*"))
    if any(p.is_symlink() for p in entries):
        raise ValueError("Skill payload must contain actual files, not symlinks")
    files = {p.relative_to(root).as_posix() for p in entries if p.is_file()}
    if files != EXPECTED:
        raise ValueError(f"Payload mismatch: missing={EXPECTED - files}, extra={files - EXPECTED}")
    content = (root / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", content, re.S)
    if not match:
        raise ValueError("Missing YAML frontmatter")
    fields = {}
    for line in match[1].splitlines():
        key, value = line.split(":", 1)
        if key in fields:
            raise ValueError(f"Duplicate frontmatter key: {key}")
        fields[key] = value.strip()
    if set(fields) != {"name", "description"}:
        raise ValueError("Expected name and description scalar frontmatter only")
    if fields["name"] != NAME or root.name != NAME:
        raise ValueError("Skill name and folder must agree")
    if not 1 <= len(fields["description"]) <= 1024:
        raise ValueError("Invalid description length")
    links = 0
    json_templates = 0
    for relative in sorted(files):
        path = root / relative
        body = path.read_text(encoding="utf-8")
        if re.search(r"/Users/[^/\s]+/|[A-Z]:\\Users\\", body):
            raise ValueError(f"Machine-specific path in {relative}")
        if "[TODO:" in body:
            raise ValueError(f"Unfinished scaffold in {relative}")
        fence = None
        for line in body.splitlines():
            marker = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
            if marker:
                if fence is None:
                    fence = marker[1]
                elif marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                    fence = None
        if fence:
            raise ValueError(f"Unclosed code fence in {relative}")
        for target in re.findall(r"\]\(([^)]+)\)", body):
            if "://" in target or target.startswith("#"):
                continue
            resolved = (path.parent / target.split("#", 1)[0]).resolve()
            if not resolved.is_relative_to(root) or not resolved.is_file():
                raise ValueError(f"Broken or escaping link: {relative} -> {target}")
            links += 1
        for payload in re.findall(r"^```json\n(.*?)\n```", body, re.M | re.S):
            data = json.loads(payload, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
            if not isinstance(data, dict):
                raise ValueError(f"Expected JSON object template in {relative}")
            json_templates += 1
    if json_templates != 2:
        raise ValueError("Expected facts and observation JSON templates")
    print(f"PASS: {len(files)} Markdown files, {links} local links, {json_templates} JSON templates; self-contained Skill")


if __name__ == "__main__":
    skill_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "skills" / NAME
    try:
        validate(skill_root)
    except (ValueError, OSError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
