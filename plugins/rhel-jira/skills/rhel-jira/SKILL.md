---
name: rhel-jira
description: RHEL Kernel JIRA workflow assistant. Use when working with RHEL, RHELTEST, or RHELMISC issues on issues.redhat.com — create, search, transition, comment, close, assign, sprint status, links, target release, or any RHEL/RHELTEST/RHELMISC issue key.
---

# RHEL Kernel JIRA Assistant

Projects **RHEL**, **RHELTEST**, **RHELMISC** on `issues.redhat.com`. Tools: `jira_*` from wtmcp.

## Gates

Skipping any gate is a rule violation.

| Gate | When | How |
|------|------|-----|
| TRANSITION | before `jira_transition_issue` | `jira_get_transitions` on that issue — IDs are numeric and differ per issue |
| TEXT GENERATION | closing summaries, descriptions, @mentions, tables/code, multi-section | one Task; read `comments.md` first |
| PREVIEW | before any mutate with `dry_run=false` | `AskQuestion` on a **rendered** preview (not raw ADF) |

| Thought | Reality |
|---------|---------|
| "Short, so simple path" | Closing summaries and descriptions are always complex |
| "Skip the Task" | Closing summaries, @mentions, descriptions, structured content always use the Task |
| "I know ADF / the transition ID" | Read `comments.md`. Discover transition IDs fresh |
| "Skip preview" | Every mutation needs PREVIEW approval |

**Simple text** (no Task): ≤3 plain paragraphs, no @mentions/tables/code, not a closing summary or description.

```json
{"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Fixed in upstream commit abc1234."}]}]}
```

Unsure of ADF shape → complex path. PREVIEW still applies.

**Complex text** — one Task. Prompt: `comments.md` ADF and @mention rules; issue key, type, purpose; session context (logs, patches, commits, tests).

1. Essay-form prose (paragraphs, no bullets). pal-skills `chat` if installed, else inline. Reject bullets and retry.
2. ADF: `type: "doc"`, `version: 1`, `content` of valid block nodes (`comments.md`).
3. Validate (pal-skills `challenge` if installed, else inline): ADF not wiki; root doc/v1; blocks only paragraph/heading/bulletList/orderedList/codeBlock/table/rule/blockquote; inline text+marks (strong, em, code, link), not `*bold*` / `h3.` / `{code}`. Fix and re-check.
4. Return:
   ```
   PLAIN_TEXT:
   [preview]

   ADF_CONTENT:
   [JSON for the Jira tool]
   ```

Task failed → write ADF from `comments.md` and self-validate. Drafting a closing summary, description, or @mention without a Task → STOP, complex path.

**PREVIEW** covers every mutating `jira_*` (create, comment, edit, set_*, transition, assign, labels, components, links, sprint, backlog, delete). Show: key or NEW, type, operation, rendered text. AskQuestion: "Apply this [operation] to [KEY] ([type])?" Yes → `dry_run=false`. No → "What would you like to change?" About to mutate without preview → STOP, `dry_run=true` first.

Wiki markup (`h3.`, `{code}`, `*bold*`) shows as raw text. ADF only. Plain `@name` does not notify; mention nodes do (`comments.md`).

## Safety

1. After create/update, re-fetch — JIRA can drop invalid fields silently.
2. Don't guess `target_release`, `severity`, `release_blocker` — ask.
3. Exclude Closed unless asked (`resolution = EMPTY`).
4. Default `project in (RHEL, RHELTEST, RHELMISC)`.
5. Never Read/Shell `.jira_cache/` — `jira_read_cache_summary` / `jira_get_issue_from_cache`.
6. Link UI is inverted: `inward_issue_key` shows the **outward** description.
7. Story/Bug ↔ Task: only "Issue split". Task is `outward_issue_key`, Story/Bug is `inward_issue_key` (Story shows "split to Task"):
   ```
   jira_add_issue_link(link_type="Issue split", outward_issue_key="PROJ-200", inward_issue_key="PROJ-100")
   ```
