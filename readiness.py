#!/usr/bin/env python3
"""Measure this repository's bundles against what BIP-360 and BIP-361 require of wallet code.

    python3 readiness.py              # the self-custody slice, plus a portfolio-wide count
    python3 readiness.py --all        # every audited codebase
    python3 readiness.py --json       # machine-readable

No dependencies, no network. Reads only the signed bundles under audits/, so every number it prints can be
re-derived — and `verify.py` tells you whether those bundles are intact in the first place. Run that first.

Why this exists
---------------
BIP-360, now titled Pay-to-Merkle-Root (P2MR), is P2TR with the key-path spend removed; it defends against long
exposure only and says in terms that post-quantum signatures are not in it and are deferred to a later proposal
that is not yet written. BIP-361, Post Quantum Migration and Legacy Signature Sunset, "follows the implementation
of any post-quantum (PQ) output type" and would, at Phase A, stop non-upgraded wallets receiving at all.

Both therefore turn on wallets being upgraded, and neither says what that means in code. This script answers the
part that is measurable from source: which codebases hold the primitives an upgrade needs.

What it can and cannot establish
--------------------------------
Presence of BIP-340 / Schnorr primitives is NECESSARY BUT NOT SUFFICIENT for producing P2MR outputs, which also
need address encoding, descriptors and PSBT support. A codebase with no Schnorr certainly cannot; one with
Schnorr merely might. A post-quantum primitive being present means it is in the code, not that a signing path
uses it. And a zero does not mean a wallet cannot do something: three of the ten codebases below delegate their
cryptography to another repository, which is itself the point — readiness cannot be read off a single tree.

Every figure belongs to the commit printed beside it.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys
from collections import Counter

SELF_CUSTODY = ["secp256k1", "rust-secp256k1", "rust-bitcoin", "libwally-core", "trezor-firmware",
                "bitbox02-firmware", "jade", "seedsigner", "krux", "bdk", "bdk-wallet"]

# The ten codebases quoted in dated write-ups, kept as a set so that figure stays reproducible as the portfolio
# grows. bdk-wallet was audited on 2026-10-29, after those figures were published.
SLICE_AS_QUOTED = SELF_CUSTODY[:10]

# Codebases whose signing primitives live in another repository, with where they actually live — checked against
# the upstream trees, not assumed. Stated so a zero in the Schnorr column is not misread as "this wallet cannot
# do taproot".
DELEGATES = {
    "bdk": "NOT a wallet: at the audited commit bitcoindevkit/bdk is the chain and indexer layer "
           "(bitcoind_rpc, chain, core, electrum, esplora, file_store, testenv) with no wallet, keys, signer or "
           "descriptor crate at all. The wallet is the separate repository bitcoindevkit/bdk_wallet, audited "
           "here as bdk-wallet",
    "bdk-wallet": "the wallet itself: ECDSA is named in src/wallet/signer.rs, src/keys/mod.rs and the descriptor "
                  "modules, but no Schnorr — BIP-340 arrives through rust-bitcoin and rust-secp256k1 as crates, "
                  "so for BDK the signing primitive is two repositories from the wallet",
    "seedsigner": "signing path is embit, pinned as a hash-locked PyPI release",
    "rust-bitcoin": "holds taproot types; Schnorr signatures are in rust-secp256k1",
}

SCHNORR = re.compile(r"schnorr|bip.?340|x-?only", re.I)
ECDSA = re.compile(r"\becdsa\b", re.I)
ECDH = re.compile(r"\becdh\b", re.I)


def audits_dir() -> pathlib.Path:
    here = pathlib.Path(__file__).resolve().parent
    for cand in (here / "audits", here):
        if any(cand.glob("*/report.json")):
            return cand
    sys.exit("no bundles found: run this from a checkout containing audits/")


def analyse(d: pathlib.Path) -> dict:
    rep = json.loads((d / "report.json").read_text())
    ref = ((rep.get("audit") or {}).get("parameters") or {}).get("ref") or ""
    proj = rep.get("project") or {}
    r = {"name": d.name, "commit": ref[:12] or "—", "upstream": proj.get("client_name") or "",
         "rows": 0, "shor": 0, "ecdsa": 0, "schnorr": 0, "ecdh": 0, "pq": 0, "pq_algos": Counter()}
    for row in rep.get("inventory", []):
        r["rows"] += 1
        blob = " ".join(str(row.get(k) or "") for k in ("algorithm", "parameter", "family", "usage", "library"))
        status = row.get("quantum_status") or ""
        if status == "vulnerable_shor":
            r["shor"] += 1
        if status == "pqc":
            r["pq"] += 1
            r["pq_algos"][row.get("algorithm") or "?"] += 1
        if SCHNORR.search(blob):
            r["schnorr"] += 1
        elif ECDSA.search(blob):
            r["ecdsa"] += 1
        elif ECDH.search(blob):
            r["ecdh"] += 1
    return r


def main(argv: list[str]) -> int:
    A = audits_dir()
    want_all = "--all" in argv
    as_json = "--json" in argv

    names = sorted(p.parent.name for p in A.glob("*/report.json"))
    targets = names if want_all else [n for n in SELF_CUSTODY if n in names]
    quoted = [n for n in SLICE_AS_QUOTED if n in names]
    if not targets:
        sys.exit("none of the self-custody codebases are present; try --all")
    res = [analyse(A / n) for n in targets]

    # Portfolio-wide, excluding translation duplicates and the sub-audit so nothing is counted twice.
    uniq = [n for n in names if not n.endswith("-en") and n != "trezor-vendored-crypto"]
    pq_strict, pq_loose = [], []
    for n in uniq:
        inv = json.loads((A / n / "report.json").read_text()).get("inventory", [])
        st = {row.get("quantum_status") for row in inv}
        if "pqc" in st:
            pq_strict.append(n)
        if st & {"pqc", "hybrid"}:
            pq_loose.append(n)

    if as_json:
        print(json.dumps({
            "codebases": [{**r, "pq_algos": dict(r["pq_algos"]),
                           "delegates_to": DELEGATES.get(r["name"])} for r in res],
            "portfolio": {"codebases": len(uniq), "pq_strict": pq_strict, "pq_or_hybrid": pq_loose},
        }, indent=2, ensure_ascii=False))
        return 0

    w = max(len(r["name"]) for r in res)
    print(f"{'codebase'.ljust(w)}  commit        rows  Shor  ECDSA  Schnorr  ECDH   PQ  post-quantum")
    print("-" * (w + 66))
    for r in sorted(res, key=lambda x: (-x["schnorr"], -x["pq"], x["name"])):
        pq = ", ".join(f"{a}x{n}" for a, n in sorted(r["pq_algos"].items())) or "-"
        print(f"{r['name'].ljust(w)}  {r['commit']:12}  {r['rows']:4}  {r['shor']:4}  {r['ecdsa']:5}  "
              f"{r['schnorr']:7}  {r['ecdh']:4}  {r['pq']:3}  {pq}")

    zeros = [r["name"] for r in res if r["schnorr"] == 0]
    if zeros:
        print("\nA zero in the Schnorr column is not a statement about what a wallet can do:")
        for n in zeros:
            why = DELEGATES.get(n, "no Schnorr primitive in the audited tree")
            print(f"  {n}: {why}")
        print("  Readiness for a consensus change cannot be read off a single repository.")

    have = [r["name"] for r in res if r["schnorr"] > 0]
    pq_here = [r["name"] for r in res if r["pq"] > 0]
    print(f"\nBIP-360 (P2MR) floor, Schnorr/BIP-340 present: {len(have)} of {len(res)}")
    print(f"Any post-quantum primitive: {len(pq_here)} of {len(res)}"
          f"{' -> ' + ', '.join(pq_here) if pq_here else ''}")
    if want_all:
        print("  (that count is over all bundles listed above, which include the -en translation duplicates")
        print("   and the sub-audit; the portfolio line below excludes them, which is why it is smaller)")
    if not want_all and len(quoted) == 10:
        qr = qs = 0
        for n in quoted:
            s = json.loads((A / n / "report.json").read_text())["summary"]
            qr += s["inventory_total"]
            qs += s["inventory_by_quantum_status"].get("vulnerable_shor", 0)
        tr = sum(r["rows"] for r in res)
        ts = sum(r["shor"] for r in res)
        print(f"\nThe ten-codebase slice quoted in dated write-ups is {qr} inventory rows and {qs} "
              f"Shor-breakable;")
        print(f"with bdk_wallet, audited 2026-10-29 after those were published, it is {tr} and {ts}.")
    print(f"\nAcross all {len(uniq)} audited codebases: {len(pq_loose)} contain post-quantum cryptography "
          f"counting pqc or hybrid, {len(pq_strict)} counting pqc strictly.")
    print(f"  {', '.join(pq_strict)}")
    print("\nNecessary, not sufficient: P2MR also needs address encoding, descriptors and PSBT support.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
