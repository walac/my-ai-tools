---
name: kernel-tutorial-writer
description: Create or revise long-form Linux kernel tutorials grounded in a local kernel tree and formatted for the kernel-tutorials Pandoc build. Use for sustained source-led explanations, not short answers or non-kernel documentation.
---

# Kernel Tutorial Writer

Write one self-contained Markdown file that the `kernel-tutorials` Pandoc build can render. Every implementation claim must be supported by the local kernel tree. The user decides the question, audience, depth, and narrative order; the build decides the Markdown contract.

## Investigate before drafting

The working directory must be a Linux kernel tree: a top-level `Makefile` with `VERSION` and `PATCHLEVEL`, plus `include/linux/`. If it is absent, ask for the tree. Do not write source-specific material from memory or Internet searches.

- Read definitions, callers, and relevant in-tree documentation. Follow call chains far enough to explain the mechanism rather than one isolated function.
- Search `Documentation/` for locking rules, historical constraints, ABI promises. Fold that in and cite it when it shapes an explanation
- Use semcode MCP to investigate the source code. Falls back to serena MCP if semcode fails.
- Prefer generic code first; investigate architecture code when the mechanism is architecture-specific or the generic path is a stub. State the architecture when it matters.
- Pin all Elixir links to one tag corresponding to the tree, normally `v$(VERSION).$(PATCHLEVEL)`. Note relevant local commits without inventing unindexed URLs.

Write to the path the user supplies, otherwise `./<topic>.md` in the kernel tree. The deliverable is the Markdown file, not a chat-only tutorial.

## Preserve the build contract

The output must work with the Pandoc build in `kernel-tutorials`, which removes the first line for document metadata and always runs `secnum.lua`.

- Put the document title as the first line: one H1 with no `{#slug}`. The build removes this line and uses it as the rendered title.
- Every H2 through H6 needs a unique lowercase-kebab `{#slug}`. Do not put section numbers in headings; `secnum.lua` adds them.
- Put `---` immediately before every H2 except the first. This preserves the collection's page and section separation.
- Use `[](#slug){.secref}` for internal section references. Each target must exist. Do not write hard-coded section numbers.
- Keep footnote definitions after the list that contains their markers; definitions inside a list split the list in Pandoc output.
- Use language tags for source listings. Reserve untagged fenced blocks for diagrams or other non-source material.

The required syntax does not prescribe a table of contents. Choose the H2/H3 structure only after investigation. Use the sequence that answers the user’s question: it may focus on an API, an execution path, initialization, a data representation, a hardware prerequisite, or another source-backed story. Include diagrams, source excerpts, sidebars, footnotes, or further reading only when they help the reader.

## Cite source accurately

Use Elixir links for every prose occurrence of a real in-tree path, and link a real symbol on its first prose occurrence in each `##` or `###` subsection. Link symbols to their definition line with `#L<number>`; whole-file links may omit the anchor. Confirm the path and line against the local tree. Do not link identifiers in source listings, literal expressions, hypothetical names, family wildcards, or generic prose that happens to match an identifier.

Use a listing only when the exact source shape, ordering, or local trick is needed. Reproduce source faithfully, split long listings at the reader’s conceptual boundaries, and label any comments that are added by the tutorial.

## Write and review

Write direct, connected prose for the specified audience. Make sure the text looks like human written. Assume C knowledge unless the user asks otherwise. Prefer concrete behavior and causal relationships. Repair existing text as though the revision had always been part of the document.

Review separately for technical clarity and grammar. Confirm that the document answers the requested question, follows a coherent route through the code, distinguishes fact from inference, and contains no material that serves only a stock tutorial structure.

Run the bundled syntax and citation checker from this skill directory:

```
python <skill-dir>/scripts/check-tutorial <draft-path> --tree <kernel-tree>
```

A Lua filter (`secnum.lua`) turns `.secref` into live "§9.5" text. That filter belongs to the document's pandoc build, not the kernel tree. If this document is not built with `--lua-filter=secnum.lua`, tell the user rather than leaving links unresolved.

## Source listings

Show a listing only when the reader needs the exact shape (subtle control flow, non-obvious ordering, a trick that only makes sense next to the bytes). Skip listings the prose already covers.

Long or multi-purpose functions: break into the smallest logical pieces (a few lines each) and explain each piece before the next. A wall of code with one explanation below forces the reader to hold the whole function in their head.

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

Do not re-link the same definition in the same subsection because the paragraph revolves around it. One link at first mention is the density; more turns the prose into a carpet of URLs. Different definitions with the same spelling each need their own link.

### Line numbers

- Symbol links have `#L<number>`. A bare URL is fine when the link deliberately refers to a whole file, such as an in-tree document or a file in “Further reading”.
- `#L` is the definition line (signature, `struct`/`typedef`, `#define`). Confirm against the file on disk, not memory.
- The same spelling can name separate definitions. Link each occurrence to the definition under discussion.
- Nearby names (`foo` vs `foo_bar`): confirm the line is the one being discussed.

`scripts/check-tutorial` errors on mixed versions, missing `#L` on symbol links, `#L` that does not contain the symbol, the same definition elixir-linked twice in one `##`/`###` subsection, and an in-tree path mentioned but not linked. First-mention-is-linked (rather than omitted) is Pass 1: the checker cannot know every identifier.

## Style

Write as a colleague sitting next to the reader at a terminal, not as a model producing a tutorial. The existing bans (possessive `'s`, defensive filler, numbered headings) still apply; they are not a license to sound like a bullet list expanded into sentences.

- Assume C. Do not explain C syntax.
- Never possessive `'s` ("the task's state"). "Of the" / compound nouns ("the state of the task", "task state") force the noun relationship into the open.
- Concrete, not vague ("walks the sorted table and stops at the first entry belonging to a different key", not "does some bookkeeping").
- No defensive filler: arguing a section is worth reading; "not X" after already stating X; hedges ("it is worth noting", "importantly", "as one might expect"). Optional-config context is one direct sentence, not an argument.
- Direct colleague prose. Bad: "this is where a reader carrying the rules forward would go wrong". Good: "Compare this with the `=y` version, which clamps negative values."
- **Natural, not generated.** Do not announce structure ("This section will…", "There are three parts."). Do not open consecutive paragraphs with the same mold ("The X is… The Y is…"). Vary sentence length: a longer why, then a short fact.
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
