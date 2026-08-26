---
name: commit
description: Create a Linux-kernel-style Git commit with a DCO sign-off. Use when the user asks to prepare or create a commit.
---

# Kernel-style commit

Inspect `git status`, `git diff HEAD`, and recent non-merge subjects before drafting anything. Stop if there are no tracked changes or a merge, rebase, or cherry-pick is in progress.

Report genuine pre-commit issues first. Draft a focused imperative subject (50 characters or fewer) using the repository's subsystem prefix; write a wrapped (72 columns) prose body explaining why and what changed. Do not invent claims, AI attribution, or trailers.

This skill bundles `scripts/dco-commit.py` beside this `SKILL.md`. Resolve that script from the installed skill directory, never from the target repository's `scripts/` directory. Never invoke `git commit` from the agent shell — wrappers inject extra trailers. Always run the bundled `dco-commit.py` against a temporary message file.

Show the complete proposed message and ask for explicit approval before committing. On approval, add tracked modifications and run the bundled `dco-commit.py` with a temporary message file. The message must contain exactly one `Signed-off-by: <git user.name> <git user.email>` trailer; add `Assisted-by: LLM` only when the user requests it. Verify the completed commit message and report its hash.
