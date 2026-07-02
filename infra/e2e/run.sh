#!/usr/bin/env bash
# Scripted e2e for the Validate layer-2 stand (docs/design-task-pipeline.md). Read-only checks
# against the deployed stand: fail on the first broken check, log artefacts to stdout, no LLM.
# The dispatcher captures the exit code and log tail. URLs come from the environment (set by the
# stand config); the defaults match infra/.env.stand so the suite is also runnable by hand once
# the stand is up: `bash infra/e2e/run.sh`.
set -uo pipefail

BACKEND="${STAND_BACKEND_URL:-http://127.0.0.1:8010}"
FRONTEND="${STAND_FRONTEND_URL:-http://127.0.0.1:4331}"
fail=0

check() {  # name  url  extended-regex-the-body-must-match (empty = any 2xx body)
  local name="$1" url="$2" pat="$3" body
  echo "--- e2e: ${name} (${url})"
  if ! body="$(curl -fsS --max-time 20 "${url}")"; then
    echo "FAIL: ${name} — request failed"; fail=1; return
  fi
  if [ -n "${pat}" ] && ! grep -qE "${pat}" <<<"${body}"; then
    echo "FAIL: ${name} — response did not match /${pat}/"
    echo "  head: $(head -c 200 <<<"${body}")"
    fail=1; return
  fi
  echo "OK: ${name}"
}

check "backend health"     "${BACKEND}/api/health"              '"status":"ok"'
check "backend profile"    "${BACKEND}/api/v1/profile/projects" '^\['
check "frontend home (en)" "${FRONTEND}/en/"                    '<html'

if [ "${fail}" -ne 0 ]; then
  echo "e2e: FAILED"
  exit 1
fi
echo "e2e: all checks passed"
