#!/usr/bin/env bash
# Tests for submodule-scope.py. The important one is case 3: a real repository cloned the way CI clones it,
# which is exactly how Jade came to measure 7 inventory rows instead of 93.
set -u
T="$(mktemp -d "${TMPDIR:-/tmp}/sms-test-XXXXXX")"
TOOL="$(cd "$(dirname "$0")" && pwd)/submodule-scope.py"
pass=0; fail=0
trap 'rm -rf "$T"' EXIT

check() { # check <name> <expected-exit> <must-contain> <command...>
  local name=$1 want=$2 needle=$3; shift 3
  local out; out="$("$@" 2>&1)"; local got=$?
  if [ "$got" = "$want" ] && { [ -z "$needle" ] || printf '%s' "$out" | grep -q -- "$needle"; }; then
    printf '  ok    %s\n' "$name"; pass=$((pass+1))
  else
    printf '  FAIL  %s  (exit %s, wanted %s)\n' "$name" "$got" "$want"
    printf '%s\n' "$out" | sed 's/^/          /'; fail=$((fail+1))
  fi
}

# 1. No .gitmodules at all.
mkdir -p "$T/plain" && : > "$T/plain/file.txt"
check "no .gitmodules exits 0" 0 "nothing to check" python3 -I "$TOOL" --repo "$T/plain"

# 2. A declared submodule whose directory is empty: the shallow-clone defect, synthetic.
mkdir -p "$T/synthetic/vendor/dep"
cat > "$T/synthetic/.gitmodules" <<'EOF'
[submodule "dep"]
	path = vendor/dep
	url = https://example.invalid/dep.git
EOF
check "empty submodule exits 1" 1 "EMPTY    vendor/dep" python3 -I "$TOOL" --repo "$T/synthetic"
check "empty submodule says how to fix" 1 "recurse-submodules" python3 -I "$TOOL" --repo "$T/synthetic"
check "out of scope is not a failure" 0 "outside the declared scope" \
  python3 -I "$TOOL" --repo "$T/synthetic" --scope src include
check "excluded by request is not a failure" 0 "excluded by request" \
  python3 -I "$TOOL" --repo "$T/synthetic" --exclude vendor/dep

# 3. The real thing: embit pins secp256k1-zkp. Cloned the way CI clones, the submodule is empty.
if git clone --quiet --depth 1 https://github.com/diybitcoinhardware/embit "$T/embit-shallow" 2>/dev/null; then
  check "REAL: embit cloned without submodules is caught" 1 "EMPTY    secp256k1/secp256k1-zkp" \
    python3 -I "$TOOL" --repo "$T/embit-shallow"
  if git -C "$T/embit-shallow" submodule update --quiet --init --recursive --depth 1 2>/dev/null; then
    check "REAL: embit with submodules materialised passes" 0 "nothing wrong" \
      python3 -I "$TOOL" --repo "$T/embit-shallow"
    # 4. --against: a tool that read only the top level must be reported as not having read the submodule.
    (cd "$T/embit-shallow" && find . -name '*.py' -not -path './secp256k1/*' | sed 's|^\./||' > "$T/toplevel.txt")
    check "--against catches an unread submodule" 1 "UNREAD   secp256k1/secp256k1-zkp" \
      python3 -I "$TOOL" --repo "$T/embit-shallow" --against "$T/toplevel.txt"
    (cd "$T/embit-shallow" && find . -type f | sed 's|^\./||' > "$T/everything.txt")
    check "--against passes when everything was read" 0 "populated and read" \
      python3 -I "$TOOL" --repo "$T/embit-shallow" --against "$T/everything.txt"
  else
    printf '  skip  REAL: submodule update failed (network?)\n'
  fi
else
  printf '  skip  REAL: clone failed (network?)\n'
fi

# 5. SARIF input, which is how most scanners report.
cat > "$T/synthetic2.sarif" <<'EOF'
{"version":"2.1.0","runs":[{"artifacts":[{"location":{"uri":"src/main.c"}}],
 "results":[{"locations":[{"physicalLocation":{"artifactLocation":{"uri":"src/other.c"}}}]}]}]}
EOF
mkdir -p "$T/sarif/vendor/dep" && : > "$T/sarif/vendor/dep/code.c"
cp "$T/synthetic/.gitmodules" "$T/sarif/.gitmodules"
check "SARIF input parsed, submodule unread" 1 "UNREAD   vendor/dep" \
  python3 -I "$TOOL" --repo "$T/sarif" --against "$T/synthetic2.sarif"

# 6. JSON output stays machine-readable and carries the verdict.
check "--json reports ok:false" 1 '"ok": false' python3 -I "$TOOL" --repo "$T/synthetic" --json

printf '\n%d passed, %d failed\n' "$pass" "$fail"
[ "$fail" -eq 0 ]
