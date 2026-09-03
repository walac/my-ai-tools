---
name: commit
description: Create a Linux-kernel-style Git commit with a DCO sign-off. Use when the user asks to prepare or create a commit.
---

# Kernel-style commit

Inspect `git status`, `git diff HEAD`, and the five most recent non-merge subjects (`git log --no-merges -n 5 --format=%s`) before drafting anything. Stop if there are no tracked changes or a merge, rebase, or cherry-pick is in progress. Do not resolve, abort, or continue an in-progress operation unless the user explicitly asks. Capture the diff in `DIFF_TEMP` with `mktemp /tmp/commit-diff-XXXXXX.txt`; if it exceeds 100 KB, truncate it and warn.

Use one dedicated review-and-drafting pass from `DIFF_TEMP` and the five subjects. When delegation is available, pass them to one worker; otherwise perform it inline. Do not re-run `git diff` during the pass. Analyze the change's purpose, approach, subsystem, and recent subject style. For cross-file API or refactor changes, use Serena when connected (`get_symbols_overview`, `find_symbol`, and `find_referencing_symbols`). Using the pre-commit skill if available, identify only genuine warn/block issues: TODO/FIXME, `printk`/`pr_debug` or other debug output, commented-out code, obvious logic errors, and whitespace-only or merge artifacts. Return:

```
ISSUES:
[warn/block findings, or None]

COMMIT_MESSAGE:
[subject, blank line, and body; no trailers]

TOOLS_USED:
[Serena or None]
```

If delegation fails, complete those review and drafting steps inline from `DIFF_TEMP`. Report issues first and ask whether the user wants them fixed. If fixed, repeat inspection and review; otherwise proceed only with the user's explicit decision. Draft a focused, imperative, no-trailing-period subject (50 characters or fewer) matching the repository's subsystem prefix and recent style. Write 72-column prose that explains why and what changed, adding how only when non-obvious; scale its length to the change. Do not invent claims, AI attribution, or trailers.

This skill bundles `scripts/dco-commit` beside this `SKILL.md`. Resolve its absolute installed path from the loaded skill, never from the target repository's `scripts/` directory. Never invoke `git commit`, `git commit -s`, use `--trailer`, or stage files directly from the agent shell — wrappers inject extra trailers. Do not write `Co-authored-by:`, `Co-Authored-by:`, or `Made-with:` in the message. The bundled helper stages tracked-file changes with `git add -u` and runs the commit internally.

Obtain `name` with `git config user.name` and `email` with `git config user.email`. If either is empty or unavailable, stop and ask the user to configure it; never invent an identity. Create `MSG_TEMP` with `mktemp /tmp/commit-msg-XXXXXX.txt`. Its complete contents must be the subject and body followed by exactly one `Signed-off-by: <name> <email>` trailer. Add `Assisted-by: LLM` only when the user requests it.

Show the complete message between `---` lines and ask for explicit approval before committing. On approval, run exactly one resolved helper invocation, with no intervening questions or tool calls:

```
"$SKILL_DIR/scripts/dco-commit" "$MSG_TEMP"
```

Here, `SKILL_DIR` is the absolute directory containing this installed `SKILL.md`; do not substitute a target-repository path. On failure, show the error, delete `DIFF_TEMP` and the temporary message, and do not retry unless asked. A hook may be bypassed with `--no-verify` only with explicit permission.

After a successful helper invocation, inspect `git log -1 --format=%B` and `git rev-parse HEAD`. Verify the completed message has exactly one line equal to `Signed-off-by: <name> <email>` and no line beginning, case-insensitively, `Co-authored-by` or `Made-with`. If verification fails, report the message and stop; do not amend, strip, or retry. Otherwise report the hash and delete `DIFF_TEMP` and the temporary message. If approval is declined or cancelled, delete both temporary files and ask what the user wants to change.
