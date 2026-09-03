---
name: cover
description: Generate a Linux-kernel-style patch-series cover letter from Git history. Use when the user asks for a cover letter or PATCH 0/N message.
---

# Kernel patch-series cover letter

Accept an optional commit count, baseline branch, and output path. Reject a count combined with a baseline. Resolve the range in this order:

1. Count: use that count.
2. Baseline: verify it with `git rev-parse --verify <baseline>` and count `git rev-list --count <baseline>..HEAD`.
3. Neither: obtain `@{upstream}` with `git rev-parse --abbrev-ref @{upstream}` and count `git rev-list --count HEAD ^@{upstream}`. If it is absent or the count is zero, ask for a count.

Stop for an invalid baseline or an empty range. Create `COMMITS_TEMP` with `mktemp /tmp/cover-commits-XXXXXX.txt`; record `git log -n <count> -p --format=fuller` for a count, or `git log <baseline>..HEAD -p --format=fuller` for a baseline. If it exceeds 50 KB, retry without `-p`; if still over 100 KB, warn. Read this file for the letter; do not re-run `git log` while drafting.

For a versioned series (an explicit vN request, or output filename `v<N>-*` for N > 1), use the available LKML tools `lkml_get_user_series`, `lkml_search_patches`, `lkml_get_thread`, and `lkml_get_raw`. Get `git config user.email`, then look up the prior cover in this order: `lkml_get_user_series` by author email (for v2, unversioned `[PATCH 0/X]`; later versions, vN-1), then `lkml_search_patches` by topic and author. Retry each failed LKML call twice. If both lookups fail, ask for the prior Message-ID; if none is available, warn and write a first-round letter. Once a Message-ID is found or supplied, call `lkml_get_thread` on it, retain the prior subject description and every `Changes in v<X>:` section verbatim, and call `lkml_get_raw` for each vN-1 patch before comparing them with the current series. Preserve a supplied prior cover's earlier Changes sections when LKML tools are unavailable, and say lookup was skipped.

Use exactly one dedicated drafting pass from `COMMITS_TEMP`. When delegation is available, give that pass `COMMITS_TEMP`, the commit count, and all recovered version data; otherwise perform it inline. It must return:

```
COVER_LETTER:
[subject, blank line, body, and any Changes sections]

TOOLS_USED:
[LKML or None]
```

The letter subject is `[PATCH 0/<count>] <theme>`, or `[PATCH v<N> 0/<count>] <prior subject description>` when versioned. Follow with two to four 72-column prose paragraphs covering motivation, series-level approach, and testing/context; keep it high-level, with no per-patch summary. Do not invent metrics, issue IDs, rationale, reviewer feedback, or version history. For a verified later version, add only substantive `Changes in v<N>:` entries: structural changes first, then code or bugfix changes, crediting reviewers where supported. Skip whitespace-only and wording changes; append all older Changes sections verbatim. Check the subject and claims against `COMMITS_TEMP` before returning. If a delegated drafting pass fails, perform those analysis, drafting, and checks inline without re-running `git log`.

Show the complete letter between `---` lines before writing. If no output path was given, ask whether terminal-only output is wanted; otherwise ask for a path. After confirmation, if the path is a `git format-patch` template, replace only `*** SUBJECT HERE ***` and `*** BLURB HERE ***`, preserving its diffstat and patch list. For any other requested path, overwrite it. Delete `COMMITS_TEMP` after writing, on failure, or on cancellation.
