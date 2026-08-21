---
name: cover
description: Generate a Linux Kernel style cover letter from git commit history
---

Generate a Linux Kernel style cover letter from git history.

**Arguments** (all optional; `num_commits` and `baseline_branch` are mutually exclusive):

- `num_commits` — commit count (auto-detected if neither this nor `baseline_branch`)
- `baseline_branch` — `git log <branch>..HEAD`
- `output_file` — write here (else terminal)

Git and temp files: Shell tool. Versioned series: LKML tools `lkml_get_user_series`, `lkml_search_patches`, `lkml_get_thread`, `lkml_get_raw` when connected. LKML failures: retry twice, then fall back.

## Gather

Both `num_commits` and `baseline_branch` → error, stop.

**Range:**
1. `num_commits` given → `COMMIT_COUNT=num_commits`.
2. `baseline_branch` given → `git rev-parse --verify <baseline_branch>` (missing → stop). `COMMIT_COUNT=$(git rev-list --count <baseline_branch>..HEAD)` (0 → stop).
3. Neither → `git rev-parse --abbrev-ref @{upstream}`. Upstream exists → `COMMIT_COUNT=$(git rev-list --count HEAD ^@{upstream})`. No upstream or count=0 → ask for a count.

**Log** to `COMMITS_TEMP=$(mktemp /tmp/cover-commits-XXXXXX.txt)`:
- `num_commits`: `git log -n <COMMIT_COUNT> -p --format=fuller`
- `baseline_branch`: `git log <baseline_branch>..HEAD -p --format=fuller`
- >50K chars → retry without `-p`. Still >100K → warn.

**Versioned series** — only if `output_file` matches `v<N>-*` with N>1:
1. `git config user.email`
2. Previous cover on LKML, in order: `lkml_get_user_series` (N=2: unversioned `[PATCH 0/X]`; N>2: v\<N-1\>) → `lkml_search_patches` (topic + author) → ask for v\<N-1\> Message-ID → if none, warn and generate a first-round letter.
3. `lkml_get_thread` on that ID. Keep the subject description and every `Changes in v<X>:` section verbatim.
4. `lkml_get_raw` for each v\<N-1\> patch. Pass all of this to the Task.

## Letter (Task)

One Task, `description: "Cover letter quality gates"`. Prompt includes `COMMITS_TEMP`, `COMMIT_COUNT`, and any versioned-series data.

**Embed verbatim:**

Read commits from the temp file. Do not re-run git log.

1. **Analyze** the series theme: problem, approach, how the commits fit, key benefits.
2. **Letter** — Linux Kernel series style:
   - Subject: `[PATCH 0/<COMMIT_COUNT>] <theme>` (versioned: `[PATCH v<N> 0/<COMMIT_COUNT>] <vN-1 subject verbatim>`)
   - Body: 2–4 paragraphs, wrap 72. (1) motivation/problem (2) approach and how the changes work together (3 optional) testing, context, future work
   - High-level narrative only — no per-patch descriptions
   - Do not invent metrics, business justifications, or JIRA IDs absent from the commits
3. **Versioned** (only if previous-version data is in the prompt):
   Diff v\<N-1\> `lkml_get_raw` patches against current: added/removed/split/squashed, substantive code/bugfix changes, replies that this version addresses.
   `Changes in v<N>:` structural first, then substantive (name the patch when useful), credit reviewers ("patch 2: use atomic ops as suggested by Alice"). Skip whitespace/rewording.
   Append after the body, then every earlier `Changes in v<X>:` **verbatim**.
4. **Check** subject, claims, and "no per-patch descriptions" against the commits. Revise on fail.
5. **Return:**
   ```
   COVER_LETTER:
   [subject + blank line + body, including Changes sections]

   TOOLS_USED:
   [e.g. LKML, or None]
   ```

Task failed → do steps 1–4 inline.

## Output

Show the letter between `---` lines.

- `output_file` is a `git format-patch` template (`*** SUBJECT HERE ***` / `*** BLURB HERE ***`): replace those markers only; keep diffstat and patch list.
- `output_file` exists but is not a template: overwrite.
- `output_file` does not exist: create it.
- No `output_file`: AskQuestion yes/no "Output to terminal only (no file)?" — No → ask for a path.

Delete `COMMITS_TEMP` on write, failure, or cancel.
