#!/usr/bin/env python3
"""Fails if any retired product name appears in the repo (outside archive/ and .git/)."""
import os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP_DIRS = {".git", "archive", "node_modules"}
SKIP_FILES = {"retired-names.txt", "build.py"}

names = [n.strip() for n in open(os.path.join(ROOT, "retired-names.txt")) if n.strip()]
pattern = re.compile("|".join(re.escape(n) for n in names), re.IGNORECASE)
hits = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    for f in filenames:
        if f in SKIP_FILES:
            continue
        p = os.path.join(dirpath, f)
        try:
            lines = open(p, encoding="utf-8").read().splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for i, line in enumerate(lines, 1):
            if pattern.search(line):
                hits.append(f"{os.path.relpath(p, ROOT)}:{i}: {line.strip()[:100]}")
if hits:
    print("Retired name found:\n" + "\n".join(hits))
    sys.exit(1)
print(f"OK: no retired names ({', '.join(names)}) found.")
