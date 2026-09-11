---
name: kernel-tutorial-writer
description: >
  This skill should be used when the user wants an in-depth tutorial-style
  write-up of a Linux kernel subsystem, mechanism, or source — e.g. "write a
  tutorial on RCU", "explain jump labels end-to-end", "document how the page
  allocator works", "deep-dive on NAPI", "walk through text_poke". Also when
  extending or fixing an existing kernel tutorial in this style (missing elixir
  links, unclear paragraphs, missing sections or diagrams). Applies to
  "explain in depth" of kernel code even without the word "tutorial": the
  deliverable is a full standalone Markdown file, not a chat answer.
---

# Kernel Tutorial Writer

One self-contained Markdown file. Competent C programmer, new to this corner of the kernel. Take them from zero to a working mental model. Every claim is evidence from the tree on disk.

## When to Use

- An in-depth walkthrough of a kernel subsystem, mechanism, or source file
- Repairing a tutorial that already aims at this shape (elixir, sections, diagrams)

## When NOT to Use

- A chat-length explanation, kernel RST, commit message, or a short comment on one function
- Userspace, distro packaging, or teaching C syntax
- No kernel tree in CWD (stop and ask; do not write from memory)

This skill's directory (the folder containing this `SKILL.md`) has:

- `assets/tutorial.md.skel` — start from this shape
- `references/excerpt.md` — read before writing the first listing (prose + listing shape, not claims)
- `evals/files/golden-tutorial.md` — a complete passing specimen (heading/elixir density)
- `scripts/check-tutorial` — run on the draft before calling it done

## Investigate first

CWD must be a Linux kernel tree: a top-level `Makefile` with `VERSION`/`PATCHLEVEL` and an `include/linux/` directory. If either is missing, stop and ask; do not invent a tree or write from memory.

- Find functions, structs, and call sites by reading and searching the tree. Use `serena` and/or `semcode` when those tools are available. Read matches in full. Follow call chains both ways until the mechanism's shape is clear.
- Search `Documentation/` for locking rules, historical constraints, ABI promises. Fold that in and cite it when it shapes an explanation.
- Pin elixir to this tree. Prefer `v$(VERSION).$(PATCHLEVEL)` from the Makefile (or `make -s kernelversion` trimmed to the tag elixir actually has). Use one `https://elixir.bootlin.com/linux/<tag>/source/` prefix everywhere. Local commits on top of that tag are fine — note them; do not point elixir at a SHA it does not index.
- Start in generic code (`kernel/`, `mm/`, `include/linux/`). Go into `arch/` only when generic is a stub or the topic is arch-specific, and state which arch was walked.
- If a claim cannot be pinned to code, read more source. A wrong explanation is worse than a gap.

Write the file to a path the user named, else `./<topic>.md` in CWD. The deliverable is that file, not a chat dump.

## Structure

Copy `assets/tutorial.md.skel` and fill it. Delete the hardware-background section when the topic is bookkeeping, not micro-arch, including the `---` that precedes it. `# TITLE` and the instructional sentences under each heading are prompts. Rewrite them as real prose; leftover template voice must not appear in the output.

**No numbers in headings.** `secnum.lua` prepends them, so `## 1 Introduction` renders as "1 1 Introduction". Text and slug only.

Document title is `#` (H1), no slug. Every `##`–`######` heading has `{#slug}`:

```
# Jump labels

What jump labels are, and which kernel version this walk uses.

## Overview {#overview}
### Grace periods {#grace-periods}
```

- `{#slug}` on every `##`–`######`. Slugs are `{#lowercase-kebab}` (`{#grace-periods}`). `{#Overview}` is rejected as missing. No slug → cannot `.secref` it. H1 is the title only.
- `---` before every `##` except the first, so a long render does not run topics together.
- Every section and subsection opens with 1–2 sentences of framing before code. Opening on `Looking at the struct...` dumps the reader mid-thought.
- Hardware primer as an early `##` only if the topic needs micro-arch the reader cannot be assumed to have (instruction encoding, cache coherency, exception frames, TLB).
- Close with "Further reading in-tree": a handful of files/functions to explore next.

### Cross-refs

Hardcoded "see section 9.5" / "§4.2" rot the moment a section is reordered.

```
## Life of a static key: boot, enable, disable {#life-of-a-static-key-boot-enable-disable}

...covered in [](#life-of-a-static-key-boot-enable-disable){.secref}.
```

A Lua filter (`secnum.lua`) turns `.secref` into live "§9.5" text. That filter belongs to the document's pandoc build, not the kernel tree. If this document is not built with `--lua-filter=secnum.lua`, tell the user rather than leaving links unresolved.

## Source listings

Read `references/excerpt.md` before writing the first listing. Copy its shape.

Show a listing only when the reader needs the exact shape (subtle control flow, non-obvious ordering, a trick that only makes sense next to the bytes). Skip listings the prose already covers.

Long or multi-purpose functions: break into the smallest logical pieces (a few lines each) and explain each piece before the next. A wall of code with one explanation below forces the reader to hold the whole function in their head.

Reproduce source verbatim. If comments are added that are not in the kernel, say so immediately above the listing ("the comments below are this tutorial's own annotations, not present in the kernel source") so they are not mistaken for maintainer comments.

## Multi-step mechanisms

Setup sentence first ("the loop does three things per entry, in this order"). Without it, the first bold item reads as a definition dropped from nowhere.

- Function already shown as one listing → short numbered list, 1–2 sentences per item, no code.
- Each step needs its own snippet → `**1. Bail on user mode.**` then those lines.

