#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [[ -f .env ]]; then
  set -o allexport
  # shellcheck disable=SC1091
  source .env
  set +o allexport
fi

usage() {
  cat <<USAGE
Usage: $(basename "$0") <command> [options]

Commands:
  build           Run the static site build once.
  start           Build the site and start the proxy stack in detached mode.
  stop            Stop all running services.
  restart         Restart the stack (stop, then start).
  logs [service]  Tail logs from the whole stack or a specific service.
  ps              Show service status.
  clean           Stop the stack and remove volumes (including the build cache).
  help            Show this help message.
USAGE
}

compose() {
  if [[ -n "${DOCKER_CONTEXT:-}" ]]; then
    docker --context "$DOCKER_CONTEXT" compose "$@"
  else
    docker compose "$@"
  fi
}

command="${1:-help}"
shift $(( $# > 0 ? 1 : 0 ))

case "$command" in
  build)
    compose run --rm builder
    ;;
  start)
    compose run --rm builder
    compose up -d
    ;;
  stop)
    compose down
    ;;
  restart)
    "$0" stop
    "$0" start
    ;;
  logs)
    compose logs -f "$@"
    ;;
  ps)
    compose ps "$@"
    ;;
  clean)
    compose down -v
    ;;
  help|--help|-h)
    usage
    ;;
  *)
    echo "Unknown command: $command" >&2
    usage >&2
    exit 1
    ;;
esac
