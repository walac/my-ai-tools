# RHEL Kernel JIRA: JQL Field Reference

Mapping of display names to JQL field names. Use **JQL Name** for queries; use `jira_debug_fields` to find `customfield_NNNNN` IDs for `jira_set_custom_field`.

| Display Name | JQL Name | Type |
|---|---|---|
| Assigned Team | `assignedteam` | Select/Option |
| Target Release | `target_release` | Version |
| Target Version | `target_version` | Version |
| Fix Version/s | `fixVersion` | Version |
| Affects Version/s | `affectedVersion` | Version |
| Severity | `severity` | Select |
| Upstream Kernel Target | `upstream_kernel_target` | Text |
| Z-Stream | `zstream` | Select |
| Target Backport Versions | `target_backport_versions` | Multi-select |
| QA Contact | `qa_contact` | User |
| Release Blocker | `release_blocker` | Select |
| Errata Link | `errata_link` | URL |
| Bugzilla Bug | `bugzilla_bug` | Text |
| Commit Hashes | `commit_hashes` | Text |
| Sub System Group | `sub_system_group` | Select |
| Developer | `developer` | User/Group |
| Team | `team` | Select |
| Story Points | `story_points` | Number |
| Sprint | `sprint` | Sprint |
| Dev Target end | `dev_target_end` | Date |
| Target end | `target_end` | Date |
| Doc Impact | `doc_impact` | Select |
| Release Note Type | `release_note_type` | Select |
| Release Note Text | `release_note_text` | Text |
| Git Pull Request | `git_pull_request` | URL |
| Testable Build | `testable_build` | Text |
| Preliminary Testing | `preliminary_testing` | Select |
| Fixed In Build | `fixed_in_build` | Text |
| Test Link | `test_link` | URL |
| Status Summary | `status_summary` | Rich Text |
| Acceptance Criteria | `acceptance_criteria` | Rich Text |
| Epic Link | `epic_link` | Issue Key |
| Epic Name | `epic_name` | Text |
| Parent Link | `parent_link` | Issue Key |

Standard JIRA fields use their normal names: `status`, `assignee`, `priority`, `project`, `labels`, `components`.

**Key rules:**
- JQL custom field names are lowercase; some use underscores (`target_release`), some do not (`assignedteam`) -- verify with `jira_debug_fields` if unsure.
- Option/select fields require exact match -- no wildcards or `~` operator.
- `assignedteam` and `team` are different fields.
- Use `jira_debug_fields(search="field name")` to find the `customfield_NNNNN` ID for `jira_set_custom_field`.
- The `epic_name` parameter in `jira_create_issue` sets the name when creating an Epic-type issue. To link a child issue to an existing epic, use `jira_set_custom_field` with the Epic Link field ID.
