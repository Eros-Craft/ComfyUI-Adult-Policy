#!/usr/bin/env bash
# The Desktop check (T1 Desktop) for this repository, on the Mac. Free: nothing renders, nothing is downloaded,
# nothing in the Desktop install it borrows changes.
#
#     bash .github/testing/desktop-check.sh                         # the ErosCraft dev install, a scratch server
#     bash .github/testing/desktop-check.sh --server http://127.0.0.1:8000   # a running Desktop that has the pack
#
# What it runs, in order, and never stops early (one run, one list):
#   1. policy/test_policy.py with the install's own Python (the Python Desktop runs, not the system's)
#   2. `comfy node validate`, the Registry's own checks, when comfy-cli is on PATH
#   3. the node.zip the Registry would ship (`comfy node pack`, or the smoke's own equivalent)
#   4. .github/testing/comfyui_smoke.py: a scratch server from that install's ComfyUI, started the way Desktop starts
#      a git install (`python -s main.py`, Desktop's two feature flags, --cpu, loopback, its own --base-directory),
#      the zip installed in it, and every node, script and gate position checked through the real /prompt
#
# The install it borrows (read, never written):
#   COMFYUI_DIR     default ~/ComfyUI-Installs/ErosCraft-Dev, the workspace's base/desktop.sh install
#   COMFYUI_PYTHON  default $COMFYUI_DIR/.venv/bin/python
#   SMOKE_PORT      default 8296, clear of the dev server (8297, 8299), the shared testbed (8199) and Desktop (8000)
# The report lands in .github/testing/reports/ (ignored by git); its Markdown is what a pull request quotes.
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
COMFYUI_DIR="${COMFYUI_DIR:-$HOME/ComfyUI-Installs/ErosCraft-Dev}"
COMFYUI_PYTHON="${COMFYUI_PYTHON:-$COMFYUI_DIR/.venv/bin/python}"
SMOKE_PORT="${SMOKE_PORT:-8296}"
SERVER=""
if [ "${1:-}" = "--server" ]; then SERVER="${2:?--server needs a URL}"; fi
export DO_NOT_TRACK=1 COMFY_NO_TELEMETRY=1

OUT="$HERE/reports"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$OUT"
FAILED=()
step(){ printf '\n== %s\n' "$*"; }

PY="$COMFYUI_PYTHON"
if [ ! -x "$PY" ]; then
  if [ -z "$SERVER" ]; then
    echo "No Python at $PY. Build the dev install first (the workspace's bash base/desktop.sh --server)," >&2
    echo "or set COMFYUI_DIR and COMFYUI_PYTHON to another ComfyUI with its venv." >&2
    exit 2
  fi
  PY="$(command -v python3)"
fi

step "1. policy/test_policy.py with $PY"
PYTHONWARNINGS=error "$PY" "$REPO/policy/test_policy.py" || FAILED+=("policy tests")

step "2. the Registry's own checks"
if command -v comfy >/dev/null 2>&1; then
  (cd "$REPO" && comfy node validate) || FAILED+=("comfy node validate")
else
  echo "comfy-cli is not on PATH, so this step was skipped (uv tool install comfy-cli)"
fi

ZIP_ARGS=()
if [ -z "$SERVER" ] && command -v comfy >/dev/null 2>&1; then
  step "3. the node.zip the Registry would ship"
  ZIP="$(mktemp -d)/node.zip"
  if (cd "$REPO" && comfy node pack >/dev/null && mv node.zip "$ZIP"); then ZIP_ARGS=(--zip "$ZIP")
  else echo "comfy node pack failed; the smoke builds the same zip itself"; fi
fi

step "4. the pack in ComfyUI, through /prompt"
if [ -n "$SERVER" ]; then
  python3 "$HERE/comfyui_smoke.py" --server "$SERVER" --venue desktop \
    --json "$OUT/desktop-$STAMP.json" > "$OUT/desktop-$STAMP.md" || FAILED+=("ComfyUI smoke")
else
  [ -d "$COMFYUI_DIR/comfy" ] || { echo "$COMFYUI_DIR is not a ComfyUI source folder" >&2; exit 2; }
  python3 "$HERE/comfyui_smoke.py" --comfyui "$COMFYUI_DIR" --python "$COMFYUI_PYTHON" --port "$SMOKE_PORT" \
    --desktop-flags --venue desktop "${ZIP_ARGS[@]}" --json "$OUT/desktop-$STAMP.json" \
    --log "$OUT/desktop-$STAMP.log" > "$OUT/desktop-$STAMP.md" || FAILED+=("ComfyUI smoke")
fi
cat "$OUT/desktop-$STAMP.md"

printf '\n== Desktop check: '
if [ ${#FAILED[@]} -eq 0 ]; then
  echo "every step green. Report: $OUT/desktop-$STAMP.json"
  echo "Still by eye, once per release (TESTING.md, \"By eye in Desktop\"): the node names and the picker button."
  exit 0
fi
echo "failed: ${FAILED[*]}. Report: $OUT/desktop-$STAMP.json"
exit 1
