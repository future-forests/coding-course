#!/usr/bin/env python3
"""Add hierarchical numbering to markdown headers in .md and .ipynb files.

- ## -> ## 1., ## 2., ...
- ### -> ### i., ### ii., ...
- #### -> #### a., #### b., ...
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HEADER_RE = re.compile(
    r"^(#{2,4})\s+(?:(?:\d+|[ivxlcdm]+|[a-z]+)\.\s+)?(.+)$"
)

UNNUMBERED_H2_TITLES = frozenset({"Quick reference card"})


def to_roman(n: int) -> str:
    vals = [
        (1000, "m"),
        (900, "cm"),
        (500, "d"),
        (400, "cd"),
        (100, "c"),
        (90, "xc"),
        (50, "l"),
        (40, "xl"),
        (10, "x"),
        (9, "ix"),
        (5, "v"),
        (4, "iv"),
        (1, "i"),
    ]
    result = ""
    for value, numeral in vals:
        while n >= value:
            result += numeral
            n -= value
    return result


def to_letter(n: int) -> str:
    result = ""
    while n > 0:
        n -= 1
        result = chr(ord("a") + n % 26) + result
        n //= 26
    return result


def process_text(text: str, counters: dict[int, int] | None = None) -> tuple[str, dict[int, int]]:
    if counters is None:
        counters = {2: 0, 3: 0, 4: 0}
    else:
        counters = dict(counters)

    lines = text.splitlines(keepends=True)
    if not lines:
        return text, counters

    out: list[str] = []

    for line in lines:
        body = line.rstrip("\n")
        newline = line[len(body) :]
        match = HEADER_RE.match(body)
        if not match:
            out.append(line)
            continue

        level = len(match.group(1))
        if level not in (2, 3, 4):
            out.append(line)
            continue

        title = match.group(2)

        if level == 2 and title in UNNUMBERED_H2_TITLES:
            counters[3] = 0
            counters[4] = 0
            out.append(f"## {title}{newline}")
            continue

        if level == 2:
            counters[3] = 0
            counters[4] = 0
            counters[2] += 1
            prefix = f"{counters[2]}."
        elif level == 3:
            counters[4] = 0
            counters[3] += 1
            prefix = f"{to_roman(counters[3])}."
        else:
            counters[4] += 1
            prefix = f"{to_letter(counters[4])}."

        out.append(f"{'#' * level} {prefix} {title}{newline}")

    return "".join(out), counters


def process_markdown_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    updated, _ = process_text(original)
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def process_notebook_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    notebook = json.loads(original)
    changed = False
    counters = {2: 0, 3: 0, 4: 0}

    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        source = cell.get("source", "")
        if isinstance(source, list):
            joined = "".join(source)
            updated, counters = process_text(joined, counters)
            if updated != joined:
                cell["source"] = updated.splitlines(keepends=True)
                if cell["source"] and not cell["source"][-1].endswith("\n"):
                    cell["source"][-1] += "\n"
                changed = True
        else:
            updated, counters = process_text(source, counters)
            if updated != source:
                cell["source"] = updated
                changed = True

    if changed:
        path.write_text(
            json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8",
        )
    return changed


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    changed_files: list[Path] = []

    for path in sorted(root.rglob("*")):
        if ".git" in path.parts or ".pixi" in path.parts:
            continue
        if path.suffix == ".md":
            if process_markdown_file(path):
                changed_files.append(path)
        elif path.suffix == ".ipynb":
            if process_notebook_file(path):
                changed_files.append(path)

    for path in changed_files:
        print(path.relative_to(root))
    print(f"Updated {len(changed_files)} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
