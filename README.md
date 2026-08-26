# my-ai-tools

Multi-platform marketplace for agent skills, commands, plugins, and MCP servers. It supports Cursor, Codex, Claude Code, and Gemini CLI. The portable core is the Agent Skills layout (`skills/<name>/SKILL.md`); each platform has a small native manifest or catalog adapter.

Hosted at [https://github.com/walac/my-ai-tools](https://github.com/walac/my-ai-tools).

Add the marketplace first, then install plugins by name. User-scope installs in Cursor sync to Cursor CLI for the same account.

## Choose a platform

| Platform | Distribution model | Start here |
| --- | --- | --- |
| Cursor | Marketplace | `.cursor-plugin/marketplace.json` |
| Codex | Marketplace | `.agents/plugins/marketplace.json` |
| Claude Code | Marketplace | `.claude-plugin/marketplace.json` |
| Gemini CLI | Individual extensions | `plugins/<name>/gemini-extension.json` |

See [platform support](docs/PLATFORM_SUPPORT.md) for validation and local-install commands. Gemini CLI does not use a repository-wide marketplace manifest; install or link the plugin directory you want.

## Install with Codex

```bash
codex plugin marketplace add walac/my-ai-tools
codex plugin add pal-skills@my-ai-tools
```

Use `codex plugin list` to browse available plugins. The Codex catalog is `.agents/plugins/marketplace.json`.

## Install with Claude Code

```bash
claude plugin marketplace add walac/my-ai-tools
claude plugin install pal-skills@my-ai-tools
```

Claude Code uses `.claude-plugin/marketplace.json`; plugin skills are namespaced by plugin name.

## Install with Gemini CLI

Gemini CLI installs each plugin as an extension. Clone the repository, `cd` into it, then link or install the plugin directory you need:

```bash
git clone https://github.com/walac/my-ai-tools.git
cd my-ai-tools
gemini extensions link ./plugins/pal-skills
```

Use `gemini extensions validate ./plugins/pal-skills` before linking a modified extension.

## Install with Cursor

### Cursor app

1. Open **Customize** in the sidebar.
2. Open the source dropdown and choose **Add Marketplace**.
3. Choose **Import from Github**.
4. Paste `https://github.com/walac/my-ai-tools`.
5. Review the plugins Cursor parsed from `.cursor-plugin/marketplace.json` and save.

To remove it later, open **Customize** → **Browse**, find this marketplace, then use **…** on the section header → **Remove**.

Teams and Enterprise admins can instead import the same URL from [Dashboard → Plugins](https://cursor.com/dashboard) under **Team Marketplaces**. Teammates then see the plugins in **Customize** without adding the GitHub URL themselves.

### Cursor CLI

The Cursor CLI binary is `agent`.

```bash
agent plugin marketplace add https://github.com/walac/my-ai-tools
```

Pin a branch, tag, or commit with `--git-ref` if you do not want the default branch:

```bash
agent plugin marketplace add https://github.com/walac/my-ai-tools --git-ref master
```

From an interactive `agent` session you can also run:

```text
/plugin marketplace add https://github.com/walac/my-ai-tools
```

Confirm it is registered:

```bash
agent plugin marketplace list
```

Re-index after the repo changes, or remove it:

```bash
agent plugin marketplace update my-ai-tools
agent plugin marketplace remove my-ai-tools
```

`my-ai-tools` is the marketplace `name` in `.cursor-plugin/marketplace.json`. `update` and `remove` also accept the GitHub URL.

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

You can also paste `https://github.com/walac/my-ai-tools` into plugin search to install from the repo directly.

## Plugins

| Plugin | Version | Kind | Notes |
|--------|---------|------|--------|
| `lkml-mcp` | 0.1.0 | MCP | Requires `uvx`. lore.kernel.org threads and patches |
| `commit` | 1.1.4 | Command + skill | Cursor `/commit`; other platforms use the skill — kernel-style messages, DCO |
| `cover` | 1.1.4 | Command + skill | Cursor `/cover`; other platforms use the skill — series cover letters; uses LKML MCP when present |
| `rhel-jira` | 1.0.0 | Skill | Requires a configured Jira MCP server exposing `jira_*` tools |
| `pal-skills` | 1.0.0 | Skills | analyze, codereview, debug, and related |
| `kernel-tutorial-writer` | 1.0.0 | Skill | Kernel subsystem tutorials from the tree on disk |

## Layout

```
.
├── .cursor-plugin/
│   └── marketplace.json    # Cursor marketplace
├── .agents/plugins/
│   └── marketplace.json    # Codex marketplace
├── .claude-plugin/
│   └── marketplace.json    # Claude Code marketplace
├── plugins/                # One directory per plugin
└── README.md
```

Each plugin lives under `plugins/<plugin-name>/`. Keep `skills/` as the shared Agent Skills payload; the manifests are platform adapters:

```
plugins/<plugin-name>/
├── .cursor-plugin/plugin.json  # Cursor adapter
├── .codex-plugin/plugin.json   # Codex adapter
├── .claude-plugin/plugin.json  # Claude Code adapter
├── gemini-extension.json       # Gemini CLI adapter
├── skills/                     # Portable skill folders with SKILL.md
├── commands/                   # Cursor slash commands (Claude commit/cover hide these)
├── agents/                     # Platform custom agents
├── rules/                      # Cursor rules (.mdc)
├── hooks/
│   └── hooks.json
├── mcp.json / .mcp.json         # Platform MCP configuration
└── scripts/, references/, assets/ # Skill resources
```

Component folders are optional. Do not make the shared `SKILL.md` depend on a platform-specific tool name or variable; put that behavior in an adapter or describe a portable fallback.

## Add a plugin

1. Create `plugins/<plugin-name>/skills/<skill-name>/SKILL.md` with `name` and `description` YAML frontmatter. Put supporting scripts, references, and assets in that skill directory.

2. Add `.cursor-plugin/plugin.json`, `.codex-plugin/plugin.json`, `.claude-plugin/plugin.json`, and `gemini-extension.json`. Use the same lowercase kebab-case name, semantic version, and description in each.

3. Register the plugin in all three marketplace catalogs. Use the matching `source` shape for each platform — do not copy one catalog into another:

   - Cursor: `"source": "<plugin-name>"` (directory name under `pluginRoot`)
   - Claude Code: `"source": "./plugins/<plugin-name>"`
   - Codex: `"source": { "source": "local", "path": "./plugins/<plugin-name>" }`

   Codex `interface.defaultPrompt` is an array of strings. If the plugin has Cursor-only slash commands that must not load on Claude, set `"commands": []` in `.claude-plugin/plugin.json`. See [platform support](docs/PLATFORM_SUPPORT.md).

4. Validate with `claude plugin validate plugins/<plugin-name> --strict`, `gemini extensions validate plugins/<plugin-name>`, and `git diff --check`. See [platform support](docs/PLATFORM_SUPPORT.md) for the full workflow.

## Docs

- [Cursor plugins](https://cursor.com/docs/plugins)
- [Plugins reference](https://cursor.com/docs/reference/plugins)
- [Cursor CLI](https://cursor.com/docs/cli/overview)
- [Claude Code marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Gemini CLI extensions](https://geminicli.com/docs/extensions/reference/)
