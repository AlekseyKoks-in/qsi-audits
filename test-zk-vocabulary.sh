#!/usr/bin/env bash
# Tests for zk-vocabulary.py. Cases 4 and 5 are the ones that matter: a real protocol implementation, and the
# real output of a scanner that had no word for any of it.
set -u
T="$(mktemp -d "${TMPDIR:-/tmp}/zkv-test-XXXXXX")"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOL="$HERE/zk-vocabulary.py"
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

# 1. The patterns, tested against the real lines they were written from.
check "self-test passes" 0 "all pass" python3 -I "$TOOL" --self-test

# 2. A tree with no zero-knowledge cryptography says so, and does not invent anything.
mkdir -p "$T/plain" && printf 'fn main() { let x = 1; }\n' > "$T/plain/main.rs"
check "clean tree exits 0" 0 "No zero-knowledge" python3 -I "$TOOL" --repo "$T/plain"

# 3. Synthetic, one line per primitive, to check the classification is attached to the right one.
mkdir -p "$T/syn"
cat > "$T/syn/lib.rs" <<'EOF'
use sinsemilla::CommitDomain;
use reddsa::orchard::SpendAuth;
use halo2_proofs::plonk::Circuit;
use halo2_poseidon::primitives::P128Pow5T3;
let cv = ValueCommitment::derive(value, rcv);
EOF
check "finds Sinsemilla and calls it binding" 0 "Sinsemilla  \[SHOR\]  breaks: binding" python3 -I "$TOOL" --repo "$T/syn"
check "finds Halo 2 and calls it soundness" 0 "Halo 2 (IPA)  \[SHOR\]  breaks: soundness" python3 -I "$TOOL" --repo "$T/syn"
check "Poseidon is NOT Shor-breakable" 0 "Poseidon  \[grover_reduced\]" python3 -I "$TOOL" --repo "$T/syn"
# The underscore case that was broken for one commit: halo2_poseidon must be found.
check "halo2_poseidon is found" 0 "Poseidon" python3 -I "$TOOL" --repo "$T/syn"

# 4. REAL: the Orchard protocol. Five primitives, none of which a generic scanner's vocabulary contains.
if git clone --quiet --depth 1 https://github.com/zcash/orchard "$T/orchard" 2>/dev/null; then
  check "REAL: orchard has Sinsemilla" 0 "Sinsemilla" python3 -I "$TOOL" --repo "$T/orchard"
  check "REAL: orchard has RedDSA" 0 "RedDSA" python3 -I "$TOOL" --repo "$T/orchard"
  check "REAL: orchard has Halo 2" 0 "Halo 2 (IPA)" python3 -I "$TOOL" --repo "$T/orchard"

  # 5. The failure this tool exists for: a scanner whose entire answer for this tree was "AES-256".
  printf '["AES-256"]\n' > "$T/blind.json"
  check "REAL: a blind scanner is caught" 1 "NOT reported by your tool" \
    python3 -I "$TOOL" --repo "$T/orchard" --against "$T/blind.json"
  printf '["AES-256","Sinsemilla","RedDSA","Halo 2 (IPA)","Pedersen commitment","Poseidon"]\n' > "$T/seeing.json"
  check "REAL: a scanner that sees them passes" 0 "also appears in what your tool reported" \
    python3 -I "$TOOL" --repo "$T/orchard" --against "$T/seeing.json"
else
  printf '  skip  REAL: clone failed (network?)\n'
fi

# 6. REAL: a library that implements a primitive without naming it in code. reddsa says RedDSA 27 times in doc
#    comments and never in code, so only the declaration-shaped patterns reach it.
if git clone --quiet --depth 1 https://github.com/ZcashFoundation/reddsa "$T/reddsa" 2>/dev/null; then
  check "REAL: reddsa's implementation is found" 0 "RedDSA" python3 -I "$TOOL" --repo "$T/reddsa"
else
  printf '  skip  REAL: reddsa clone failed (network?)\n'
fi

# 7. SARIF in, and machine-readable out.
cat > "$T/results.sarif" <<'EOF'
{"version":"2.1.0","runs":[{"results":[{"ruleId":"CODE-QV-ASYMMETRIC","message":{"text":"AES-256"}}]}]}
EOF
check "SARIF parsed as what the tool reported" 1 "NOT reported" \
  python3 -I "$TOOL" --repo "$T/syn" --against "$T/results.sarif"
check "--json carries the verdict" 1 '"ok": false' \
  python3 -I "$TOOL" --json --repo "$T/syn" --against "$T/results.sarif"

printf '\n%d passed, %d failed\n' "$pass" "$fail"
[ "$fail" -eq 0 ]
