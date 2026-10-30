# Post-quantum cryptography review: zingolib @ 81d799775f11

*One-page brief* · Reviewed: 2026-10-29 23:55 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Zingo Labs — public repository (passive review)

Source: https://github.com/zingolabs/zingolib/tree/81d799775f11e882896e8710e8af12d6d4d29a41

**Post-quantum maturity:** Level 4 of 4 — post-quantum by default in the critical paths. **Next step:** Keep the inventory current and review new code paths before release.

**Findings:** Critical 0 · High 2 · Medium 8 · Low 31 · Info 11

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · pulldown-cmark 0.13.4 is affected by RUSTSEC-2026-0414 (QSI-2026-07465)\
   What to do: Upgrade to a fixed version (0.13.5).
2. **High** · rustls-webpki 0.101.7 is affected by GHSA-82j2-j2ch-gfr8 (CVE-2026-93599, RUSTSEC-2026-0104) (QSI-2026-07475)\
   What to do: Upgrade to a fixed version (0.103.13, 0.104.0-alpha.7).
3. **Medium** · rustls 0.21.12 is affected by GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346) (QSI-2026-07467)\
   What to do: Upgrade to a fixed version (0.23.46, 0.24.0-dev.2).
4. **Medium** · rustls 0.23.43 is affected by GHSA-2mjx-qc3c-rqvc (RUSTSEC-2026-0285) (QSI-2026-07470)\
   What to do: Upgrade to a fixed version (0.23.45).

37 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · threshold signing and MPC protocols | Pedersen commitment | Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the… |
| **Medium** · transaction and message signing | ECDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |

## Known vulnerable components

Advisories for the versions in use: 41; unlikely to apply to this build: 17 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 24.

---

Static review of source code and manifests; files analysed: 205. No requests were sent to the owner's systems.

Full report, content SHA-256: `b483913c63ed4f898763dd5a8af350e3d6f7242566bb78c10722ddaaaaa3ce49`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.