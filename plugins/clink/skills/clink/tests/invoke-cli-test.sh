#!/usr/bin/env bash
# Verify provider-specific command construction by observing a fake CLI.

set -euo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
fixture_dir=$(mktemp -d)
trap 'rm -rf -- "$fixture_dir"' EXIT

mkdir -p "$fixture_dir/bin"

cat > "$fixture_dir/bin/agent" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$@" > "$CLINK_CAPTURE"
EOF
chmod +x "$fixture_dir/bin/agent"

capture="$fixture_dir/capture"
expected="$fixture_dir/expected"
printf '%s\n' -p 'Review the current branch.' --mode=ask --trust --model gpt-5 > "$expected"

printf '%s' 'Review the current branch.' \
  | PATH="$fixture_dir/bin:/usr/bin:/bin" CLINK_CAPTURE="$capture" \
    "$script_dir/scripts/invoke-cli.sh" cursor --model gpt-5

cmp -- "$expected" "$capture"
