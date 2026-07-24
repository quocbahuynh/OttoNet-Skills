#!/usr/bin/env python3
"""Validate OttoNet Skill frontmatter without third-party dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path


SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
KEY_VALUE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):[ \t]*(.*)$")


def error(errors: list[str], path: Path, message: str) -> None:
    errors.append(f"{path}: {message}")


def parse_frontmatter(path: Path, errors: list[str]) -> dict[str, str] | None:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        error(errors, path, "frontmatter must begin on line 1 with '---'")
        return None

    try:
        end = lines.index("---", 1)
    except ValueError:
        error(errors, path, "frontmatter is missing its closing '---' delimiter")
        return None

    values: dict[str, str] = {}
    for number, line in enumerate(lines[1:end], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = KEY_VALUE.fullmatch(line)
        if match is None:
            error(errors, path, f"line {number}: expected a simple YAML key/value entry")
            continue
        key, value = match.groups()
        if key in values:
            error(errors, path, f"line {number}: duplicate frontmatter key '{key}'")
            continue
        values[key] = value.strip().strip('"\'')

    return values


def validate_skill(path: Path, errors: list[str], names: dict[str, Path]) -> None:
    values = parse_frontmatter(path, errors)
    if values is None:
        return

    directory_name = path.parent.name
    name = values.get("name", "")
    description = values.get("description", "")

    if not name:
        error(errors, path, "frontmatter is missing a non-empty 'name'")
    else:
        if name != directory_name:
            error(errors, path, f"name '{name}' does not match directory '{directory_name}'")
        if not SKILL_NAME.fullmatch(name):
            error(errors, path, "name must use lowercase letters, numbers, and hyphens only")
        if name in names:
            error(errors, path, f"duplicate skill name '{name}' (also in {names[name]})")
        else:
            names[name] = path

    if not description:
        error(errors, path, "frontmatter is missing a non-empty 'description'")


def main() -> int:
    repository = Path(__file__).resolve().parents[1]
    skills_root = repository / "skills"
    errors: list[str] = []
    names: dict[str, Path] = {}

    if not skills_root.is_dir():
        print(f"ERROR: expected skills directory: {skills_root}")
        return 1

    skill_directories = sorted(path for path in skills_root.iterdir() if path.is_dir())
    for directory in skill_directories:
        if not (directory / "SKILL.md").is_file():
            error(errors, directory, "skill directory is missing SKILL.md")

    direct_skills = sorted(skills_root.glob("*/SKILL.md"))
    all_skills = sorted(skills_root.rglob("SKILL.md"))
    direct_set = set(direct_skills)

    if not direct_skills:
        errors.append(f"{skills_root}: no skills/*/SKILL.md files found")

    for nested in all_skills:
        if nested not in direct_set:
            error(errors, nested, "SKILL.md must be directly inside skills/<skill-name>/")

    for skill in direct_skills:
        validate_skill(skill, errors, names)

    if errors:
        print("Skill validation failed:")
        for item in errors:
            print(f"- {item}")
        return 1

    print(f"Validated {len(direct_skills)} skill(s):")
    for name in sorted(names):
        print(f"- {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
