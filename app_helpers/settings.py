from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Any


DEFAULT_NAVIGATION = {
    "home_label": "Home",
    "bio_label": "Bio",
    "work_label": "Areas of Work",
    "interests_label": "Interests",
    "projects_label": "Projects",
    "github_label": "GitHub",
    "schedule_label": "Schedule",
    "primary_section_label": "Explore",
}


DEFAULT_THEME = {
    "theme": {
        "fonts": {
            "display": "Fraunces",
            "body": "Space Grotesk",
        },
        "colors": {
            "background": "#F7F3EA",
            "surface": "#FFFDF8",
            "surface_alt": "#F3EEE2",
            "text": "#14213D",
            "muted": "#52616B",
            "border": "#D9CDBA",
            "primary": "#0F766E",
            "primary_soft": "#D9F2EE",
            "accent": "#D97706",
            "accent_soft": "#FFF0DA",
            "hero_from": "#0F766E",
            "hero_to": "#D97706",
        },
        "radii": {
            "xl": "28px",
            "lg": "22px",
            "md": "16px",
        },
    }
}


def load_settings_file(path: str | Path) -> dict[str, Any]:
    file_path = Path(path)
    if not file_path.exists():
        return DEFAULT_THEME.copy() if "config" in file_path.name else {}

    data = parse_simple_yaml(file_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{file_path} must contain a mapping at the top level.")

    if file_path.name == "config.yaml":
        return merge_nested(DEFAULT_THEME, data)

    return normalize_settings(data)


def normalize_settings(data: dict[str, Any]) -> dict[str, Any]:
    profile = dict(data.get("profile", {}))
    profile.setdefault("name", "Your Name")
    profile.setdefault("role", "Builder")
    profile.setdefault("bio", [])
    profile.setdefault("social_links", [])
    profile.setdefault("signature_points", [])

    work_areas = [dict(item) for item in data.get("work_areas", [])]
    interests = dict(data.get("interests", {}))
    interests.setdefault("intro", "")
    interests.setdefault("items", [])

    github = dict(data.get("github", {}))
    github.setdefault("repositories", [])

    projects: list[dict[str, Any]] = []
    for item in data.get("projects", []):
        project = dict(item)
        project.setdefault("slug", slugify(project.get("name", "project")))
        project.setdefault("description", [])
        project.setdefault("outcomes", [])
        project.setdefault("stack", [])
        projects.append(project)

    calendar = dict(data.get("calendar", {}))
    calendar.setdefault("provider", "Google Calendar")
    calendar.setdefault("meeting_topics", [])

    normalized = {
        "profile": profile,
        "work_areas": work_areas,
        "work_intro": data.get("work_intro", "A snapshot of the work I like to do best."),
        "interests": interests,
        "github": github,
        "projects": projects,
        "projects_intro": data.get(
            "projects_intro",
            "The projects that are shipping, evolving, or being explored right now.",
        ),
        "calendar": calendar,
        "navigation": {**DEFAULT_NAVIGATION, **dict(data.get("navigation", {}))},
    }

    if not normalized["github"]["repositories"]:
        normalized["github"]["repositories"] = [
            {
                "name": project["name"],
                "description": project["summary"],
                "url": project["github_url"],
            }
            for project in projects
            if project.get("github_url")
        ]

    return normalized


def merge_nested(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    for key in set(base) | set(override):
        base_value = base.get(key)
        override_value = override.get(key)
        if isinstance(base_value, dict) and isinstance(override_value, dict):
            merged[key] = merge_nested(base_value, override_value)
        elif key in override:
            merged[key] = override_value
        else:
            merged[key] = base_value
    return merged


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "project"


def parse_simple_yaml(raw_text: str) -> Any:
    prepared_lines = _prepare_lines(raw_text)
    if not prepared_lines:
        return {}
    node, next_index = _parse_node(prepared_lines, 0, prepared_lines[0][0])
    if next_index != len(prepared_lines):
        raise ValueError("Unable to parse the full YAML document.")
    return node


def _prepare_lines(raw_text: str) -> list[tuple[int, str, int]]:
    prepared: list[tuple[int, str, int]] = []
    for line_number, raw_line in enumerate(raw_text.splitlines(), start=1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        prepared.append((indent, raw_line.strip(), line_number))
    return prepared


def _parse_node(lines: list[tuple[int, str, int]], index: int, indent: int) -> tuple[Any, int]:
    _, content, _ = lines[index]
    if content.startswith("- "):
        return _parse_list(lines, index, indent)
    return _parse_mapping(lines, index, indent)


def _parse_mapping(
    lines: list[tuple[int, str, int]], index: int, indent: int
) -> tuple[dict[str, Any], int]:
    result: dict[str, Any] = {}
    while index < len(lines):
        current_indent, content, line_number = lines[index]
        if current_indent < indent:
            break
        if current_indent != indent or content.startswith("- "):
            break
        key, separator, value_text = content.partition(":")
        if not separator:
            raise ValueError(f"Line {line_number} is missing a ':' separator.")

        key = key.strip()
        value_text = value_text.strip()
        index += 1

        if not value_text:
            if index < len(lines) and lines[index][0] > current_indent:
                value, index = _parse_node(lines, index, lines[index][0])
            else:
                value = None
        else:
            value = _parse_scalar(value_text)

        result[key] = value
    return result, index


def _parse_list(lines: list[tuple[int, str, int]], index: int, indent: int) -> tuple[list[Any], int]:
    result: list[Any] = []
    while index < len(lines):
        current_indent, content, _ = lines[index]
        if current_indent < indent:
            break
        if current_indent != indent or not content.startswith("- "):
            break

        value_text = content[2:].strip()
        index += 1

        if not value_text:
            if index < len(lines) and lines[index][0] > current_indent:
                value, index = _parse_node(lines, index, lines[index][0])
            else:
                value = None
            result.append(value)
            continue

        if _looks_like_inline_mapping(value_text):
            key, _, first_value_text = value_text.partition(":")
            item: dict[str, Any] = {}
            first_value_text = first_value_text.strip()
            if first_value_text:
                item[key.strip()] = _parse_scalar(first_value_text)
            elif index < len(lines) and lines[index][0] > current_indent:
                nested_value, index = _parse_node(lines, index, lines[index][0])
                item[key.strip()] = nested_value
            else:
                item[key.strip()] = None

            if index < len(lines) and lines[index][0] > current_indent:
                extra_mapping, index = _parse_mapping(lines, index, lines[index][0])
                item.update(extra_mapping)

            result.append(item)
            continue

        result.append(_parse_scalar(value_text))
    return result, index


def _looks_like_inline_mapping(value_text: str) -> bool:
    if value_text.startswith(("'", '"')):
        return False
    key, separator, _ = value_text.partition(":")
    if not separator:
        return False
    return bool(key) and re.fullmatch(r"[A-Za-z0-9_ -]+", key) is not None


def _parse_scalar(value_text: str) -> Any:
    lowered = value_text.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in {"null", "none"}:
        return None

    if value_text.startswith(('"', "'")) and value_text.endswith(('"', "'")):
        return ast.literal_eval(value_text)

    if value_text.startswith(("[", "{", "(")):
        try:
            return ast.literal_eval(value_text)
        except (SyntaxError, ValueError):
            return value_text

    try:
        return int(value_text)
    except ValueError:
        pass

    try:
        return float(value_text)
    except ValueError:
        return value_text
