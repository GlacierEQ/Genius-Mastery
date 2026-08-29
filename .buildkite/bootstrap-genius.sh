#!/usr/bin/env bash
set -Eeuo pipefail

ORG="${1:-}"
CLUSTER_NAME="${2:-}"
TRIGGER_BUILDS="${TRIGGER_BUILDS:-1}"

if [[ -z "$ORG" ]]; then
  echo "usage: $0 <buildkite-org-slug> [cluster-name]" >&2
  exit 64
fi

if ! command -v bk >/dev/null 2>&1; then
  echo "ERROR: Buildkite CLI 'bk' is not installed." >&2
  echo "Install it from https://buildkite.com/docs/platform/cli/installation" >&2
  exit 127
fi

if ! bk auth status >/dev/null 2>&1; then
  echo "ERROR: Buildkite CLI is not authenticated." >&2
  echo "Run: bk auth login --org $ORG" >&2
  exit 77
fi

bk auth switch "$ORG" >/dev/null

UPLOAD_CONFIG='steps:
  - label: ":pipeline: Upload repository pipeline"
    command: "buildkite-agent pipeline upload"'

repos=(
  "Genius-Mastery"
  "Genius-Code"
  "Genius-Verification"
)

create_pipeline() {
  local name="$1"
  local repo_url="https://github.com/GlacierEQ/${name}.git"
  local slug
  slug="$(printf '%s' "$name" | tr '[:upper:]' '[:lower:]')"

  echo "==> Reconciling $ORG/$slug"

  if ! bk pipeline view "$ORG/$slug" --json >/dev/null 2>&1; then
    args=(
      pipeline create "$name"
      --org "$ORG"
      --description "GlacierEQ Genius family CI for $name"
      --repository "$repo_url"
      --create-webhook
    )
    if [[ -n "$CLUSTER_NAME" ]]; then
      args+=(--cluster-name "$CLUSTER_NAME")
    fi
    bk "${args[@]}"
  fi

  payload="$(python3 - "$repo_url" "$UPLOAD_CONFIG" <<'PY'
import json
import sys
repo_url = sys.argv[1]
configuration = sys.argv[2]
print(json.dumps({
    "repository": repo_url,
    "default_branch": "main",
    "configuration": configuration,
    "provider_settings": {
        "publish_commit_status": True,
        "publish_commit_status_per_step": True,
        "build_pull_requests": True,
        "build_pull_request_forks": False,
        "build_tags": False,
    },
}))
PY
)"

  bk api --method PATCH "/pipelines/$slug" --data "$payload" >/dev/null

  if ! bk api --method POST "/pipelines/$slug/webhook" >/dev/null 2>&1; then
    echo "    webhook: already present or provider does not permit auto-creation"
  else
    echo "    webhook: created"
  fi

  bk pipeline view "$ORG/$slug" --json >/dev/null
  echo "    pipeline: reconciled"

  if [[ "$TRIGGER_BUILDS" == "1" ]]; then
    bk build create       --pipeline "$ORG/$slug"       --branch main       --commit HEAD       --message "Genius Buildkite bootstrap verification"
    echo "    build: triggered"
  fi
}

for repo in "${repos[@]}"; do
  create_pipeline "$repo"
done

echo
echo "Buildkite Genius family bootstrap complete."
echo "Inspect builds with:"
for repo in "${repos[@]}"; do
  slug="$(printf '%s' "$repo" | tr '[:upper:]' '[:lower:]')"
  echo "  bk build view --pipeline $ORG/$slug --summary"
done
