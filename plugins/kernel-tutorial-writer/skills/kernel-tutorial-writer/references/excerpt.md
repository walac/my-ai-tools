# Style specimen (not a source of truth)

Copy the *shape*, not the claims or line numbers. Look those up in the tree being documented.

The passage below is a mid-document slice: a framing opener, a split listing, a "Concretely:" call site, a sidebar, a footnote, a `.secref`, an in-tree file link, and symbol elixir density (first mention in the subsection only). Elixir URLs use a placeholder version. Line numbers here match `evals/files/mini-kernel/` so they are not random; they are still not a source of truth for a real kernel.

## Prose {#prose}

Write like a colleague, not like an outline expanded into sentences.

Stiff (rewrite this shape):

> This section will now examine the enable path. It is important to note that `fake_key_enable()` is responsible for handling the increment of the counter. Then, it checks whether the count equals one. If so, it patches text.

Human (this genre):

> Turning a key on is a counted transition, not a boolean flip. The first increment is the one that has to patch text; later increments only move the counter.

The human version still uses short paragraphs and names the rule in one breath. It does not announce the section, does not hedge, and does not open three sentences on the same mold.

---

## Enabling a key {#enabling-a-key}

Turning a key on is a counted transition, not a boolean flip. The first increment is the one that has to patch text; later increments only move the counter.

[`fake_key_enable()`](https://elixir.bootlin.com/linux/<version>/source/kernel/fake_key.c#L11) in [`kernel/fake_key.c`](https://elixir.bootlin.com/linux/<version>/source/kernel/fake_key.c) does two jobs in a fixed order. Here is what it actually does, one step at a time.

**1. Bump the counter.**

```c
int count = atomic_inc_return(&key->enabled);
```

The increment is the commit point. Everything after this line is looking at a count that other CPUs can already observe.

**2. Patch on the 0 → 1 edge.**

```c
if (count == 1)
    fake_key_update(key, true);
```

Building that update around the edge, rather than around "the key is on", is what keeps a nested enable from patching twice. The disable path in [](#disabling-a-key){.secref} is the mirror: it patches only on 1 → 0.

Concretely: [`early_boot_setup()`](https://elixir.bootlin.com/linux/<version>/source/init/main.c#L6) calls `fake_key_enable()` before [`fake_key_init()`](https://elixir.bootlin.com/linux/<version>/source/kernel/fake_key.c#L6) has built the site table. If the 0 → 1 edge ran the updater that early, it would walk an empty table and the later init pass would have nothing to patch. The enable function therefore records the count and leaves the text alone until init runs.

> The updater itself is a small state machine over the site table, not part of the enable/disable story.
>
> ```
>   enable 0→1          disable 1→0
>        |                    |
>        v                    v
>    [walk sites] ------> [walk sites]
>        |                    |
>      jmp                  nop
> ```
>
> Skip this if only the counter rule is needed. Nothing later depends on the diagram.

A site is a linker-collected record[^site] of one instruction that has to change when the key flips.

[^site]: A linker section here is just a named slice of the binary that `ld` concatenates from every `.o` that contributed to it — the table is not built in C.

---

## Disabling a key {#disabling-a-key}

Disable is the 1 → 0 mirror of [](#enabling-a-key){.secref}. The rest of the section is omitted in this specimen.
