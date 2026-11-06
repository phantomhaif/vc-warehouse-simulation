"""Validate portable component metadata. Does not execute VC or component code."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = re.compile(r"\d+\.\d+\.\d+")
ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def validate(root):
    errors = []
    catalog = {}

    def check(condition, message):
        if not condition:
            errors.append(message)

    def path_exists(base, value):
        if not isinstance(value, str) or not value or "\\" in value:
            return False
        candidate = (base / value).resolve()
        return candidate.is_relative_to(base.resolve()) and candidate.is_file()

    for folder in sorted((root / "components").iterdir()):
        if not folder.is_dir():
            continue
        manifest = folder / "manifest.json"
        label = folder.name
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("manifest must be an object")
        except (OSError, ValueError) as exc:
            errors.append(f"{label}: invalid/missing manifest: {exc}")
            continue
        catalog[label] = data
        check(bool(ID.fullmatch(label)) and data.get("id") == label, f"{label}: id must match folder")
        check(bool(VERSION.fullmatch(str(data.get("version", "")))), f"{label}: version must be X.Y.Z")
        check(data.get("status") in ("draft", "experimental", "validated"), f"{label}: invalid status")
        for key in ("description", "owner"):
            check(isinstance(data.get(key), str) and bool(data[key].strip()), f"{label}: {key} required")
        check((folder / "README.md").is_file(), f"{label}: README.md required")
        compat = data.get("compatibility", {})
        check(isinstance(compat, dict) and all(isinstance(compat.get(k), str) and compat[k] for k in ("product", "version", "python")), f"{label}: compatibility required")
        check(data.get("units") == {"length": "mm", "time": "s", "speed": "mm/s"}, f"{label}: units must be mm, s, mm/s")
        check("model" in data, f"{label}: model field required (null allowed for draft)")
        model = data.get("model")
        if model is not None:
            check(path_exists(folder, model), f"{label}: model must be a local existing file")
        if data.get("status") != "draft":
            check(model is not None, f"{label}: non-draft requires model")
        for key in ("scripts", "test_scenarios", "evidence"):
            values = data.get(key)
            check(isinstance(values, list), f"{label}: {key} must be a list")
            if isinstance(values, list):
                base = root if key == "evidence" else folder
                for value in values:
                    check(path_exists(base, value), f"{label}: invalid/missing {key} path: {value}")
        if data.get("status") == "validated":
            check(bool(data.get("test_scenarios")) and bool(data.get("evidence")), f"{label}: validated requires scenarios and evidence")
            check(isinstance(compat, dict) and compat.get("version") not in (None, "unverified") and compat.get("python") not in (None, "unverified"), f"{label}: validated requires tested runtime")
        deps = data.get("dependencies")
        check(isinstance(deps, list), f"{label}: dependencies must be a list")

    graph = {}
    for label, data in catalog.items():
        graph[label] = []
        deps = data.get("dependencies")
        if not isinstance(deps, list):
            continue
        for dep in deps:
            if not isinstance(dep, dict) or not isinstance(dep.get("id"), str):
                errors.append(f"{label}: dependency must contain id and version")
                continue
            target = catalog.get(dep["id"])
            check(target is not None, f"{label}: missing dependency {dep['id']}")
            if target:
                check(dep.get("version") == target.get("version"), f"{label}: dependency version mismatch {dep['id']}")
                graph[label].append(dep["id"])

    visited, active = set(), set()

    def visit(node):
        if node in active:
            errors.append(f"dependency cycle at {node}")
            return
        if node in visited:
            return
        active.add(node)
        for child in graph.get(node, []):
            visit(child)
        active.remove(node)
        visited.add(node)

    for node in graph:
        visit(node)
    return errors, len(catalog)


if __name__ == "__main__":
    errors, count = validate(ROOT)
    for error in errors:
        print("ERROR:", error)
    print(f"Catalog: {count} components; {len(errors)} errors. VC simulation is not checked.")
    sys.exit(bool(errors))
