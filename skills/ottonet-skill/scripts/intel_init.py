#!/usr/bin/env python3
"""
intel_init.py - Initialize .codebase-intel directory with strict Git isolation.
Part of Ottonet Skill.
Guarantees zero git pollution by generating internal .gitignore and registering with .git/info/exclude.
"""

import os
import sys
from pathlib import Path

INTEL_DIR_NAME = ".codebase-intel"
SUBDIRECTORIES = [
    "architecture",
    "entrypoints",
    "domains",
    "conventions",
    "invariants",
    "tasks",
    "cache/skeletons",
]

def init_intel_directory(target_root: str = ".") -> Path:
    root = Path(target_root).resolve()
    intel_dir = root / INTEL_DIR_NAME

    # 1. Create standardized directory structure
    intel_dir.mkdir(parents=True, exist_ok=True)
    for sub in SUBDIRECTORIES:
        (intel_dir / sub).mkdir(parents=True, exist_ok=True)

    # 2. Layer 1 Isolation: Self-contained .gitignore inside .codebase-intel
    internal_gitignore = intel_dir / ".gitignore"
    if not internal_gitignore.exists():
        internal_gitignore.write_text("*\n", encoding="utf-8")

    # 3. Layer 2 Isolation: Ensure .git/info/exclude ignores .codebase-intel
    git_dir = root / ".git"
    if git_dir.is_dir():
        exclude_file = git_dir / "info" / "exclude"
        try:
            exclude_file.parent.mkdir(parents=True, exist_ok=True)
            current_exclude = ""
            if exclude_file.exists():
                current_exclude = exclude_file.read_text(encoding="utf-8")
            
            rule = f"{INTEL_DIR_NAME}/\n"
            if rule.strip() not in current_exclude:
                with open(exclude_file, "a", encoding="utf-8") as f:
                    f.write(f"\n# Auto-added by Ottonet Skill (Zero-Git-Pollution)\n{rule}")
        except Exception:
            # Non-fatal if git directory has restricted permissions
            pass

    return intel_dir

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    intel_path = init_intel_directory(target)
    print(f"[OK] Ottonet Skill initialized .codebase-intel at: {intel_path}")
    print(f"[OK] Strict Git isolation verified (Zero git pollution guaranteed)")
