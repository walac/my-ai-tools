# RHEL Kernel JIRA: Tool Quick Reference

All mutating tools require user confirmation via the PREVIEW GATE before execution with `dry_run=false`.

## Search & Read
| Tool | Purpose | Supports `dry_run` |
|------|---------|-------------------|
| `jira_search` | JQL search, returns summaries + cache path | N/A (read) |
| `jira_get_issues` | Fetch by key list, use `expand` for changelog/comments, `all_fields` for complete data | N/A (read) |
| `jira_get_user` | Look up user by username or search string | N/A (read) |
| `jira_debug_fields` | Discover custom field IDs and names (use `search` param to filter) | N/A (read) |
| `jira_get_transitions` | List valid transitions for an issue (returns transition IDs) | N/A (read) |
| `jira_get_resolutions` | List all valid resolution values | N/A (read) |
| `jira_get_link_types` | List issue link types | N/A (read) |
| `jira_get_myself` | Get authenticated user's profile (accountId, displayName, email) | N/A (read) |
| `jira_download_attachment` | Download attachment by ID (text as UTF-8, binary as base64) | N/A (read) |

## Cache (avoid re-fetching)
| Tool | Purpose | Supports `dry_run` |
|------|---------|-------------------|
| `jira_read_cache_summary` | Extract compact summaries from cache file | N/A (read) |
| `jira_get_issue_from_cache` | Get full issue from cache by key | N/A (read) |
| `jira_query_local_sprint_data` | Filter cached data by assignee, team, status | N/A (read) |
| `jira_flush_cache` | Clear local cache when data may be stale | N/A (local) |

## Create (confirm first, dry_run=false to execute)
| Tool | Purpose | Supports `dry_run` |
|------|---------|-------------------|
| `jira_create_issue` | Create issue (required: `project`, `issue_type`, `summary`). `description` uses ADF | Yes |
| `jira_add_comment` | Add comment (ADF). See `comments.md` for node reference | Yes |
| `jira_add_issue_link` | Link two issues (use `jira_get_link_types` first) | Yes |
| `jira_add_attachment` | Upload local file to issue | No |
| `jira_issue_worklog` | Log time (e.g. `"2h 30m"`, `"1d 4h"`) | Yes |

## Update (confirm first, dry_run=false to execute)
| Tool | Purpose | Supports `dry_run` |
|------|---------|-------------------|
| `jira_set_text_field` | Set standard field by name (`summary`, `description`, `fixVersions`). `description` uses ADF; `summary` is plain text | Yes |
| `jira_set_custom_field` | Set custom field by `field_id` (use `jira_debug_fields` to find ID). Supports `field_type`: text, number, select, multi-select, user, auto | Yes |
| `jira_transition_issue` | Move to new status (requires `transition_id` from `jira_get_transitions`, optional `resolution`) | Yes |
| `jira_assign_issue` | Assign/reassign (supports `"me"`) | Yes |
| `jira_set_priority` | Set priority by name | Yes |
| `jira_set_story_points` | Set story points (numeric, supports fractional) | Yes |
| `jira_set_labels` / `jira_add_labels` / `jira_remove_labels` | Manage labels | Yes |
| `jira_set_components` | Set components | Yes |
| `jira_set_parent` | Set parent on issues (valid hierarchy: Epic > Story/Bug > Task) | Yes |
| `jira_clear_parent` | Remove parent from issues | Yes |
| `jira_edit_comment` | Edit existing comment by `comment_id` (ADF) | Yes |

## Delete (confirm first -- irreversible)
| Tool | Purpose | Supports `dry_run` |
|------|---------|-------------------|
| `jira_delete_issue_link` | Delete an issue link by ID | No |
| `jira_delete_attachment` | Delete an attachment by ID | No |

## Sprint & Board
| Tool | Purpose | Supports `dry_run` |
|------|---------|-------------------|
| `jira_search_by_sprint` | Search issues in a sprint (aliases: `"current"`, `"last"`, `"prev"`) | N/A (read) |
| `jira_get_sprint_issues` | Get all issues from a sprint by name | N/A (read) |
| `jira_list_available_sprints` | List sprints for a board | N/A (read) |
| `jira_get_sprint_details` | Sprint metadata (dates, state, goal) | N/A (read) |
| `jira_get_sprint_report` | Sprint completion metrics (Server/DC only) | N/A (read) |
| `jira_get_all_sprints` | Get sprints for a board, filter by state | N/A (read) |
| `jira_get_all_active_sprints` | Get active sprints for a board | N/A (read) |
| `jira_add_issues_to_sprint` | Add issues to sprint by ID | No |
| `jira_add_issues_to_backlog` | Move issues to backlog | No |
| `jira_get_issues_for_board` | Get all issues for a board (cached) | N/A (read) |
| `jira_get_all_issues_for_sprint_in_board` | Get all issues for a sprint in a board (by `board_id` + `sprint_id`) | N/A (read) |

## Sprint Export & Metrics
| Tool | Purpose | Supports `dry_run` |
|------|---------|-------------------|
| `jira_export_sprint_data` | Export sprint issues to local JSON | N/A (local) |
| `jira_export_sprint_report` | Export sprint report with metrics (Server/DC only) | N/A (local) |
| `jira_export_board_sprints` | Export all sprint metadata for a board | N/A (local) |
| `jira_compare_sprints` | Compare sprint snapshots for scope changes | N/A (local) |
| `jira_sprint_metrics_summary` | Calculate velocity, completion rate from cached data | N/A (local) |
