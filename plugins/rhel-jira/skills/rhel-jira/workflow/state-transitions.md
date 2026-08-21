# RHEL Kernel JIRA: Per-Status Activity Guide

Detailed guidance for what to do at each workflow status. Read this file
when triaging, transitioning, or auditing issues — it explains the expected
activities and fields for each status, not just the transition mechanics.

## New

**Goal**: Create the issue and ensure it is filed against the correct component.

- **Issue types**:
  - **Bug** -- for defects
  - **Story** -- for new functionality, RFEs, hardware enablement (should almost always be a child of an Epic)
  - **Task** -- recommended for rebases; link to resolved bugs/stories with "Blocks" / "Blocked By"
- **Set the Component** -- an automation script will auto-assign:
  - Pool Team, Assignee, Developer, QA Contact, Doc Contact
  - Sub-components are available in forward-slash notation (e.g. "kernel / Core / Scheduler")
- **Affects Version/s** -- set for defects to indicate which RHEL version the bug was discovered in
- **Target Version** -- optional; acts as a request for the team to consider including the work
- **Description** -- required; explain the problem or desired outcome and why the change should be made
- **Team review** -- verify the component is correct; if not, select the best alternative (triggers reassignment)
- **Triage complete** -- move to **Planning**
- **Direct close** -- tickets can move directly to Closed with Won't Fix, Not a Bug, Duplicate, etc.
- Few issues should remain in New for long; transferring out typically requires minimal effort

## Planning

**Goal**: Triage, scope, and commit the work to a release plan.

- **Fix Version/s** -- required when the team agrees to include the item in their release plan. Setting Fix Version (and later Target end) is understood as a proxy for approval, replacing Bugzilla's "release:+"
- **Dev Target end (DTM)** -- recommended (not required for z-stream clones). Date when development is expected to complete
- **Target end (ITM)** -- required (not for z-stream clones). Set by QE to the best estimate of when changes will be fully verified in a nightly compose. Cements approval for the release
- **Docs Impact** -- required. Set to "No" if no documentation changes needed; "Yes" if unsure or known impact
- **Move to In Progress** -- when work begins: upstream work, research, code on local machine, scoping testing infrastructure, or beginning documentation
- **Definition of Ready** -- teams determine their own rules for when a ticket is ready to move to In Progress (e.g. Dev ack, QE ack). Check with your SST lead

## In Progress

**Goal**: Develop, test preliminary builds, and get the fix attached to an erratum.

### MR Creation

- Dev creates an MR referencing the Jira ticket
- For GitLab dist-git (`gitlab.com/redhat/centos-stream`): link is auto-created as an Issue Link
- For non-GitLab repos (GitHub, etc.): use the **Git Pull Request** field (also serves as fallback if GitLab integration is unavailable)

### Preliminary Testing Workflow

1. Dev marks **Preliminary Testing: Requested** when the MR is ready for review (pre-merge) OR when merged into a -candidate build
2. QE runs preliminary testing and sets **Preliminary Testing: Pass** or **Fail**
3. Builds should not be marked -pending or attached to erratum until PT: Pass

### Testable Builds

Optional; add references when scratch/MR builds are available for QE.

### Merge Workflows

- **Early Merge** (default): Dev verifies MR via automated tests and manual review, merges, and builds binary artifacts
- **Late Merge** (optional): Maintainer checks tickets with PT: Pass, merges into main repo, and ensures the package is built

### Required Fields Before Integration

- **Fixed In Build** -- the NVR of the official build containing the patches (usually set automatically)
- **Errata Link** -- link to the advisory URL when the ticket is included in an erratum
  - Responsibility chain for attaching to erratum: (1) Automation, (2) Last actor, (3) QE, (4) Devel, (5) SST Lead
- **Docs** -- if Doc Impact = Yes, update **Release Note Type** and **Release Note Text** throughout development
- **Auto-transition** -- Errata Link + PT: Pass triggers automatic move to **Integration**

## Integration

**Goal**: Final verification of the build in nightly Composes.

- Preliminary Testing is complete and the build is attached to an erratum with the -pending tag
- Build is included in **nightly Composes**
- QE runs:
  - Final functional tests
  - Integration testing
  - Regression testing
- QE moves the ticket to **Release Pending** once satisfied with verification

## Release Pending

**Goal**: Confirm all tickets in the errata are verified and ready to ship.

- All Jira tickets referenced in the errata must be in **Release Pending** status before shipping
- This status signals that all final verifications have passed and the code is waiting to ship

## Closed

**Goal**: Record the shipped state and release metadata.

- **Automation**: When the advisory ships, all issues in the advisory are moved to Closed with resolution **"Done-Errata"**
- **PgM**: Marks Fix Version as Released
- **Automation**: Errata tool timestamps all tickets with the **Release Date**

### Bugzilla Migration Notes

Some Bugzilla resolutions do not exist in Jira:
- WORKSFORME -> Closed + "Cannot Reproduce" or "Not a Bug"
- CURRENT RELEASE -> Closed + proper Fix Version set
- DEFERRED -> Do **not** close; bring back to "New" or "Planning"
