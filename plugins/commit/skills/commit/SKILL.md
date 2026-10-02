---
name: commit
description: Use when asked to prepare or create a Git commit, draft a commit message, or record changes with Linux kernel style and DCO sign-off.
---

# Kernel-Style Commit

1. **Inspect**
   - Run `git status`, `git diff --no-ext-diff`, `git diff --no-ext-diff --cached`, and `git log --no-merges -n 3` to examine changes and recent commit conventions.
   - If there are no changes, inform the user and stop.
   - Ignore untracked files unless referenced by tracked modifications. If an untracked file should be committed, warn the user and stop.

2. **Draft Message**
   - Analyze change purpose and subsystem/component prefix. For cross-file API or refactor context, use Serena if available (`get_symbols_overview`, `find_symbol`, `find_referencing_symbols`).
   - **Subject**: ≤50 chars, imperative mood, no trailing period, matching repository prefix conventions (e.g., `component: description`).
   - **Body Structure**: Separate from subject with a blank line. Wrap prose at 72 columns. Structure logically:
     - *Problem & Motivation*: State the underlying problem motivating the change (bug, missing capability, unclear docs, workflow gap). Convince the reviewer why it is worth fixing in the opening paragraph.
     - *Impact*: Describe user- or system-visible effects (errors, unexpected behavior, degraded performance, broken consumers). Help reviewers and downstream users understand why the change matters.
     - *Technical Solution*: Explain in plain English what the change actually does in technical detail, allowing reviewers to verify implementation against intent.
     - *Trade-offs & Metrics*: If claiming improvements (speed, memory, size, clarity), include concrete numbers or rationale. Disclose non-obvious costs or trade-offs (e.g., performance vs readability, backwards compatibility).
   - **Constraints**: Do not fabricate metrics, error logs, issue references, AI attribution (`Co-authored-by`, `Made-with`), or trailers. `git commit -s` automatically adds `Signed-off-by`.

3. **Request Approval**
   - Display the complete commit message to the user and prompt for approval (e.g. via a menu or selection).
   - If the user declines or requests modifications, do not commit.

4. **Commit & Clean Up**
   - Create a temporary file: `MSG_FILE=$(mktemp .commit-msg-XXXXXXXXXX.txt)`
   - Write the approved commit message to `$MSG_FILE`.
   - Run `git commit -as -F "$MSG_FILE"` to stage tracked changes and commit with sign-off.
   - Remove the temporary file immediately (even on failure): `rm -f "$MSG_FILE"`.
   - Do not perform any additional actions beyond these instructions (do not push or amend).
