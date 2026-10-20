#!/usr/bin/env bash
# Fresh-user install smoke test: uv tool install into an empty HOME, then help, diff, capture.
# Run: scripts/smoke_install.sh [SRC_DIR]   (default: this repo). Leaves the real ~ untouched.
set -uo pipefail
SRC=$(cd "${1:-$(dirname "$0")/..}" && pwd)
H=$(mktemp -d)
trap 'chmod -R u+w "$H"; rm -rf "$H"' EXIT
run() { env -i HOME="$H" PATH="$H/.local/bin:/usr/bin:/bin:$(dirname "$(command -v uv)")" "$@"; }
step() { echo "== $*"; }
fail() { echo "FAIL: $*"; exit 1; }
F="$SRC/tests/fixtures/web"

step "install"
run uv tool install --from "$SRC" pixel-perfect-cli 2>&1 | tail -3
run sh -c 'command -v pixel-perfect' || fail "pixel-perfect not on PATH"

step "help"
run pixel-perfect --help | head -3 || fail "--help"

step "diff gap (expect exit 1, a gap delta with fix)"
run pixel-perfect diff "$F/base.png" "$F/gap.png" --design-map "$F/base.json" --shot-map "$F/gap.json" > "$H/diff.json"
code=$?
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); g=[x for x in d["deltas"] if x["type"]=="gap" and x["fix"]]; print(json.dumps(g[0]) if g else "no gap delta with fix"); sys.exit(0 if g else 1)' "$H/diff.json" || fail "no gap delta with fix"
[ "$code" = 1 ] || fail "diff exit $code, want 1"

printf '<html><body style="margin:0"><div id="a" style="width:40px;height:40px;background:#e00"></div></body></html>' > "$H/t.html"
step "capture without a browser (expect exit 12, one line)"
out=$(run pixel-perfect capture "$H/t.html" --out "$H/shot.png"); code=$?
echo "$out"
[ "$code" = 12 ] || fail "capture exit $code, want 12"
case "$out" in *"playwright install chromium"*) ;; *) fail "no install hint" ;; esac

step "install chromium"
t0=$(date +%s)
run "$(run uv tool dir)/pixel-perfect-cli/bin/playwright" install chromium 2>&1 | tail -1
echo "chromium install: $(( $(date +%s) - t0 ))s"

step "capture"
run pixel-perfect capture "$H/t.html" --out "$H/shot.png" --map "$H/shot.json" --width 200 --height 100 || fail "capture"
[ -s "$H/shot.png" ] || fail "no screenshot"
echo "SMOKE OK"
