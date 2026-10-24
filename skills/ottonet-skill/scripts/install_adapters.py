#!/usr/bin/env python3
"""
install_adapters.py - Multi-Agent Configuration Installer for Ottonet Skill.
Installs native instruction files for:
- OpenAI Codex & ChatGPT (CODEX.md / .codexrules)
- OpenCode (OPENCODE.md / .opencoderules)
- Cursor (.cursorrules)
- Claude Code (CLAUDE.md)
- GitHub Copilot (.github/copilot-instructions.md)
- Windsurf (.windsurfrules)
- Cline / Roo Code (.clinerules)

Usage:
  python install_adapters.py [target_project_dir] [--agents all|codex|chatgpt|opencode|cursor|claude|copilot|windsurf|cline]
"""

import sys
import shutil
import argparse
from pathlib import Path

ADAPTERS_DIR = Path(__file__).parent.parent / "adapters"

ADAPTER_MAPPINGS = {
    "codex": [("CODEX.md", "CODEX.md"), ("codexrules", ".codexrules")],
    "chatgpt": [("CODEX.md", "CODEX.md")],
    "opencode": [("OPENCODE.md", "OPENCODE.md"), ("opencoderules", ".opencoderules")],
    "cursor": [("cursorrules", ".cursorrules")],
    "claude": [("CLAUDE.md", "CLAUDE.md")],
    "copilot": [("copilot-instructions.md", ".github/copilot-instructions.md")],
    "windsurf": [("windsurfrules", ".windsurfrules")],
    "cline": [("clinerules", ".clinerules")],
}

def install_adapters(target_dir: str = ".", agents: str = "all"):
    root = Path(target_dir).resolve()
    root.mkdir(parents=True, exist_ok=True)

    if agents == "all":
        selected = ["codex", "opencode", "cursor", "claude", "copilot", "windsurf", "cline"]
    else:
        selected = [a.strip().lower() for a in agents.split(",")]

    installed = []
    for agent in selected:
        if agent in ADAPTER_MAPPINGS:
            for src_name, dest_rel in ADAPTER_MAPPINGS[agent]:
                src_file = ADAPTERS_DIR / src_name
                dest_file = root / dest_rel
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                if src_file.exists():
                    shutil.copy2(src_file, dest_file)
                    installed.append(f"{agent} -> {dest_file.relative_to(root)}")

    return installed

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Install Ottonet Skill Multi-Agent Configs")
    parser.add_argument("target", nargs="?", default=".", help="Target project root directory")
    parser.add_argument("--agents", default="all", help="Comma-separated agents: all, codex, chatgpt, opencode, cursor, claude, copilot, windsurf, cline")

    args = parser.parse_args()
    res = install_adapters(args.target, args.agents)
    print(f"[OK] Installed {len(res)} AI Agent adapter files in: {args.target}")
    for item in res:
        print(f"  * {item}")