When a later step relies on an earlier one, say so explicitly ("building both `code` and `nop` up front is what makes the next safety check possible").

Ground an invariant in one real call site from the tree, not a hypothetical. Flag that shift with "Concretely:".

When a formula, encoding, or convention recurs, invoke it by name with a `.secref`. Re-deriving it looks like a new idea.

## Diagrams, sidebars, footnotes

- **ASCII diagrams** (fenced code blocks): structs, state machines, before/after layouts. Label an edge when the arrow alone would not say why.
- **Sidebars** (`>`): skippable tangents (history, corner cases). Must reach a conclusion. May be a long numbered code walkthrough if nothing outside the blockquote depends on it.
- **Footnotes** (`[^label]`): short definitions of off-topic terms. Marker at first mention; definition right after that paragraph, not at document end — the reader should not have to hunt.

## Elixir links

Form:

`https://elixir.bootlin.com/linux/<version>/source/<path>#L<line>`

A link that lands on the wrong line looks verified and is not. That is worse than no link.

**In-tree files.** Every prose mention of a path that exists in the tree (`kernel/jump_label.c`, `include/linux/jump_label.h`, `Documentation/core-api/jump-labels.rst`) is an elixir link. Do not leave that path in backticks only. A whole-file link may omit `#L`; add an anchor when pointing to a particular definition or line.

**Symbols.** Functions, structs, macros, and globals: elixir-link the first mention in each subsection (`##` or `###`). Later mentions in that same subsection are backticks, not a second elixir link. A new `##` or `###` starts the count again. `####` does not.

Do not link: symbols inside fenced code, listings, or ASCII diagrams; generic English that overlaps a C word (`key`, `entry`, `text`, `type` used loosely, `foo->bar` as a field access).

Do not re-link a symbol in the same subsection because the paragraph revolves around it. One link at first mention is the density; more turns the prose into a carpet of URLs.

### Line numbers

- Symbol links have `#L<number>`. A bare URL is fine when the link deliberately refers to a whole file, such as an in-tree document or a file in “Further reading”.
- `#L` is the definition line (signature, `struct`/`typedef`, `#define`). Confirm against the file on disk, not memory.
- Same symbol → same line number everywhere. Later subsections that re-link it must not drift.
- Nearby names (`foo` vs `foo_bar`): confirm the line is the one being discussed.

`scripts/check-tutorial` errors on mixed versions, missing `#L` on symbol links, `#L` that does not contain the symbol, the same symbol elixir-linked twice in one `##`/`###` subsection, and an in-tree path mentioned but not linked. First-mention-is-linked (rather than omitted) is Pass 1: the checker cannot know every identifier.

## Style

Write as a colleague sitting next to the reader at a terminal, not as a model producing a tutorial. The existing bans (possessive `'s`, defensive filler, numbered headings) still apply; they are not a license to sound like a bullet list expanded into sentences.

- Assume C. Do not explain C syntax.
- Short paragraphs; one job each. Sentences inside a paragraph connect. A stack of isolated declarations reads generated even when each sentence is true.
- Never possessive `'s` ("the task's state"). "Of the" / compound nouns ("the state of the task", "task state") force the noun relationship into the open.
- Concrete, not vague ("walks the sorted table and stops at the first entry belonging to a different key", not "does some bookkeeping").
- No defensive filler: arguing a section is worth reading; "not X" after already stating X; hedges ("it is worth noting", "importantly", "as one might expect"). Optional-config context is one direct sentence, not an argument.
- Direct colleague prose. Bad: "this is where a reader carrying the rules forward would go wrong". Good: "Compare this with the `=y` version, which clamps negative values."
- **Natural, not generated.** Do not announce structure ("This section will…", "There are three parts."). Do not open consecutive paragraphs with the same mold ("The X is… The Y is…"). Vary sentence length: a longer why, then a short fact. Read `references/excerpt.md` for a good/bad pair.
- At most two or three `.secref` per paragraph, and only when the reader needs to look something up.
- Fixes to existing docs: write the paragraph as it should always have read. A future reader has no memory of the edit conversation.

## Review (required)

A first draft is not the deliverable. Two separate passes — readability and grammar are different mistakes, and catching both at once misses half of each.

**Pass 1 — readability/structure:** unreadable paragraphs; missing intro sentences; possessive `'s`; in-tree path left unlinked; symbol skipped on first mention in a subsection or elixir-linked again later in it; missing or unverified elixir `#L` on symbol links; missing `{#slug}` on `##`–`######`; missing `---` before later `##`; numbers in headings; oversized listings; defensive filler; stiff/model prose (announced structure, parallel paragraph openers, isolated declarations); leftover skeleton meta (`Framing:`, `Lede:`, `# TITLE`); excess `.secref`.

**Pass 2 — grammar** (skip code, diagrams, kernel identifiers): subject-verb agreement and tense (timeless fact vs narrated sequence — pick one per passage); run-ons and comma splices; `a`/`an`/`the` and singular/plural around kernel terms ("the jump_label subsystem"); dangling modifiers; fragments; punctuation inside Markdown links and footnotes.

Resolve this skill's installed directory, then run its bundled checker against the kernel tree. Do not assume `scripts/` exists in the kernel workspace:

```
<skill-dir>/scripts/check-tutorial <draft-path> --tree <kernel-tree>
```

Fix every error. Warnings are possessive `'s` leftovers — rephrase those too. A clean checker run does not prove first-mention coverage or that the prose sounds human; Pass 1 still has to.

Fix what is wrong. Do not rewrite correct sentences for variety. If a grammar fix would change a technical claim, take the smallest correction that does not.

Done only after both passes and a clean checker run.
