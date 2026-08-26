---
name: cover
description: Generate a Linux-kernel-style patch-series cover letter from Git history. Use when the user asks for a cover letter or PATCH 0/N message.
---

# Kernel patch-series cover letter

Determine the range from an explicit commit count, a baseline branch, or the upstream branch; reject conflicting range inputs and stop for an empty range. Read the commits and diff before writing.

Produce a `[PATCH 0/N]` subject and a concise, 72-column prose letter covering the motivation, series-level approach, and testing. Keep it high-level: do not restate every patch or invent metrics, issue IDs, or rationale absent from the history.

For a versioned series (output path matching `v<N>-*` with N>1, or an explicit vN request), recover the previous cover when LKML tools (`lkml_get_user_series`, `lkml_search_patches`, `lkml_get_thread`, `lkml_get_raw`) are available:

1. Look up the prior cover by author email, then topic search (N=2: unversioned `[PATCH 0/X]`; N>2: `vN-1`). Ask for a Message-ID if lookup fails. Retry a failed LKML call twice, then fall back.
2. Keep the prior subject description and every `Changes in v<X>:` section verbatim.
3. Compare previous patches to the current series. Add only substantive `Changes in v<N>:` (structural first, then real code or bugfix changes; credit reviewers). Skip whitespace and rewording.

If those tools are missing, preserve prior `Changes in vN:` sections when the user supplies them, warn that LKML lookup was skipped, and generate a first-round letter when no prior cover is available.

Show the final letter before writing. If the user gives an output path, replace only the `git format-patch` subject/blurb markers when present; otherwise write the requested file after confirmation.
