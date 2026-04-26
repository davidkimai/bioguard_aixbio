"""Build a hackathon code submission surface without docs."""

from __future__ import annotations

from pathlib import Path
import argparse
import hashlib
import json
import shutil


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_DIR = ROOT / "artifacts" / "submission_surface"
_IGNORE_PATTERNS = ("__pycache__", "*.pyc")

SURFACE_ITEMS = [
    ROOT / "src",
    ROOT / "spec",
    ROOT / "skills",
    ROOT / "scripts",
    ROOT / "Makefile",
    ROOT / "pyproject.toml",
]


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def build_surface(out_dir: Path, *, clean: bool = True, include_examples: bool = False) -> dict:
    if clean and out_dir.exists():
        shutil.rmtree(out_dir)

    out_dir.mkdir(parents=True, exist_ok=True)

    for item in SURFACE_ITEMS:
        if not item.exists():
            continue
        target = out_dir / item.relative_to(ROOT)
        if item.is_dir():
            shutil.copytree(
                item,
                target,
                ignore=shutil.ignore_patterns(*_IGNORE_PATTERNS),
            )
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)

    if include_examples:
        examples_dir = ROOT / "artifacts" / "examples"
        if examples_dir.exists():
            shutil.copytree(examples_dir, out_dir / "artifacts" / "examples")

    manifest = {
        "submission_surface": str(out_dir),
        "files": [],
    }
    for artifact in sorted(out_dir.rglob("*")):
        if artifact.is_file():
            manifest["files"].append(
                {
                    "path": str(artifact.relative_to(out_dir)),
                    "sha256": sha256_file(artifact),
                    "size_bytes": artifact.stat().st_size,
                }
            )

    manifest_path = out_dir / "submission_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    readme = (
        "# BioGuard Submission Surface\n\n"
        "Code package for hackathon evaluation only.\n"
        "Run: `make init`, `make check`, `make screen`, `make eval`.\n"
        "Docs and full report artifacts intentionally kept out of this package.\n"
    )
    (out_dir / "README_SUBMISSION.md").write_text(readme, encoding="utf-8")

    return {
        "path": str(out_dir),
        "files": len(manifest["files"]),
        "manifest": str(manifest_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--include-examples", action="store_true")
    args = parser.parse_args()

    payload = build_surface(args.out, include_examples=args.include_examples)
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
