---
name: cover
description: Use when asked to generate or draft a Linux-kernel-style patch-series cover letter (PATCH 0/N) from Git history or update an existing versioned cover letter.
---

# Kernel Patch-Series Cover Letter

1. **Resolve Range**
   - Accept optional `<count>`, `<baseline>`, and output path. Reject if both `<count>` and `<baseline>` are given.
   - Resolve commit count in order:
     1. `<count>`: use specified count.
     2. `<baseline>`: verify with `git rev-parse --verify <baseline>`, then count with `git rev-list --count <baseline>..HEAD`.
     3. Neither: get upstream with `git rev-parse --abbrev-ref @{upstream}` and count with `git rev-list --count HEAD ^@{upstream}`. If upstream is missing or count is 0, prompt user for a count.
   - Stop immediately if baseline is invalid or commit count is 0.

2. **Inspect Commits**
   - Run `git log -p -n <count>` (or `git log -p <baseline>..HEAD`). If diff exceeds 100 KB, warn the user.
   - Analyze theme, problem, solution design, and commit relationships.

3. **Recover Prior Version (Versioned Series Only)**
   - Trigger on explicit vN request or output filename matching `v<N>-*` (N > 1).
   - If LKML tools (`lkml_get_user_series`, `lkml_search_patches`, `lkml_get_thread`, `lkml_get_raw`) are available:
     - Get email: `git config user.email`.
     - Locate prior cover (retry failed calls twice):
       1. `lkml_get_user_series` by author email (v2: `[PATCH 0/X]`; vN: `v<N-1>`).
       2. `lkml_search_patches` by topic and author.
       3. If both fail, ask user for prior Message-ID; if none, warn and proceed as v1.
     - With Message-ID: call `lkml_get_thread` to extract prior subject and all historical `Changes in v<X>:` sections verbatim. Call `lkml_get_raw` for each v<N-1> patch to compare against current commits.
   - If LKML tools are unavailable: warn that lookup was skipped, preserve any user-supplied prior `Changes in v<X>:` sections verbatim, or draft as v1.

4. **Draft Cover Letter**
   - **Subject**: `[PATCH 0/<count>] <theme>` (unversioned) or `[PATCH v<N> 0/<count>] <prior subject verbatim>` (versioned).
   - **Body**: 2–4 paragraphs, 72-column wrap:
     - *Motivation*: problem and why it matters.
     - *Approach*: high-level technical solution and how patches fit together.
     - *Context/Testing (optional)*: test coverage, benchmarks, or next steps.
   - **Constraints**:
     - Narrative only: do NOT summarize patches individually or list commits.
     - Do NOT fabricate metrics, issue IDs, rationale, reviewer feedback, or history.
   - **Changelog (`Changes in v<N>:`)** (versioned only):
     - List structural changes first (added/removed/split/squashed), then substantive code/bugfix changes (credit reviewers where supported).
     - Skip whitespace and wording changes.
     - Append all older `Changes in v<X>:` sections verbatim below.

5. **Request Approval**
   - Display the complete cover letter to the user and prompt for approval (e.g. via a menu or selection).
   - If the user declines or requests modifications, iterate with the user to improve the text until he approves.

6. **Review & Output**
   - Display complete letter between `---` lines.
   - If no output path was provided: ask whether terminal-only output is desired, or prompt for a path.
   - After confirmation:
     - If target is a `git format-patch` template (`*** SUBJECT HERE ***` / `*** BLURB HERE ***`): replace only those markers, keeping diffstat and patch list intact.
     - Otherwise: write/overwrite file.
