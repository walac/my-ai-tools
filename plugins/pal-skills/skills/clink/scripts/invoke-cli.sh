#!/usr/bin/env bash
# Invoke an external AI CLI with a prompt from stdin.
# Usage: echo "prompt" | invoke-cli.sh <gemini|claude|codex> [extra-args...]
#
# The prompt is read from stdin and passed to the CLI via -p.
# Output goes to stdout. Exit code is preserved.

set -euo pipefail

cli="${1:?Usage: invoke-cli.sh <gemini|claude|codex> [extra-args...]}"
shift

if ! command -v "$cli" &>/dev/null; then
    echo "Error: '$cli' not found in PATH." >&2
    exit 127
fi

prompt=$(cat)

case "$cli" in
    gemini)
        exec gemini -p "$prompt" --yolo "$@"
        ;;
    claude)
        exec claude -p "$prompt" --permission-mode acceptEdits --model sonnet "$@"
        ;;
    codex)
        exec codex "$prompt" --dangerously-bypass-approvals-and-sandbox --enable web_search_request "$@"
        ;;
    *)
        exec "$cli" -p "$prompt" "$@"
        ;;
esac
