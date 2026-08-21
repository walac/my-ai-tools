# RHEL Kernel JIRA: Z-Stream Process

Requirements and workflow for including fixes in RHEL z-stream releases.

## What is a Z-Stream?

Z-stream releases (e.g. RHEL 9.4.z) are minor update releases that include
critical bug fixes, security patches, and hardware enablement. They follow
the main Y-stream release.

## Inclusion Criteria

Fixes typically need to meet one or more of these criteria:

- Security fix (CVE with severity >= Important)
- Data corruption or loss
- System crash or hang
- Regression from previous release
- Critical hardware enablement

## Required Fields

When marking an issue for z-stream inclusion:

| Field | JQL Name | What to Set |
|-------|----------|-------------|
| Z-Stream | `zstream` | Set to indicate z-stream targeting |
| Target Release | `target_release` | Must specify the z-stream version (e.g. 9.4.0.z) |
| Severity | `severity` | Must be set (Urgent, Important, Moderate, or Low) |
| Release Blocker | `release_blocker` | Set if the fix blocks the z-stream release |
| Component | `component` | At least one component set |
| Description | `description` | Non-empty |
| Assignee | `assignee` | Non-empty |

## Process

1. Issue is identified as z-stream candidate (meets inclusion criteria).
2. Issue is flagged with the appropriate `zstream` field value.
3. Fix is developed and reviewed.
4. Fix is included in the z-stream build.
5. QE verifies the fix in the z-stream context.
6. Fix ships with the z-stream errata.

## JQL Examples

Open z-stream issues for a specific release:
```
project = RHEL AND zstream is not EMPTY AND target_release = "9.4.0.z" AND resolution = EMPTY
```

Z-stream issues missing required fields:
```
project = RHEL AND zstream is not EMPTY AND (severity is EMPTY OR target_release is EMPTY OR assignee is EMPTY) AND resolution = EMPTY
```
