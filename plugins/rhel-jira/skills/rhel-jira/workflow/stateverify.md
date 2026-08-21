# RHEL Kernel JIRA: Ticket State Verification

Detailed field-completeness checks for common readiness states. Read this
file when asked to "verify", "check", or "audit" a ticket's readiness.

## How to Run a Verification

1. Fetch the issue with `jira_get_issues(issue_keys=[key], all_fields=true)`.
2. Look up the requested verification state in the tables below.
3. For each required field, check whether it is set and non-empty.
4. For fields with constrained values (marked **valid values**), confirm the
   current value is in the allowed set.
5. Report results as a checklist: pass/fail per field, with the current value
   shown for failures.

If the user does not specify a state, infer the most likely one from the
issue's current status (see **Default State Mapping** below).

## Verification States

### sprint-ready

The issue has enough context to be pulled into a sprint.

| Field (Display Name) | JQL Name | Condition |
|----------------------|----------|-----------|
| Component/s | `component` | At least one component set |
| Assigned Team | `assignedteam` | Non-empty |
| Sprint | `sprint` | Assigned to a sprint |

### triage-complete

The issue has been triaged and is ready to move from **New** to **Planning**.

| Field (Display Name) | JQL Name | Condition |
|----------------------|----------|-----------|
| Component/s | `component` | At least one component set |
| Summary | `summary` | Non-empty |
| Description | `description` | Non-empty, with a meaningful problem statement |
| Severity | `severity` | Set to one of: Urgent, Important, Moderate, Low |
| Priority | `priority` | Non-empty |
| Affects Version/s | `affectedVersion` | At least one version set (Bug type only) |

### planning-complete

The issue is fully scoped and ready to move from **Planning** to **In Progress**.

| Field (Display Name) | JQL Name | Condition |
|----------------------|----------|-----------|
| Component/s | `component` | At least one component set |
| Assigned Team | `assignedteam` | Non-empty |
| Assignee | `assignee` | Non-empty |
| Fix Version/s | `fixVersion` | At least one version set |
| Target end | `target_end` | Date set (ITM) -- not required for z-stream clones |
| Doc Impact | `doc_impact` | Set to "Yes" or "No" |
| Severity | `severity` | Set to one of: Urgent, Important, Moderate, Low |
| Description | `description` | Non-empty |

### integration-ready

The issue has completed development and is ready to move from **In Progress** to **Integration**.

| Field (Display Name) | JQL Name | Condition |
|----------------------|----------|-----------|
| Fixed In Build | `fixed_in_build` | Non-empty (NVR of the build) |
| Errata Link | `errata_link` | Non-empty (advisory URL) |
| Preliminary Testing | `preliminary_testing` | Set to **Pass** |
| Assignee | `assignee` | Non-empty |
| Fix Version/s | `fixVersion` | At least one version set |
| Target Release | `target_release` | Non-empty |

### zstream-ready

The issue is properly configured for z-stream inclusion.

| Field (Display Name) | JQL Name | Condition |
|----------------------|----------|-----------|
| Z-Stream | `zstream` | Non-empty |
| Target Release | `target_release` | Set to a z-stream version (e.g. 9.4.0.z) |
| Severity | `severity` | Set to one of: Urgent, Important, Moderate, Low |
| Component/s | `component` | At least one component set |
| Description | `description` | Non-empty |
| Assignee | `assignee` | Non-empty |

## Default State Mapping

When the user asks to "verify RHEL-XXXXX" without specifying a state, use the
issue's current status to pick the verification:

| Current Status | Default Verification |
|----------------|---------------------|
| New | triage-complete |
| Planning | planning-complete |
| In Progress | integration-ready |

If the issue is already Closed or Release Pending, report that no forward
verification is applicable and offer to check a specific state instead.

## Output Format

Present results as a checklist with clear pass/fail indicators:

```
Verification: sprint-ready  --  RHEL-12345

[PASS] Component/s: kernel / Core / Memory Management
[PASS] Assigned Team: rhel-kernel-ft-plumbers-1
[FAIL] Sprint: (not set)

Result: 1 of 3 checks failed -- issue is NOT sprint-ready.
  -> Sprint must be assigned before pulling into a sprint.
```

For failures, include a brief recommendation on what to set or fix.

## Multiple Issues

When asked to verify a list of issues (or results from a JQL query), run the
verification for each issue and produce a summary table:

```
Sprint-Ready Verification Summary (3 issues)

| Issue | Pass | Fail | Missing Fields |
|-------|------|------|----------------|
| RHEL-111 | 3/3 | 0 | -- |
| RHEL-222 | 1/3 | 2 | Sprint, Assigned Team |
| RHEL-333 | 2/3 | 1 | Sprint |
```
