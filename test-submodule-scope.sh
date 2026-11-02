#!/usr/bin/env bash
# Tests for submodule-scope.py. The important one is case 3: a real repository cloned the way CI clones it,
# which is exactly how Jade came to measure 7 inventory rows instead of 93. Case 8 holds the tool to what git
# itself does with `update = none`, offline, because getting that wrong failed CI on SeedSigner.
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

# 7. `update = none`: the project's own declaration that a submodule is not part of a default checkout. Empty is
#    then the declared state, not a defect — but it must not mask a real empty submodule beside it.
mkdir -p "$T/upd/shots" "$T/upd/vendor/dep"
cat > "$T/upd/.gitmodules" <<'EOF'
[submodule "shots"]
	path = shots
	url = https://example.invalid/shots.git
	update = none
EOF
check "empty update=none submodule is not a failure" 0 "declared update = none" python3 -I "$TOOL" --repo "$T/upd"
check "--json lists it apart from the empty ones" 0 '"not_checked_out_by_default"' \
  python3 -I "$TOOL" --repo "$T/upd" --json
sed -i 's/update = none/update = "none"/' "$T/upd/.gitmodules"
check "a quoted value means the same, as it does to git" 0 "declared update = none" python3 -I "$TOOL" --repo "$T/upd"
cat >> "$T/upd/.gitmodules" <<'EOF'
[submodule "dep"]
	path = vendor/dep
	url = https://example.invalid/dep.git
EOF
check "update=none does not mask a real empty submodule" 1 "EMPTY    vendor/dep" python3 -I "$TOOL" --repo "$T/upd"

# 8. The same against git itself, offline. Build a superproject with one ordinary and one `update = none`
#    submodule, clone it the way CI clones with submodules on, and require that git really left the second one
#    empty (the premise), that the tool accepts it, and that the tool checks it again once someone checks it out.
g() { git -c protocol.file.allow=always -c user.name=test -c user.email=test@example.invalid \
          -c init.defaultBranch=main -c commit.gpgsign=false "$@"; }
if command -v git >/dev/null 2>&1; then
  for r in lib shots; do
    mkdir -p "$T/git/$r" && echo "int $r(void) { return 0; }" > "$T/git/$r/$r.c"
    g -C "$T/git/$r" init -q && g -C "$T/git/$r" add . && g -C "$T/git/$r" commit -qm "$r"
  done
  mkdir -p "$T/git/super" && echo "int main(void) { return 0; }" > "$T/git/super/main.c"
  g -C "$T/git/super" init -q
  g -C "$T/git/super" submodule add -q "$T/git/lib" vendor/lib
  g -C "$T/git/super" submodule add -q "$T/git/shots" shots
  g -C "$T/git/super" config -f .gitmodules submodule.shots.update none
  g -C "$T/git/super" add -A && g -C "$T/git/super" commit -qm super
  g clone -q --recurse-submodules "$T/git/super" "$T/git/clone" 2>/dev/null
  if [ -n "$(ls -A "$T/git/clone/vendor/lib" 2>/dev/null)" ] && [ -d "$T/git/clone/shots" ] \
     && [ -z "$(ls -A "$T/git/clone/shots")" ]; then
    printf '  ok    %s\n' "GIT: --recurse-submodules filled vendor/lib and left shots empty"; pass=$((pass+1))
  else
    printf '  FAIL  %s\n' "GIT: git did not do what the tool assumes"; fail=$((fail+1))
  fi
  check "GIT: the tool accepts what git did" 0 "declared update = none" python3 -I "$TOOL" --repo "$T/git/clone"
  rm -rf "$T/git/clone/vendor/lib" && mkdir "$T/git/clone/vendor/lib"
  check "GIT: and still catches the ordinary one emptied" 1 "EMPTY    vendor/lib" \
    python3 -I "$TOOL" --repo "$T/git/clone"
  g -C "$T/git/clone" submodule update -q --init --checkout -- vendor/lib shots
  (cd "$T/git/clone" && find . -name '*.c' -not -path './shots/*' | sed 's|^\./||' > "$T/git-noshots.txt")
  check "GIT: once checked out, an unread update=none submodule is UNREAD" 1 "UNREAD   shots" \
    python3 -I "$TOOL" --repo "$T/git/clone" --against "$T/git-noshots.txt"
else
  printf '  skip  GIT: git is not installed\n'
fi

printf '\n%d passed, %d failed\n' "$pass" "$fail"
[ "$fail" -eq 0 ]
