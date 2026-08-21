# RHEL Kernel JIRA: Release Blockers and Exceptions

Process for requesting and managing Release Blockers and Release Commit
Exceptions in the RHEL kernel workflow.

## When Does This Apply?

After the normal development phase, a **release candidate (RC) branch** is
created. To target work for this RC branch, you need either an approved
**Release Blocker** or an approved **Release Commit Exception**. Both use
the `release_blocker` field.

## Release Blocker

A Release Blocker means **"we can't do the release without this."** In
theory, the entire release will not ship until all approved release blockers
are resolved.

### Process

1. Set the **Release Blocker** field to **"Proposed Blocker"**
2. Automation creates a **RHELMISC** ticket for the approval group to discuss the issue
3. Fill in the supplied template in the RHELMISC ticket promptly
4. The approval group reviews the request in the B&E Dashboard
5. The approval group sets the field to **"Approved Blocker"** or **"Rejected Blocker"**

## Release Commit Exception

A Release Commit Exception allows changes to be made to the RC branch
without blocking the release.

### Process

1. Set the **Release Blocker** field to **"Proposed Exception"**
2. Automation creates a **RHELMISC** ticket for the approval group to discuss the issue
3. Fill in the supplied template in the RHELMISC ticket promptly
4. The approval group reviews the request in the B&E Dashboard
5. The approval group sets the field to **"Approved Exception"** or **"Rejected Exception"**

## Cross-Classification

The review team may reclassify requests:

- A **Proposed Blocker** may be determined to not block the release but
  still warrant an exception -- it will be set to **"Approved Exception"**
  instead
- A **Proposed Exception** may be determined to actually block the release
  -- it will be set to **"Approved Blocker"** instead

## Valid `release_blocker` Field Values

| Value | Meaning |
|-------|---------|
| Proposed Blocker | Request submitted for release blocker review |
| Approved Blocker | Blocker approved -- release will not ship without this |
| Rejected Blocker | Blocker request denied |
| Proposed Exception | Request submitted for RC branch commit exception |
| Approved Exception | Exception approved -- changes allowed on RC branch |
| Rejected Exception | Exception request denied |

## JQL Examples

```
project = RHEL AND release_blocker = "Proposed Blocker" AND resolution = EMPTY
```

```
project = RHEL AND release_blocker in ("Approved Blocker", "Approved Exception") AND resolution = EMPTY
```
