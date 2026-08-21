# RHEL Kernel JIRA: Comments and Descriptions

Jira Cloud rich text is ADF JSON, not wiki markup. `summary` is plain text.

| Tool | Field | Format |
|------|-------|--------|
| `jira_add_comment` / `jira_edit_comment` | body | ADF |
| `jira_create_issue` / `jira_set_text_field` | `description` | ADF |

Pass ADF as a dict, a JSON string, or plain text (auto-converted to paragraphs). A `type: "doc"` / `version: 1` dict is passed through as-is.

## ADF nodes

Root: `{"type": "doc", "version": 1, "content": [...]}`.

Blocks: `paragraph`, `heading` (`attrs.level`), `bulletList` / `orderedList` of `listItem`, `codeBlock` (`attrs.language`), `rule`, `blockquote`, `table` of `tableRow` / `tableHeader` / `tableCell`.

`listItem`, `blockquote`, `tableHeader`, and `tableCell` children must be blocks (usually `paragraph`), not bare text.

Inline inside paragraph/heading `content`:

- text: `{"type": "text", "text": "..."}` with optional `marks`: `strong`, `em`, `code`, `link` (`attrs.href`)
- mention: `{"type": "mention", "attrs": {"id": "accountId", "text": "@Display Name"}}`
- `{"type": "hardBreak"}`

```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {"type": "heading", "attrs": {"level": 3}, "content": [{"type": "text", "text": "Summary"}]},
    {"type": "paragraph", "content": [
      {"type": "text", "text": "Fixed the "},
      {"type": "text", "text": "timeout issue", "marks": [{"type": "strong"}]},
      {"type": "text", "text": " in firmware reset flow."}
    ]}
  ]
}
```

## @Mentions

Only if the text contains `@` tokens.

1. Collect `@…` tokens.
2. Candidates from the issue, in order: Reporter, Assignee, QA Contact, Developer, Watchers, previous commenters, previously mentioned. `jira_get_issues` with `expand=["comments"]`, `all_fields=true`.
3. Exact match (case-insensitive) on username/display name, else substring. Ambiguity: longest / token-boundary match, then earliest in the candidate list. `jira_get_user` to verify.
4. Replace with a mention node; `id` is the Cloud `accountId`.
5. Unresolved: leave the original `@mention` as plain text.

CC: append a final paragraph `cc:` plus mention nodes, same resolution.

## Comment shape

Essay-form prose (paragraphs, not bullets). Include what, why, impact, next steps, and links (LKML, MR, commits, benchmarks) as they apply.

Technical updates, as ADF: h3 Summary (1–2 sentences); h4 Details (`code` marks); h4 Results (table: Metric, Before, After).

## Closing comments

Pull from the session:

| Source | Include |
|--------|---------|
| LKML | thread link, version, patch count |
| MR/PR | URL |
| commits | key hashes + one-line |
| tests/benchmarks | summary table |
| review | how feedback was addressed |
| follow-up | remaining work / related keys |

What was done, how it was verified, links, follow-up.

## Description updates

Fetch the current description with `jira_get_issues` first. If it is non-empty, show current and proposed and get confirmation before replacing.
