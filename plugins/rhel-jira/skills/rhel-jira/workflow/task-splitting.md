# RHEL Kernel JIRA: Task Splitting (Child Task Creation)

How to split a parent RHEL kernel JIRA issue into linked child tasks
using the **Planning** checkbox field.

## Overview

Task splitting creates linked child tasks from a parent issue to track
individual work streams (development, QE, documentation, etc.) separately.
This is done by setting values on the **Planning** checkbox field of the
parent issue. Each checked value triggers the creation of a corresponding
linked child task.

This typically happens during the **Planning** status, after triage and
before work begins.

## How It Works

1. Open the parent issue (Bug, Story, or Task).
2. Set one or more values on the **Planning** checkbox field.
3. JIRA automation creates linked child tasks for each selected value.
4. Child tasks inherit relevant context from the parent (component, target
   release, etc.) and are linked back to the parent.

### Setting the Planning Field via MCP Tools

Use `jira_set_custom_field` to set the Planning checkbox. First discover
the field ID with `jira_debug_fields(search="Planning")`. The field
accepts an array of string values.

## Available Child Task Types

| Planning Value | Purpose |
|---|---|
| **Upstream Development Task** | Track upstream kernel development work (patches, RFC, mailing list submissions) |
| **DEV Task** | Track RHEL downstream development work (backporting, MR creation, builds) |
| **OtherQA Testing Task** | Track additional or specialized QA testing beyond standard QE |
| **Preliminary Testing Task** | Track preliminary testing of scratch/MR builds before merge |
| **Test Case Writing Task** | Track creation of new test cases or test automation |
| **QE Task** | Track QE verification and functional testing |
| **Integration Testing** | Track integration and regression testing in nightly composes |
| **DOC Task** | Track documentation updates (release notes, man pages, guides) |
| **Root Cause Analysis Task** | Track investigation and root cause analysis for complex bugs |
| **Patch Review Task** | Track code review of patches or MRs |
| **Patch Update Task** | Track patch revision work after review feedback |

## Typical Combinations

### Bug Fix
- DEV Task, QE Task, Preliminary Testing Task
- Add Root Cause Analysis Task for complex or hard-to-reproduce bugs
- Add DOC Task if Doc Impact = Yes

### Story / RFE
- Upstream Development Task (if new upstream work needed), DEV Task,
  QE Task, Test Case Writing Task, Preliminary Testing Task
- Add DOC Task if Doc Impact = Yes

### Rebase / Large Change
- DEV Task, QE Task, Integration Testing, Preliminary Testing Task,
  Patch Review Task

## Notes

- The Planning field is a **checkbox** (multi-select) type -- multiple
  values can be selected simultaneously.
- Child tasks are **linked** to the parent, not JIRA sub-tasks. They
  appear as separate issues in the backlog and can be independently
  assigned and tracked.
- Each child task type can only be created once per parent (selecting a
  value that already has a linked child task will not create a duplicate).
- Child tasks should be assigned to the appropriate team member or group
  for that work stream (e.g., QE Task to the QA contact, DOC Task to
  the doc contact).
