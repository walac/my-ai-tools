# JQL query templates for RHEL kernel Jira work

## My Issues

- My open issues: `assignee = currentUser() AND resolution = EMPTY ORDER BY priority DESC`
- Issues I'm watching: `watcher = currentUser() AND resolution = EMPTY ORDER BY updated DESC`

## By Status

- In Progress kernel issues: `project = RHEL AND status = "In Progress" AND component in componentMatch("kernel") ORDER BY priority DESC`
- New/untriaged kernel issues: `project = RHEL AND status = "New" AND resolution = EMPTY AND component in componentMatch("kernel") ORDER BY created DESC`

## By Target Release

- Open issues for a release: `project = RHEL AND target_release = "9.6.0" AND resolution = EMPTY ORDER BY priority DESC`
- Missing target release: `project = RHEL AND target_release is EMPTY AND resolution = EMPTY AND component in componentMatch("kernel")`

## By Severity / Priority

- Urgent and Important: `project = RHEL AND severity in ("Urgent", "Important") AND resolution = EMPTY ORDER BY severity ASC, priority DESC`
- Missing severity: `project = RHEL AND severity is EMPTY AND resolution = EMPTY AND component in componentMatch("kernel")`

## Release Blockers

- All release blockers: `project = RHEL AND release_blocker is not EMPTY AND resolution = EMPTY ORDER BY priority DESC`

## Triage / Housekeeping

- Unassigned kernel issues: `project = RHEL AND assignee is EMPTY AND component in componentMatch("kernel") AND resolution = EMPTY ORDER BY created DESC`
- Missing severity and target release: `project = RHEL AND severity is EMPTY AND target_release is EMPTY AND resolution = EMPTY AND component in componentMatch("kernel")`
- Recently updated (last 7 days): `project = RHEL AND component in componentMatch("kernel") AND resolution = EMPTY AND updated >= -7d ORDER BY updated DESC`

## Agile

- My current sprint tasks: `assignee = currentUser() AND sprint in openSprints() ORDER BY priority DESC`
- My open current sprint tasks: `assignee = currentUser() AND sprint in openSprints() AND resolution = EMPTY ORDER BY priority DESC`

## Notes

- `componentMatch("kernel")` matches all components starting with "kernel".
- All queries exclude Closed issues unless noted. Adjust `ORDER BY` as needed.
- For ad-hoc queries, prefer `resolution = EMPTY` over `status != Closed` to catch all non-resolved statuses (including Planning, Refinement, etc.).
