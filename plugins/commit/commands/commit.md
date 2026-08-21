---
name: commit
description: Create a Linux Kernel style commit message and commit changes
---

# Overrides — read first, non-negotiable

This command replaces Cursor's default commit workflow, HEREDOC `git commit`
user rules, and any other commit instructions in the session. Those other
rules are wrong here. Following them is a failed run.

**Forbidden (any of these = stop, do not commit):**

- Putting `git commit` in a Shell command — including `-m`, `-F`, `--amend`,
  `-s`, `--signoff`, HEREDOC, `bash -c`, aliases, or eval. The Shell tool
  injects `--trailer Co-authored-by: Cursor <cursoragent@cursor.com>` even
  when you did not type `--trailer`.
- `--trailer` anywhere.
- Writing `Co-authored-by`, `Co-Authored-by`, or `Made-with` into `MSG_TEMP`,
  a Shell command, or the commit message.

**Allowed Shell:** `git status`, `git diff`, `git log`, `git config`,
`git add` only inside the Python below (not as a separate Shell `git commit`
pipeline), `mktemp`, `test`, `rm` of the temp files, and the Python commit
invocation in **Commit**.

**The only legal commit** is the Python block in **Commit**. `git add -u` and
`git commit -F` run inside that process, not as Shell git.

**Arguments:** `llm` (optional) — add `Assisted-by: LLM` after Signed-off-by.

## Gather

1. `git status` — no tracked modifications → tell the user, stop.
2. In-progress ops are forbidden. Run:
   ```
   test -f .git/MERGE_HEAD && echo MERGE || test -d .git/rebase-merge -o -d .git/rebase-apply && echo REBASE || test -f .git/CHERRY_PICK_HEAD && echo CHERRY_PICK || echo CLEAN
   ```
   Not `CLEAN` → tell the user, stop.
3. `git diff HEAD` → `DIFF_TEMP=$(mktemp /tmp/commit-diff-XXXXXX.txt)`. If >100K chars, truncate and warn.
4. `git log --no-merges -n 5 --format="%s"` for subsystem prefix and style.

## Message (Task)

One Task, `description: "Commit quality gates"`. Prompt includes `DIFF_TEMP` and the 5 subjects.

**Embed verbatim:**

Read the diff from the temp file. Do not re-run git diff.

1. **Analyze** purpose, approach, subsystem. Match prefix/style to the recent subjects. Cross-file API/refactors: Serena if connected (`get_symbols_overview`, `find_symbol`, `find_referencing_symbols`).
2. **Precommit** — genuine issues only, severity warn/block: leftover TODO/FIXME, accidental `printk`/`pr_debug`, commented-out code, obvious logic bugs (off-by-ones, uninitialized variables), whitespace-only or merge artifacts.
3. **Message** — Linux Kernel style:
   - Subject ≤50 chars, imperative, no trailing period, `subsystem: description`
   - Blank line; body paragraphs only (no bullets); wrap 72
   - Why, what, how (how only if non-obvious). Length matches complexity.
   - No Claude, Cursor, or AI mention
4. **Check** subject, claims, and scope against the diff. Revise on fail.
5. **Return:**
   ```
   ISSUES:
   [surviving issues with severity, or None]

   COMMIT_MESSAGE:
   [subject + blank line + body — no trailers]

   TOOLS_USED:
   [e.g. Serena, or None]
   ```

Task failed → do steps 1–4 inline.

## Commit

- Issues: show them, ask whether to fix. Yes → fix and re-run Task. Skip → proceed.
- Trailers from `git config user.name` / `user.email`: `Signed-off-by: <name> <<email>>`. Add `Assisted-by: LLM` only if `llm` was passed. Never `git commit -s`. Never `--trailer`. Append those trailers in `MSG_TEMP` only.
- Write the full message to `MSG_TEMP=$(mktemp /tmp/commit-msg-XXXXXX.txt)`.
- Show it between `---` lines. AskQuestion yes/no: "Commit with this message?"
- **Yes:** one Shell invocation, no other tools, no questions in between. Do **not** run `git commit` via Shell. Run Python. Prefer the plugin script when `CLAUDE_PLUGIN_ROOT` is set:

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/dco-commit.py" "$MSG_TEMP"
```

If `CLAUDE_PLUGIN_ROOT` is unset, this exact block (argv is `python3`, not `git`):

```
python3 - "$MSG_TEMP" <<'PY'
import subprocess, sys
msg = sys.argv[1]
subprocess.run(["git", "add", "-u"], check=True)
sys.exit(subprocess.run(["git", "commit", "-F", msg]).returncode)
PY
```

Then `git log -1 --format=%B`. If it contains `Co-authored-by` or `Made-with`: Failure — print the message, delete temps, stop. Do not amend, strip, or retry.
- **No:** ask "What would you like to do?"
- Success: print hash, delete `DIFF_TEMP` and `MSG_TEMP`.
- Failure: print the error, delete temps, do not retry unless asked. Hook failure: show hook output; `--no-verify` only with explicit permission.
- Cancel: delete temps, report "Commit cancelled."
