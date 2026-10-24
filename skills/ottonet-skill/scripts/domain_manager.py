#!/usr/bin/env python3
"""
domain_manager.py - Task and Domain Context Switcher for Ottonet Skill.
Isolates domain knowledge between tasks and branches (e.g. Task #102 Incident vs Task #103 Schedule).
Updates active task and active domain states in .codebase-intel.
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from typing import Dict, Any

INTEL_DIR_NAME = ".codebase-intel"

def get_current_git_branch(root: Path) -> str:
    try:
        res = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=str(root),
            capture_output=True,
            text=True,
            check=True
        )
        return res.stdout.strip() or "detached_head"
    except Exception:
        return "unknown_branch"

def switch_domain(task_id: str, domain_name: str, target_root: str = ".") -> Dict[str, Any]:
    root = Path(target_root).resolve()
    intel_dir = root / INTEL_DIR_NAME
    tasks_dir = intel_dir / "tasks"
    domains_dir = intel_dir / "domains"
    tasks_dir.mkdir(parents=True, exist_ok=True)
    domains_dir.mkdir(parents=True, exist_ok=True)

    branch = get_current_git_branch(root)
    clean_domain = domain_name.strip().lower().replace(" ", "-")

    task_state = {
        "task_id": str(task_id),
        "domain": clean_domain,
        "branch": branch,
        "isolated": True
    }

    # Save to active-task.json and active-domain.json
    (tasks_dir / "active-task.json").write_text(json.dumps(task_state, indent=2), encoding="utf-8")
    (domains_dir / "active-domain.json").write_text(json.dumps({"active_domain": clean_domain}, indent=2), encoding="utf-8")

    # Check if domain rules card exists, if not inform to extract
    rule_card = domains_dir / f"{clean_domain}-rules.md"
    card_exists = rule_card.exists()

    return {
        "task_state": task_state,
        "rule_card_path": str(rule_card),
        "rule_card_exists": card_exists
    }

def get_status(target_root: str = ".") -> Dict[str, Any]:
    root = Path(target_root).resolve()
    intel_dir = root / INTEL_DIR_NAME
    task_file = intel_dir / "tasks" / "active-task.json"
    if task_file.exists():
        try:
            return json.loads(task_file.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"status": "No active task registered"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ottonet Skill Domain Context Manager")
    subparsers = parser.add_subparsers(dest="command")

    switch_parser = subparsers.add_parser("switch")
    switch_parser.add_argument("--task", required=True, help="Task number or identifier (e.g. 103)")
    switch_parser.add_argument("--domain", required=True, help="Module or Domain name (e.g. project-schedule)")
    switch_parser.add_argument("--root", default=".", help="Root directory")

    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("--root", default=".", help="Root directory")

    args = parser.parse_args()

    if args.command == "switch":
        res = switch_domain(args.task, args.domain, args.root)
        print("================ OTTONET SKILL: CONTEXT SWITCHED ================")
        print(f"Task ID:         #{res['task_state']['task_id']}")
        print(f"Active Domain:   {res['task_state']['domain']}")
        print(f"Current Branch:  {res['task_state']['branch']}")
        print(f"Domain Card:     {res['rule_card_path']} (Exists: {res['rule_card_exists']})")
        print("=================================================================")
        print("[NOTICE] Previous task context has been isolated. Active domain loaded.")
    elif args.command == "status":
        print(json.dumps(get_status(args.root), indent=2))
    else:
        parser.print_help()
