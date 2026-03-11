#!/usr/bin/env python3
import os
import re

ROOT = "."
OUTPUT = "SUMMARY.md"

IGNORE_DIRS = {".git", "_book", "node_modules", ".venv"}
TITLE_RE = re.compile(r"^\s*#\s+(.*)")

def natural_key(s):
    """
    稳定自然排序 key：
    数字 -> (0, number)
    字符 -> (1, string)
    """

    key = []

    parts = re.split(r'[\-_\.]', s)

    for part in parts:
        subs = re.split(r'(\d+)', part)
        for item in subs:
            if item == "":
                continue
            if item.isdigit():
                key.append((0, int(item)))
            else:
                key.append((1, item.lower()))

    return key

def title_of(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                m = TITLE_RE.match(line)
                if m:
                    return m.group(1).strip()
    except:
        pass

    return os.path.splitext(os.path.basename(path))[0]

def rel(path):
    return "./" + os.path.relpath(path, ROOT).replace("\\", "/")

def generate(dir_path, level, lines):
    entries = sorted(os.listdir(dir_path), key=natural_key)

    readme = None
    subdirs = []
    files = []

    for entry in entries:
        full = os.path.join(dir_path, entry)

        if entry in IGNORE_DIRS:
            continue

        if os.path.isdir(full):
            subdirs.append(full)
        elif entry.lower() == "readme.md":
            readme = full
        elif entry.endswith(".md") and entry != OUTPUT:
            files.append(full)

    # ROOT：封面，只输出，不参与层级
    if dir_path == ROOT:
        if readme:
            lines.append(f"- [{title_of(readme)}]({rel(readme)})")

        for sub in subdirs:
            generate(sub, 0, lines)
        return

    # 模块 README
    if readme:
        indent = "  " * level
        lines.append(f"{indent}- [{title_of(readme)}]({rel(readme)})")
    else:
        print(f"⚠ Warning: {dir_path} has no README.md")

    # 子模块
    for sub in subdirs:
        generate(sub, level + 1, lines)

    # 模块内容 md
    for f in files:
        indent = "  " * (level + 1)
        lines.append(f"{indent}- [{title_of(f)}]({rel(f)})")

def main():
    lines = ["# 目录\n"]
    generate(ROOT, 0, lines)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("SUMMARY.md generated.")

if __name__ == "__main__":
    main()
