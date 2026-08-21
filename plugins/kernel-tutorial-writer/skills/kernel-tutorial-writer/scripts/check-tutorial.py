#!/usr/bin/env python3
"""Check a kernel tutorial Markdown file against this skill's mechanical rules.

Usage:
  python3 check-tutorial.py TUTORIAL.md [--tree KERNEL_ROOT]

Exit 0 if no errors (warnings are allowed). Exit 1 if any error.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HEADING_RE = re.compile(r"^(#{2,6})\s+(.+?)\s*$")
SLUG_RE = re.compile(r"\s+\{#([a-z0-9][a-z0-9-]*)\}\s*$")
NUMBERED_HEADING_RE = re.compile(r"^\d+(\.\d+)*\s+\S")
HR_RE = re.compile(r"^-{3,}\s*$")
SECREF_RE = re.compile(r"\[\]\(#([a-z0-9-]+)\)\{\.secref\}")
ELIXIR_RE = re.compile(
    r"https://elixir\.bootlin\.com/linux/([^/\s)]+)/source/([^)\s#]+)(#L(\d+))?"
)
MD_LINK_RE = re.compile(r"\[([^\]]*)\]\((https://elixir\.bootlin\.com/linux/[^)]+)\)")
IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
POSSESSIVE_RE = re.compile(r"\b([A-Za-z][A-Za-z0-9_]*)'s\b")
CONTRACTIONS = {
    "it's",
    "that's",
    "there's",
    "here's",
    "what's",
    "let's",
    "who's",
    "he's",
    "she's",
    "they're",  # not 's but keep the set tight
}


def strip_fences(text: str) -> list[tuple[int, str, bool]]:
    """Return (lineno, line, in_code) for each line. lineno is 1-based."""
    rows = []
    in_code = False
    for i, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            rows.append((i, line, True))
            in_code = not in_code
            continue
        rows.append((i, line, in_code))
    return rows


def heading_text_without_slug(raw: str) -> str:
    return SLUG_RE.sub("", raw).strip()


def check(path: Path, tree: Path | None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    text = path.read_text(encoding="utf-8")
    rows = strip_fences(text)

    headings: list[tuple[int, str, str, str | None]] = []
    # (lineno, hashes, display_text, slug)
    for lineno, line, in_code in rows:
        if in_code:
            continue
        m = HEADING_RE.match(line)
        if not m:
            continue
        hashes, rest = m.group(1), m.group(2)
        slug_m = SLUG_RE.search(rest)
        slug = slug_m.group(1) if slug_m else None
        display = heading_text_without_slug(rest)
        headings.append((lineno, hashes, display, slug))

    slugs: dict[str, int] = {}
    first_h2: int | None = None
    for lineno, hashes, display, slug in headings:
        if hashes == "##" and first_h2 is None:
            first_h2 = lineno
        if NUMBERED_HEADING_RE.match(display):
            errors.append(
                f"{path}:{lineno}: heading has a section number "
                f"(secnum.lua will double it): {display!r}"
            )
        if slug is None:
            errors.append(f"{path}:{lineno}: heading missing {{#slug}}: {display!r}")
        elif slug in slugs:
            errors.append(
                f"{path}:{lineno}: duplicate slug {{#{slug}}} "
                f"(also line {slugs[slug]})"
            )
        else:
            slugs[slug] = lineno

    # --- before every ## except the first
    h2s = [(ln, disp) for ln, hs, disp, _ in headings if hs == "##"]
    for i, (lineno, display) in enumerate(h2s):
        if i == 0:
            continue
        # Walk back through non-code lines for the previous non-blank line.
        prev = None
        for ln, line, in_code in reversed(rows):
            if ln >= lineno:
                continue
            if in_code:
                continue
            if line.strip() == "":
                continue
            prev = (ln, line)
            break
        if prev is None or not HR_RE.match(prev[1].strip()):
            errors.append(
                f"{path}:{lineno}: ## heading {display!r} is not preceded by ---"
            )

    for lineno, line, in_code in rows:
        if in_code:
            continue
        for slug in SECREF_RE.findall(line):
            if slug not in slugs:
                errors.append(
                    f"{path}:{lineno}: .secref target {{#{slug}}} does not exist"
                )

    versions: set[str] = set()
    symbol_urls: dict[str, str] = {}
    for lineno, line, in_code in rows:
        if in_code:
            continue
        for text_label, url in MD_LINK_RE.findall(line):
            em = ELIXIR_RE.search(url)
            if not em:
                continue
            version, relpath, hashpart, linenum = em.group(1), em.group(2), em.group(3), em.group(4)
            versions.add(version)
            if not hashpart or not linenum:
                errors.append(
                    f"{path}:{lineno}: elixir link has no #L<number>: {url}"
                )
                continue
            ident = text_label.strip().strip("`").rstrip("()")
            if IDENT_RE.match(ident):
                prev_url = symbol_urls.get(ident)
                # Compare path+#L, ignore version drift separately.
                key = f"{relpath}#L{linenum}"
                if prev_url and prev_url != key:
                    errors.append(
                        f"{path}:{lineno}: {ident} links to {key} but earlier "
                        f"linked to {prev_url}"
                    )
                else:
                    symbol_urls[ident] = key
            if tree is None:
                continue
            src = tree / relpath
            if not src.is_file():
                errors.append(
                    f"{path}:{lineno}: elixir path not in tree: {relpath}"
                )
                continue
            src_lines = src.read_text(encoding="utf-8", errors="replace").splitlines()
            n = int(linenum)
            if n < 1 or n > len(src_lines):
                errors.append(
                    f"{path}:{lineno}: {relpath}#L{n} is out of range "
                    f"({len(src_lines)} lines)"
                )
                continue
            target = src_lines[n - 1]
            if IDENT_RE.match(ident) and ident not in target:
                errors.append(
                    f"{path}:{lineno}: {relpath}#L{n} does not contain {ident!r}: "
                    f"{target.rstrip()!r}"
                )

    if len(versions) > 1:
        errors.append(
            f"{path}: elixir links mix versions {sorted(versions)}; "
            "pick one prefix and use it everywhere"
        )

    for lineno, line, in_code in rows:
        if in_code:
            continue
        if HEADING_RE.match(line):
            continue
        for m in POSSESSIVE_RE.finditer(line):
            word = m.group(0)
            if word.lower() in CONTRACTIONS:
                continue
            warnings.append(
                f"{path}:{lineno}: possessive {word!r} — rephrase as "
                f"'of the …' or a compound noun"
            )

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tutorial", type=Path)
    parser.add_argument("--tree", type=Path, default=None, help="Kernel tree root")
    args = parser.parse_args()
    if not args.tutorial.is_file():
        print(f"error: {args.tutorial} is not a file", file=sys.stderr)
        return 2
    tree = args.tree.resolve() if args.tree else None
    if tree is not None and not tree.is_dir():
        print(f"error: --tree {tree} is not a directory", file=sys.stderr)
        return 2
    errors, warnings = check(args.tutorial, tree)
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    print(
        f"{len(errors)} error(s), {len(warnings)} warning(s) in {args.tutorial}"
        + (f" (tree {tree})" if tree else "")
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
