# wander-plugins

Cursor marketplace for skills, commands, plugins, rules, agents, hooks, and MCP servers.

Hosted at [https://github.com/walac/cursor-marketplace](https://github.com/walac/cursor-marketplace).

Add the marketplace first, then install plugins by name. User-scope installs in Cursor sync to Cursor CLI for the same account.

## Install the marketplace

### Cursor

1. Open **Customize** in the sidebar.
2. Open the source dropdown and choose **Add Marketplace**.
3. Choose **Import from Github**.
4. Paste `https://github.com/walac/cursor-marketplace`.
5. Review the plugins Cursor parsed from `.cursor-plugin/marketplace.json` and save.

To remove it later, open **Customize** → **Browse**, find this marketplace, then use **…** on the section header → **Remove**.

Teams and Enterprise admins can instead import the same URL from [Dashboard → Plugins](https://cursor.com/dashboard) under **Team Marketplaces**. Teammates then see the plugins in **Customize** without adding the GitHub URL themselves.

### Cursor CLI

The Cursor CLI binary is `agent`.

```bash
agent plugin marketplace add https://github.com/walac/cursor-marketplace
```

Pin a branch, tag, or commit with `--git-ref` if you do not want the default branch:

```bash
agent plugin marketplace add https://github.com/walac/cursor-marketplace --git-ref main
```

From an interactive `agent` session you can also run:

```text
/plugin marketplace add https://github.com/walac/cursor-marketplace
```

Confirm it is registered:

```bash
agent plugin marketplace list
```

Re-index after the repo changes, or remove it:

```bash
agent plugin marketplace update wander-plugins
agent plugin marketplace remove wander-plugins
```

`wander-plugins` is the marketplace `name` in `.cursor-plugin/marketplace.json`. `update` and `remove` also accept the GitHub URL.

## Install plugins

Plugin names come from this marketplace, not from the GitHub URL: `lkml-mcp`, `commit`, `cover`, `rhel-jira`, `pal-skills`, `kernel-tutorial-writer`.

### Cursor

1. Open **Customize** in the sidebar.
2. Find the plugin (search, or look under this marketplace).
3. Select **Install** and choose **user** or **project** scope.

### Cursor CLI

Start an interactive session and install from the plugin UI. There is no non-interactive `agent plugin install` command.

```bash
agent
```

Then:

1. Type `/plugin`.
2. Open the **Marketplace** tab.
3. Select the plugin and press Enter.
4. Choose **user** or **project** scope.

You can also paste `https://github.com/walac/cursor-marketplace` into plugin search to install from the repo directly.

## Plugins

| Plugin | Version | Kind | Notes |
|--------|---------|------|--------|
| `lkml-mcp` | 0.1.0 | MCP | Requires `uvx`. lore.kernel.org threads and patches |
| `commit` | 1.1.4 | Command | `/commit` — kernel-style messages, DCO |
| `cover` | 1.1.4 | Command | `/cover` — series cover letters; uses LKML MCP when present |
| `rhel-jira` | 1.0.0 | Skill | Needs wtmcp Jira tools |
| `pal-skills` | 1.0.0 | Skills | analyze, codereview, debug, and related |
| `kernel-tutorial-writer` | 1.0.0 | Skill | Kernel subsystem tutorials from the tree on disk |

## Layout

```
.
├── .cursor-plugin/
│   └── marketplace.json    # Marketplace registry
├── plugins/                # One directory per plugin
└── README.md
```

Each plugin lives under `plugins/<plugin-name>/` and uses the Cursor plugin format:

```
plugins/<plugin-name>/
├── .cursor-plugin/
│   └── plugin.json         # Required plugin manifest
├── skills/                 # Skill folders, each with SKILL.md
├── commands/               # Slash commands (.md)
├── agents/                 # Custom agents (.md)
├── rules/                  # Cursor rules (.mdc)
├── hooks/
│   └── hooks.json
├── mcp.json                # MCP servers
└── README.md
```

Component folders are optional. Cursor discovers them automatically when they exist.

## Add a plugin

1. Create `plugins/<plugin-name>/.cursor-plugin/plugin.json`:

```json
{
  "name": "plugin-name",
  "version": "0.1.0",
  "description": "What this plugin does",
  "author": {
    "name": "Wander Lairson Costa",
    "email": "wander@redhat.com"
  }
}
```

2. Add skills, commands, agents, rules, hooks, or `mcp.json` as needed.

3. Register the plugin in `.cursor-plugin/marketplace.json`. With `pluginRoot` set to `plugins`, `source` is the directory name only (no `./` prefix):

```json
{
  "name": "plugin-name",
  "source": "plugin-name",
  "version": "0.1.0",
  "description": "What this plugin does"
}
```

Keep `name` lowercase kebab-case and unique in this marketplace.

## Docs

- [Cursor plugins](https://cursor.com/docs/plugins)
- [Plugins reference](https://cursor.com/docs/reference/plugins)
- [Cursor CLI](https://cursor.com/docs/cli/overview)
