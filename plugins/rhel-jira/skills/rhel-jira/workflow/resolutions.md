# RHEL Kernel JIRA: Resolution Values

When closing or resolving an issue, a resolution must be provided.
These are the valid resolution values for the `jira_transition_issue` tool.

## Resolution Values

| Resolution | When to Use |
|------------|-------------|
| **Fixed** | The issue has been resolved with a code change or configuration fix. |
| **Won't Fix** | The issue is acknowledged but will not be addressed (e.g. by design, out of scope). |
| **Duplicate** | The issue is a duplicate of another. Link to the original issue. |
| **Cannot Reproduce** | The issue could not be reproduced with the information provided. |
| **Not a Bug** | The reported behavior is not a defect (working as designed). |
| **Done** | General completion (typically for Tasks and Stories, not Bugs). |
| **Done-Errata** | Used by automation when an advisory ships. All issues in the advisory are auto-closed with this resolution. Do not set manually. |
| **Won't Do** | Similar to Won't Fix; the work will not be done (typically for Tasks/Stories). |
| **Incomplete** | The issue lacks sufficient information and the reporter has not responded. |

## Guidelines

- **Bugs** should generally use "Fixed", "Won't Fix", "Duplicate", "Cannot Reproduce", or "Incomplete".
- **Tasks and Stories** should generally use "Done" or "Won't Do".
- **CVE Trackers** should use "Fixed" when the CVE is addressed, or "Won't Fix" if the CVE does not affect the target release.
- When using "Duplicate", always add a link to the original issue before or during the transition.
- When using "Won't Fix" or "Won't Do", add a comment explaining the rationale.
- **"Done-Errata"** is reserved for automation. Do not set this resolution manually.