8. Epic depends on Stories/Bugs, never the reverse; never Epic↔Task. Depend: `inward`=depends, `outward`=depended-on (inward shows "depends on"):
   ```
   jira_add_issue_link(link_type="Depend", inward_issue_key="PROJ-100", outward_issue_key="PROJ-200")
   ```
9. `jira_set_parent` only Epic > Story/Bug > Task. Unsure → `jira_debug_fields`.
10. Never `jira_get_all_agile_boards` (thousands of boards). Use `jira_get_issues_for_board` with a known board ID.
11. Sprint and story points are **Task-only**. Refuse on Story/Bug/Epic.

JQL names ≠ update IDs. JQL: `target_release`, `qa_contact`, `assignedteam`. Updates: `customfield_NNNNN` via `jira_debug_fields(search="...")`.

## Close

Read `workflow/resolutions.md` first. Never set Done-Errata (automation). Bugs: Fixed / Won't Fix / Duplicate / Cannot Reproduce / Incomplete. Tasks/Stories: Done / Won't Do.

| Clue | Resolution |
|------|------------|
| fixed, patched, MR | Fixed |
| done, completed (Task/Story) | Done |
| won't fix, out of scope | Won't Fix |
| won't do, not needed | Won't Do |
| duplicate, same as KEY | Duplicate |
| can't reproduce | Cannot Reproduce |
| not a bug, expected | Not a Bug |
| incomplete, stale | Incomplete |

Can't infer → AskQuestion menu filtered by issue type. **Duplicate:** need the original key (ask if missing); `link_type="Duplicate"` before closing.

When closing, pull LKML / MR / tests / commits / review into the closing comment.

## Create

`jira_create_issue`: `project`, `issue_type`, `summary`, `description`, `assignee`, `priority`, `labels`, `components`, `fix_versions`, `epic_name` (new Epics only), `assigned_team`, `dry_run`.

- Components are case-sensitive — read `components.md`.
- Extra fields after create: `jira_set_custom_field`. Assignee rejected → `jira_assign_issue`. Aliases: `"me"` / `"myself"` / `"currentUser"`; team `"my team"`.
- Report `https://issues.redhat.com/browse/<KEY>`.
- Infer from the session; put values in the dry_run preview.

| Source | Infer |
|--------|-------|
| logs, traces | summary, description, priority |
| diffs | summary, description, components |
| commits | summary, description, upstream refs |
| LKML | description link, upstream |
| build failures | summary, repro, expected vs actual |
| subsystem talk | components, `sched:` / `net/mlx5:` prefix |

**Summary:** `net/mlx5: fix timeout in firmware reset flow`

**Task summaries** start `[<Planning Value>]` — read `workflow/task-splitting.md`. Infer (`[QE Task]` to verify, `[DEV Task]` for backport/MR, `[Test Case Writing Task]` for tests). Can't infer → AskQuestion menu.

**Description:** problem; repro if any; expected vs actual; acceptance; kernel/version; upstream refs.

## Errors and worklog

- Read timeout: retry once. Create timeout: do not retry — search by summary first.
- Field errors: `jira_debug_fields`, then retry. Bad component: `components.md`.
- After a successful mutate, cache is stale: `jira_flush_cache` or re-fetch.

`jira_issue_worklog`: `"2h 30m"`, `"1d 4h"`, `"30m"`. PREVIEW includes key, time, optional comment.

Flow: New → Planning → In Progress → Integration → Release Pending → Closed. Errata Link + Preliminary Testing: Pass → Integration. Advisory ships → Closed Done-Errata.

## Read before acting

These are not auto-loaded. Read **before** the action, not after an error.

| When | File |
|------|------|
| complex text | `comments.md` |
| components | `components.md` |
| JQL | `fields.md` |
| transition / close / z-stream / verify | `workflows.md` |
| per-status activity | `workflow/state-transitions.md` |
| ticket verification | `workflow/stateverify.md` |
| resolutions | `workflow/resolutions.md` |
| blockers / exceptions | `workflow/blockers-exceptions.md` |
| task splitting | `workflow/task-splitting.md` |
| z-stream | `workflow/zstream.md` |
| JQL examples | `queries.md` |
| tool params / dry_run | `tools.md` |
