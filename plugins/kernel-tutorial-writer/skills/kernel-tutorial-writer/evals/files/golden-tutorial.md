# Fake keys

A counted on/off switch in this fixture tree. The first enable may patch text; nested enables only move the counter. Written against v6.16 of this tree.

## Overview {#overview}

The mechanism is a counter plus an updater. [fake_key_enable()](https://elixir.bootlin.com/linux/v6.16/source/kernel/fake_key.c#L11) and [fake_key_disable()](https://elixir.bootlin.com/linux/v6.16/source/kernel/fake_key.c#L19) change the count; [fake_key_update()](https://elixir.bootlin.com/linux/v6.16/source/kernel/fake_key.c#L27) is what would patch sites once [fake_key_init()](https://elixir.bootlin.com/linux/v6.16/source/kernel/fake_key.c#L6) has marked the table ready.

---

## Data structures {#data-structures}

The only type is [`struct fake_key`](https://elixir.bootlin.com/linux/v6.16/source/include/linux/fake_key.h#L6), which holds an `enabled` counter.

---

## Enabling a key {#enabling-a-key}

Turning a key on is a counted transition. Here is what [fake_key_enable()](https://elixir.bootlin.com/linux/v6.16/source/kernel/fake_key.c#L11) does, one step at a time.

**1. Bump the counter.**

```c
int count = atomic_inc_return(&key->enabled);
```

The increment is the commit point.

**2. Patch on the 0 → 1 edge, and only if init already ran.**

```c
if (count == 1 && fake_key_ready)
    fake_key_update(key, true);
```

Concretely: [early_boot_setup()](https://elixir.bootlin.com/linux/v6.16/source/init/main.c#L6) calls [fake_key_enable()](https://elixir.bootlin.com/linux/v6.16/source/kernel/fake_key.c#L11) during boot. If that call happens before [fake_key_init()](https://elixir.bootlin.com/linux/v6.16/source/kernel/fake_key.c#L6), `fake_key_ready` is still false and the updater is skipped.

The disable path in [](#disabling-a-key){.secref} is the 1 → 0 mirror.

---

## Disabling a key {#disabling-a-key}

[fake_key_disable()](https://elixir.bootlin.com/linux/v6.16/source/kernel/fake_key.c#L19) decrements, then calls [fake_key_update()](https://elixir.bootlin.com/linux/v6.16/source/kernel/fake_key.c#L27) only when the count hits zero and the table is ready.

---

## Further reading in-tree {#further-reading-in-tree}

- [fake_key_enabled()](https://elixir.bootlin.com/linux/v6.16/source/include/linux/fake_key.h#L10) — the read-side helper
- `Documentation/core-api/fake_key.rst` — the in-tree note
