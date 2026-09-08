#!/usr/bin/env python3
"""Scan staged .md files for secrets / internal identifiers before commit.
This is a lightweight safety net, not a full secret scanner."""
import re
import subprocess
import sys

PATTERNS = [
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key block"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key id"),
    (re.compile(r"(?i)(api[_-]?key|secret|password|passwd|token)\s*[:=]\s*[\"']?[A-Za-z0-9/+=_-]{8,}"), "possible credential"),
    (re.compile(r"(?i)ravensec\.eu"), "company domain"),
    (re.compile(r"(?i)\braven\s*cyber"), "company name"),
    (re.compile(r"\b(10\.\d{1,3}\.\d{1,3}\.\d{1,3}|172\.(1[6-9]|2[0-9]|3[01])\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3})\b"), "internal/private IP"),
]

def staged_md_files():
    out = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True, text=True, check=True
    ).stdout.splitlines()
    return [f for f in out if f.endswith(".md")]

def staged_content(path):
    return subprocess.run(
        ["git", "show", f":{path}"], capture_output=True, text=True
    ).stdout

def main():
    files = staged_md_files()
    if not files:
        return 0
    hit = False
    for f in files:
        content = staged_content(f)
        for pattern, label in PATTERNS:
            if pattern.search(content):
                print(f"pre-commit: '{f}' matches a flagged pattern ({label})")
                hit = True
    if hit:
        print("\nCommit blocked — this may contain a secret, an internal IP, or a company name.")
        print("Double-check the file(s) above. If it's a false positive: git commit --no-verify")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
