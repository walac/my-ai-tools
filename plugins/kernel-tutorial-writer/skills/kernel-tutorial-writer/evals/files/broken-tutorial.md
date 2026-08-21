# Fake keys (broken on purpose)

This file is an eval fixture. It violates the tutorial skill on purpose.

## 1 Introduction

Looking at the struct, a fake key is a counted switch.

The [fake_key_enable()](https://elixir.bootlin.com/linux/v6.16/source/kernel/fake_key.c) function turns the key's state on. See section 2.

## Enabling {#enabling}

[fake_key_enable()](https://elixir.bootlin.com/linux/v6.15/source/kernel/fake_key.c#L1) bumps a counter. Nested enables are covered in [](#does-not-exist){.secref}.

## Disabling {#disabling}

[fake_key_enable()](https://elixir.bootlin.com/linux/v6.16/source/kernel/fake_key.c#L19) is also used here by mistake. [fake_key_disable()](https://elixir.bootlin.com/linux/v6.16/source/kernel/fake_key.c#L19) is the real disable.
