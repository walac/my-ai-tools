# Platform Support

This repository distributes the same plugin payload to multiple coding agents. `skills/<name>/SKILL.md` is the portable core: keep its YAML `name` and `description` frontmatter tool-neutral, and keep scripts, references, and assets inside the same plugin directory.

| Platform | Catalog or entry point | Adapter |
| --- | --- | --- |
| Cursor | `.cursor-plugin/marketplace.json` | `.cursor-plugin/plugin.json` |
| Codex | `.agents/plugins/marketplace.json` | `.codex-plugin/plugin.json` |
| Claude Code | `.claude-plugin/marketplace.json` | `.claude-plugin/plugin.json` |
| Gemini CLI | Individual plugin directory | `gemini-extension.json` |

Gemini CLI uses independently installed extensions rather than a repository-wide marketplace catalog. Each `plugins/<name>/` directory is an extension and contains its own manifest. Cursor-specific commands remain in `commands/`; portable workflows belong in `skills/`.

Keep the plugin `name`, `version`, and `description` identical across the four adapter manifests and the Cursor/Claude catalogs. Codex marketplace entries do not carry `description`; they still need matching `name` values.

## Catalog `source` shapes

Each marketplace uses a different `source` field. Do not copy one catalog's value into another:

```json
"source": "plugin-name"
```

Cursor: directory name under `pluginRoot` (`plugins/`).

```json
"source": "./plugins/plugin-name"
```

Claude Code: path relative to the repository root.

```json
"source": { "source": "local", "path": "./plugins/plugin-name" }
```

Codex: object with `source` and `path`. A string path is invalid.

## Claude `commands: []` on commit and cover

`plugins/commit` and `plugins/cover` keep Cursor slash commands in `commands/`. Their `.claude-plugin/plugin.json` sets `"commands": []` so Claude Code **replaces** the default `commands/` scan and does not register `/commit` or `/cover`. Claude uses the portable `skills/` payload instead.

Do not delete that key. After changing it, confirm a Claude install of those plugins has no `/commit` or `/cover` slash command. Claude's `skills` field is additive; never set `"skills": []`.

## MCP config lockstep (`lkml-mcp`)

`lkml-mcp` ships the same `uvx` server in three places. Keep them identical when changing the command, args, or package source:

- `plugins/lkml-mcp/mcp.json` — Cursor
- `plugins/lkml-mcp/.mcp.json` — Claude Code and Codex (`mcpServers: "./.mcp.json"`)
- `plugins/lkml-mcp/gemini-extension.json` — inline `mcpServers`

## Codex `interface.defaultPrompt`

Use an array of at most three strings, each 128 characters or fewer:

```json
"defaultPrompt": ["Prepare a kernel-style commit for my changes."]
```

`rhel-jira` is a workflow skill, not a bundled Jira client. Configure an organization-approved Jira MCP server that exposes its required `jira_*` tools before enabling it on any platform.

## Local validation

Run these commands from the repository root after changing a manifest or skill:

```bash
for plugin in plugins/*; do
  claude plugin validate "$plugin" --strict
  gemini extensions validate "$plugin"
done
claude plugin validate .claude-plugin/marketplace.json --strict
git diff --check
```

Claude's validator also checks the marketplace when given `.claude-plugin/marketplace.json`. Codex validates its marketplace and plugin manifests when they are added or installed.

## Local installation

```bash
codex plugin marketplace add .
claude plugin marketplace add .
gemini extensions link ./plugins/pal-skills
agent plugin marketplace add .
```

Then install the desired plugin with the platform's plugin UI or CLI. For Gemini, link or install each desired `plugins/<name>` directory. Test external MCP integrations only after reviewing their configuration and having their required runtime installed.
