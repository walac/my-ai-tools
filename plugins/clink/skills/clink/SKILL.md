---
name: clink
description: "Use when the user asks for a second opinion from another AI model, wants to delegate a task to Gemini or Codex, or says ask gemini, ask codex, get gemini's take, run this through gemini, use another model, what does gemini think. Also use when the user needs web search integrated with code analysis."
---

# External CLI Agent Bridge

Delegate a task to an external AI CLI (Gemini, Claude, Codex) and return its
response. This is useful when a second model's perspective adds value, when
the user explicitly asks for another model, or when Gemini's web search
capability is needed.

## Quick Reference

| CLI | Best For | Installed? |
|-----|----------|------------|
| gemini | Web search, alternative perspective, long-context | Run `command -v gemini` to check |
| claude | Code generation, careful reasoning | Run `command -v claude` to check |
| codex | Fast code review, web-aware analysis | Run `command -v codex` to check |

Default to **gemini** unless the user specifies otherwise.

## How to Invoke

First, locate this skill's script directory. The script is at `scripts/invoke-cli.sh` relative to this SKILL.md file. When running locally, you can invoke it directly from the skill's directory:

```bash
# scripts/invoke-cli.sh is next to this SKILL.md (skills/clink/scripts/invoke-cli.sh).
# Resolve that path from the plugin checkout, then:
echo "Your prompt here" | /path/to/skills/clink/scripts/invoke-cli.sh gemini
```

The script reads the full prompt from stdin and passes it to the
selected CLI via its `-p` flag. All output goes to stdout.

## Roles

Select a role by prepending its system prompt to the user's request.
The role shapes how the external CLI approaches the task.

### default

Prepend this to the prompt:

> You are an external CLI agent with full repository access. Use terminal
> tools to inspect files and gather context before responding. Provide concise,
> actionable responses in Markdown. Keep output tight — prefer summaries and
> short bullet lists. Surface assumptions and missing inputs. Always conclude
> with `<SUMMARY>...</SUMMARY>` containing a terse (500 words max) recap of
> key findings and next steps.

### codereviewer

Prepend this to the prompt:

> You are an external CLI code reviewer with full repository access. Inspect
> relevant files directly — run linters or tests as needed. Report findings
> in severity order (Critical, High, Medium, Low) across security, correctness,
> performance, and maintainability. For each issue cite file:line plus a short
> excerpt, describe impact, and recommend a concrete fix. Recognize positive
> practices worth keeping. Conclude with `<SUMMARY>...</SUMMARY>` highlighting
> top risks, recommended fixes, and key positives in 500 words max.

### planner

Prepend this to the prompt:

> You are a planning agent. Inspect relevant files, scripts, or docs before
> outlining the plan. Break work into numbered phases with dependencies,
> validation gates, alternatives, and explicit next actions. Highlight risks
> with mitigations. Keep each step concise. Produce a compact plan summary
> (500 words max) capturing phases, risks, and immediate next actions.

## Prompt Assembly

Build the full prompt in this order:

1. Role system prompt (from the section above)
2. A separator: `---`
3. The user's actual request
4. Any relevant file contents or diffs — the external CLI receives everything
   in the prompt, it cannot read your conversation context

Example:

```bash
{
  cat <<'ROLE'
You are an external CLI code reviewer with full repository access...
ROLE
  echo "---"
  echo "Review this diff for security issues:"
  git diff HEAD~1
} | /path/to/invoke-cli.sh gemini
```

## Handling the Response

- Extract and present the `<SUMMARY>...</SUMMARY>` block if present
- Always attribute: "**Gemini's assessment:**" or "**Codex's review:**"
- Do not present the external CLI's response as your own analysis
- If the response is very long (>20k chars), present only the summary

## When to Use vs Not

**Use clink when:**
- The user asks for another model's opinion
- Web search results are needed alongside code analysis (gemini)
- A different perspective would catch blind spots in your own analysis

**Do not use when:**
- The user just wants code analysis (use analyze, codereview, debug skills)
- The requested CLI is not installed
- The task is simple enough that a second model adds nothing
