# RHEL Kernel JIRA Workflow Reference -- state machine, resolutions, z-stream, blockers, task splitting, and field verification.

## Detailed Workflow Guides

For in-depth guidance beyond this summary, read the appropriate file from `workflow/`:

| Need | File |
|------|------|
| Per-status activity guide (what to do at New, Planning, In Progress, etc.), MR workflows, preliminary testing steps | `workflow/state-transitions.md` |
| Detailed verification checklists with JQL field names, output format, multi-issue summaries | `workflow/stateverify.md` |
| Resolution values, per-issue-type guidelines, Bugzilla mapping | `workflow/resolutions.md` |
| Release blocker and exception process, approval workflow, cross-classification | `workflow/blockers-exceptions.md` |
| Task splitting via Planning field, child task types, typical combinations | `workflow/task-splitting.md` |
| Z-stream inclusion criteria, required fields, JQL examples | `workflow/zstream.md` |

## Status Flow

```
New -> Planning -> In Progress -> Integration -> Release Pending -> Closed
```

| Status | Purpose |
|--------|---------|
| New | Untriaged; set component, severity, description, affects version (bugs) |
| Planning | Scoping; set fix version, target end (ITM), docs impact, assignee |
| In Progress | Dev/QE/docs work; MRs, preliminary testing, errata attachment |
| Integration | Build in nightly composes; QE runs final/regression testing |
| Release Pending | All verification done; waiting for advisory to ship |
| Closed | Resolved and released (or otherwise closed) |

## Transition Map

| From | To | Required Fields |
|------|----|-----------------|
| New | Planning | -- |
| New | Closed | Resolution |
| Planning | In Progress | Assignee (recommended, not enforced), fix version, target end (ITM = Iteration Target Milestone), docs impact |
| Planning | Closed | Resolution |
| In Progress | Integration | Fixed In Build, Errata Link, Preliminary Testing: Pass |
| In Progress | Closed | Resolution |
| Integration | Release Pending | QE verification complete |
| Integration | Closed | Resolution |
| Release Pending | Closed | Resolution |

**Backward transitions**: Not all backward transitions are available (e.g., Integration back to In Progress may not exist). Always use `jira_get_transitions` to discover which transitions are valid for the current status rather than assuming any transition is possible.

## Automation Triggers

| Trigger | Action |
|---------|--------|
| MR created in `gitlab.com/redhat/centos-stream` with Jira key | Auto-transition to In Progress (kernel/virt teams) |
| Errata Link set + Preliminary Testing: Pass | Auto-transition to Integration |
| Advisory shipped | Auto-close with "Done-Errata" + set Release Date |

## Resolutions

- **Fixed** -- code/config change resolved the issue
- **Done** -- general completion (Tasks/Stories)
- **Done-Errata** -- automation-only; set when advisory ships
- **Won't Fix** -- acknowledged but won't address (add comment explaining why)
- **Won't Do** -- work won't be done (Tasks/Stories equivalent of Won't Fix)
- **Duplicate** -- link to original issue before closing
- **Cannot Reproduce** -- could not reproduce with info provided
- **Not a Bug** -- working as designed
- **Incomplete** -- insufficient info, reporter unresponsive

Guidelines: Bugs use Fixed/Won't Fix/Duplicate/Cannot Reproduce/Incomplete. Tasks/Stories use Done/Won't Do. CVE Trackers use Fixed or Won't Fix. Always verify exact values with `jira_get_resolutions` at runtime — names and casing may vary by instance.

## Z-Stream Process

**Inclusion criteria** (one or more): CVE >= Important, data corruption/loss, crash/hang, regression, critical HW enablement.

**Required fields**: `zstream` (set), `target_release` (z-stream version, e.g. 9.4.0.z), `severity`, `release_blocker` (if blocking).

**Flow**: Identify candidate -> flag zstream field -> develop/review fix -> QE verifies in z-stream context -> ships with z-stream errata.

## Release Blockers and Exceptions

Applies after the RC branch is created. Use the `release_blocker` field.

| Value | Meaning |
|-------|---------|
| Proposed Blocker | Submitted for blocker review |
| Approved Blocker | Release will not ship without this |
| Rejected Blocker | Blocker request denied |
| Proposed Exception | Submitted for RC commit exception |
| Approved Exception | RC branch changes allowed |
| Rejected Exception | Exception denied |

**Process**: Set field to Proposed Blocker/Exception -> automation creates RHELMISC ticket -> fill template -> approval group reviews -> field updated to Approved/Rejected. Cross-classification is possible (blocker may become exception or vice versa).

## Task Splitting

Set the **Planning** checkbox field on the parent issue to create linked child tasks.

| Planning Value | Purpose |
|----------------|---------|
| DEV Task | Downstream development (backport, MR, builds) |
| Upstream Development Task | Upstream patches, RFC, mailing list |
| QE Task | QE verification and functional testing |
| Preliminary Testing Task | Testing scratch/MR builds pre-merge |
| Integration Testing | Integration/regression testing in composes |
| Test Case Writing Task | New test cases or automation |
| OtherQA Testing Task | Specialized QA beyond standard |
| DOC Task | Docs updates (release notes, man pages) |
| Root Cause Analysis Task | Investigation for complex bugs |
| Patch Review Task | Code review of patches/MRs |
| Patch Update Task | Patch revision after review feedback |

**Typical combos**: Bug = DEV + QE + Preliminary Testing (+RCA if complex). Story/RFE = Upstream Dev + DEV + QE + Test Case Writing + Preliminary Testing. Rebase = DEV + QE + Integration Testing + Preliminary Testing + Patch Review. Add DOC Task when Doc Impact = Yes.

## Field Verification Checklists

Use these to audit ticket readiness. Default verification is based on current status.

**triage-complete** (New -> Planning): Component, Summary, Description, Severity (Urgent/Important/Moderate/Low), Priority, Affects Version (bugs only).

**planning-complete** (Planning -> In Progress): Component, Assigned Team, Assignee, Fix Version, Target End (ITM = Iteration Target Milestone; not for z-stream clones), Doc Impact (Yes/No), Severity, Description.

**sprint-ready**: Component, Assigned Team, Sprint.

**integration-ready** (In Progress -> Integration): Fixed In Build (NVR), Errata Link (URL), Preliminary Testing = Pass, Assignee, Fix Version, Target Release.

**zstream-ready**: zstream (set), Target Release (z-stream version), Severity, Component, Description, Assignee.

### Default Verification by Status

| Status | Verify |
|--------|--------|
| New | triage-complete |
| Planning | planning-complete |
| In Progress | integration-ready |

If Closed or Release Pending, no forward verification applies.
