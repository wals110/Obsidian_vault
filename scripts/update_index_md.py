#!/usr/bin/env python3
"""
Update or create index.md in every non-hidden directory for GitHub Pages.
- Skips any directory whose path contains a hidden segment (starts with '.')
- Lists child directories first, then files
- Percent-encodes link targets (spaces, accents, &, …) so links are clickable on GitHub Pages
- Adds YAML front matter with a safely quoted title
- Writes files only when content changes (to keep Git diffs small)

Usage:
  python3 scripts/update_index_md.py [ROOT_DIR]
Defaults to current directory if ROOT_DIR is omitted.
"""
import argparse
import os
import sys
import urllib.parse
from typing import List, Tuple


def is_hidden_anywhere(root: str, path: str) -> bool:
    rel = os.path.relpath(path, root)
    if rel == ".":
        return False
    return any(part.startswith(".") for part in rel.split(os.sep))


def list_children(dirpath: str) -> Tuple[List[str], List[str]]:
    try:
        entries = os.listdir(dirpath)
    except Exception:
        return [], []
    dirs: List[str] = []
    files: List[str] = []
    for name in entries:
        if name.startswith('.'):
            continue  # skip hidden entries
        p = os.path.join(dirpath, name)
        if os.path.isdir(p):
            dirs.append(name)
        elif os.path.isfile(p):
            if name == 'index.md':
                continue
            files.append(name)
    dirs.sort(key=str.casefold)
    files.sort(key=str.casefold)
    return dirs, files


def yaml_quote(s: str) -> str:
    # Quote for YAML using double quotes, escaping backslashes and quotes
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def build_content(root: str, dirpath: str) -> str:
    rel = os.path.relpath(dirpath, root)
    title = 'Home' if rel == '.' else os.path.basename(dirpath)

    lines: List[str] = []
    lines.append('---')
    lines.append(f'title: {yaml_quote(title)}')
    lines.append('---')
    lines.append('')
    lines.append(f'# {title}')
    lines.append('')

    dirs, files = list_children(dirpath)

    if dirs:
        lines.append('## Dossiers')
        lines.append('')
        for d in dirs:
            enc = urllib.parse.quote(d)
            lines.append(f'- [{d}](./{enc}/)')
        lines.append('')

    if files:
        lines.append('## Fichiers')
        lines.append('')
        for f in files:
            enc = urllib.parse.quote(f)
            lines.append(f'- [{f}](./{enc})')
        lines.append('')

    return '\n'.join(lines).rstrip() + '\n'


def write_if_changed(path: str, content: str) -> str:
    existed_before = os.path.exists(path)
    if existed_before:
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
                old = fh.read()
            if old == content:
                return 'unchanged'
        except Exception:
            pass
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(content)
    return 'created' if not existed_before else 'updated'


def main() -> int:
    ap = argparse.ArgumentParser(description='Generate/update index.md files for GitHub Pages.')
    ap.add_argument('root', nargs='?', default='.', help='Root directory (default: current)')
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    created = updated = unchanged = 0

    for dirpath, dirnames, filenames in os.walk(root):
        # Skip hidden directories anywhere in the path
        if is_hidden_anywhere(root, dirpath):
            dirnames[:] = []
            continue
        # Avoid descending into hidden children
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]

        content = build_content(root, dirpath)
        out = os.path.join(dirpath, 'index.md')
        status = write_if_changed(out, content)
        if status == 'created':
            created += 1
        elif status == 'updated':
            updated += 1
        else:
            unchanged += 1

    print(f'created={created} updated={updated} unchanged={unchanged}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
