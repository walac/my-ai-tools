#!/usr/bin/env python3
"""Stage tracked changes and commit from a message file.

Run this from the Shell tool. Do not run `git commit` from Shell — the
wrapper injects `--trailer Co-authored-by: Cursor <cursoragent@cursor.com>`.
"""

from __future__ import annotations

import subprocess
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: dco-commit.py MSG_FILE", file=sys.stderr)
        return 2
    msg = sys.argv[1]
    subprocess.run(["git", "add", "-u"], check=True)
    return subprocess.run(["git", "commit", "-F", msg]).returncode


if __name__ == "__main__":
    sys.exit(main())
