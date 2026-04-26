"""Execution-state helpers for deterministic project progression.

This module tracks gate/task state and execution notes for the BioGuard workflow.
It is intentionally named `orchestrator` for backwards compatibility only.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import DEFAULT_ORCHESTRATION_MANIFEST
from .utils import read_json_or_yaml, utcnow_iso, write_json


def _status_entry(task_id: str, role: str, status: str, open_items: Optional[List[str]] = None) -> Dict[str, Any]:
    return {
        "task_id": task_id,
        "role": role,
        "status": status,
        "open_items": open_items or [],
        "updated_at_utc": utcnow_iso(),
    }


def init_orchestration_state(manifest_path: str | Path, out_path: str | Path) -> Dict[str, Any]:
    """Backwards-compatible entrypoint; prefer `init_execution_state`."""
    return init_execution_state(manifest_path, out_path)


def init_execution_state(manifest_path: str | Path, out_path: str | Path) -> Dict[str, Any]:
    manifest = read_json_or_yaml(manifest_path)
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    state: Dict[str, Any] = {
        "manifest_path": str(manifest_path),
        "program_mode": manifest.get("program_mode", "hybrid"),
        "updated_at_utc": utcnow_iso(),
        "status": "active",
        "tasks": [],
        "notes": [],
    }
    for role in manifest.get("agent_roles", []):
        state["tasks"].append(
            _status_entry(
                task_id=role["id"],
                role=role["owner"],
                status="not_started",
            )
        )
    write_json(out, state)
    return state


def load_state(path: str | Path) -> Dict[str, Any]:
    return load_execution_state(path)


def load_execution_state(path: str | Path) -> Dict[str, Any]:
    path = Path(path)
    if not path.exists():
        return {"status": "missing", "tasks": []}
    return json.loads(path.read_text(encoding="utf-8"))


def summarize_state(path: str | Path) -> Dict[str, Any]:
    """Backwards-compatible entrypoint; prefer `summarize_execution_state`."""
    return summarize_execution_state(path)


def summarize_execution_state(path: str | Path) -> Dict[str, Any]:
    state = load_state(path)
    total = len(state.get("tasks", []))
    done = sum(1 for t in state.get("tasks", []) if t.get("status") in {"done", "complete"})
    in_progress = sum(1 for t in state.get("tasks", []) if t.get("status") == "in_progress")
    blocked = sum(1 for t in state.get("tasks", []) if t.get("status") == "blocked")
    state.update(
        {
            "counts": {"total": total, "done": done, "in_progress": in_progress, "blocked": blocked},
            "updated_at_utc": utcnow_iso(),
            "completion_pct": round((done / total) * 100, 1) if total else 0.0,
        }
    )
    return state


def update_task(path: str | Path, task_id: str, status: str, open_items: List[str] | None = None) -> Dict[str, Any]:
    state = load_state(path)
    tasks = state.get("tasks", [])
    hit = False
    for entry in tasks:
        if entry.get("task_id") == task_id:
            entry["status"] = status
            if open_items is not None:
                entry["open_items"] = open_items
            entry["updated_at_utc"] = utcnow_iso()
            hit = True
    if not hit:
        tasks.append(_status_entry(task_id=task_id, role="manual", status=status, open_items=open_items))
    state["tasks"] = tasks
    state["updated_at_utc"] = utcnow_iso()
    write_json(path, state)
    return summarize_state(path)


def default_manifest() -> str:
    return str(DEFAULT_ORCHESTRATION_MANIFEST)
